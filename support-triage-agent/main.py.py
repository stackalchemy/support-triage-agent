import pandas as pd
import os

# -------------------------------
# LOAD DOCUMENTS
# -------------------------------
def load_docs():
    docs = []
    base_path = "data"

    for product in ["claude", "hackerrank", "visa"]:
        folder = os.path.join(base_path, product)

        for file in os.listdir(folder):
            file_path = os.path.join(folder, file)

            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    text = f.read()

                    # skip useless export/index files
                    if "exported" in text.lower():
                        continue

                    # split into chunks
                    parts = text.split("\n\n")

                    for part in parts:
                        if len(part.strip()) > 80:
                            docs.append({
                                "product": product,
                                "text": part
                            })
            except:
                continue

    return docs


docs = load_docs()

# -------------------------------
# CLASSIFICATION
# -------------------------------
def classify_request(ticket):
    t = str(ticket).lower()

    if any(x in t for x in ["fraud", "stolen", "unauthorized", "identity"]):
        return "fraud"

    if any(x in t for x in ["charged", "payment", "refund", "money", "dispute"]):
        return "billing"

    if any(x in t for x in ["not working", "error", "failing", "down", "issue"]):
        return "bug"

    if any(x in t for x in ["login", "access", "account"]):
        return "account_access"

    if any(x in t for x in [
        "how", "help", "can you", "request",
        "unable", "cannot", "not able"
    ]):
        return "faq"

    return "other"


# -------------------------------
# ESCALATION LOGIC
# -------------------------------
def decide_action(ticket, request_type):
    t = str(ticket).lower()

    # High-risk cases
    if any(x in t for x in [
        "fraud", "stolen", "unauthorized",
        "charged twice", "identity", "urgent cash"
    ]):
        return "escalate"

    # Impossible or policy violations
    if any(x in t for x in [
        "increase my score", "review my answers",
        "ban the seller", "force refund"
    ]):
        return "escalate"

    # Security probing
    if any(x in t for x in [
        "show internal", "rules", "logic", "delete all files"
    ]):
        return "escalate"

    # Billing → safer to escalate
    if request_type == "billing":
        return "escalate"

    return "reply"


# -------------------------------
# RETRIEVAL (improved matching)
# -------------------------------
def retrieve_doc(ticket, product):
    t = str(ticket).lower()

    product_docs = [d for d in docs if d["product"] == product]

    best_doc = None
    best_score = 0

    for d in product_docs:
        text = d["text"].lower()
        score = 0

        # strong keyword matches
        if "login" in t and "login" in text:
            score += 5
        if "password" in t and "password" in text:
            score += 5
        if "refund" in t and "refund" in text:
            score += 5
        if "payment" in t and "payment" in text:
            score += 5
        if "account" in t and "account" in text:
            score += 5

        # fallback word matching
        for word in t.split():
            if len(word) > 3 and word in text:
                score += 1

        if score > best_score:
            best_score = score
            best_doc = d["text"]

    return best_doc


# -------------------------------
# CLEAN DOCUMENT
# -------------------------------
def clean_doc(text):
    lines = text.split("\n")

    useful = []
    for line in lines:
        line = line.strip()

        if not line:
            continue

        if any(x in line.lower() for x in [
            "title:", "source_url", "final_url",
            "last_modified", "exported", "#", "##"
        ]):
            continue

        useful.append(line)

    return " ".join(useful)


# -------------------------------
# MAIN PIPELINE
# -------------------------------
df = pd.read_csv("support_tickets/support_tickets.csv")

outputs = []

for i, row in df.iterrows():
    ticket = row["Issue"]
    product = str(row["Company"]).lower()

    # Fix missing product
    if product == "nan" or product == "none":
        t = str(ticket).lower()
        if "visa" in t:
            product = "visa"
        elif "claude" in t:
            product = "claude"
        elif "hackerrank" in t:
            product = "hackerrank"
        else:
            product = "unknown"

    request_type = classify_request(ticket)
    action = decide_action(ticket, request_type)

    if action == "escalate":
        response = "This issue requires assistance from the official support team. Please contact support."

    else:
        doc = retrieve_doc(ticket, product)

        if doc:
            clean_text = clean_doc(doc)
            response = f"According to official {product} support documentation: {clean_text[:200]}"
        else:
            response = f"This appears to be a {request_type} issue related to {product}. Please refer to the official {product} support documentation or contact support."

    outputs.append({
        "ticket_id": i,
        "request_type": request_type,
        "product_area": product,
        "action": action,
        "response": response
    })


# -------------------------------
# SAVE OUTPUT
# -------------------------------
pd.DataFrame(outputs).to_csv("output.csv", index=False)

print("Done. Check output.csv")