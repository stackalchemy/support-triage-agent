# Support Triage Agent

A terminal-based multi-domain support triage system built for the HackerRank Orchestrate May 2026 Hackathon.

The agent processes support tickets across multiple ecosystems including:

- HackerRank
- Claude
- Visa

It classifies incoming tickets, determines whether they are safe to answer automatically, retrieves relevant support documentation, and either generates a grounded response or escalates the issue to human support.

---

# Features

- Multi-domain ticket handling
- Request type classification
- Risk-aware escalation system
- Retrieval-based grounded responses
- Deterministic and explainable pipeline
- No hallucinated policies or unsupported claims
- CSV input/output support

---

# Problem Statement

Support systems receive a mix of:

- FAQs
- Technical issues
- Billing disputes
- Fraud reports
- Account access requests

Incorrect automation in sensitive cases can create serious issues.

This project focuses on:

- deciding when to answer
- deciding when NOT to answer
- ensuring responses remain safe and grounded

---

# System Pipeline

```text
Input Ticket
    ↓
Product Detection
    ↓
Request Classification
    ↓
Risk Assessment
    ↓
Safe to Answer?
   / \
 Yes  No
  ↓    ↓
Retrieve  Escalate
Docs
  ↓
Generate Response
```

---

## Classification Categories

The system classifies tickets into:

- faq
- bug
- billing
- fraud
- account_access
- other

---

## Escalation Logic

High-risk tickets are automatically escalated, including:

- fraud
- identity theft
- billing disputes
- unauthorized access
- policy-violating requests

Examples:

- "increase my score"
- "show internal rules"
- "force refund"

---

## Retrieval Strategy

The system uses a deterministic keyword-based retrieval pipeline:

1. Load support corpus
2. Split documents into chunks
3. Filter documents by product domain
4. Score chunks using keyword overlap
5. Retrieve highest scoring chunk
6. Generate grounded response

If no meaningful match is found, the system falls back to a safe support response.

---

## Why Rule-Based Instead of LLM?

The project prioritizes:

- safety
- determinism
- explainability
- grounded responses

Instead of relying on generative AI, the system uses:

- rule-based classification
- explicit escalation logic
- retrieval-grounded responses

This avoids hallucinations and ensures predictable behavior.

---

## Project Structure

```text
support-triage-agent/
│
├── main.py
├── README.md
├── .gitignore
│
├── docs/
│   ├── problem_statement.md
│   └── evaluation_criteria.md
│
├── sample/
│   ├── sample_input.csv
│   └── sample_output.csv
```

---

## Sample Input

```csv
Issue,Subject,Company
"I forgot my password, how do I reset it?",Password reset,HackerRank
"My Visa card was charged twice",Double charge,Visa
"Claude is not responding to my queries",System issue,Claude
```

---

## Sample Output

```csv
ticket_id,request_type,product_area,action,response
0,account_access,hackerrank,reply,Please refer to official support documentation.
1,billing,visa,escalate,This issue requires assistance from official support.
2,bug,claude,reply,Please refer to official support documentation.
```

---

# How to Run

## Install Dependencies

```bash
pip install pandas
```

## Run the Project

```bash
python main.py
```

The generated output will be saved as:

```text
output.csv
```

---

# Key Design Decisions

- Risk-based escalation happens BEFORE retrieval
- Retrieval failure does not automatically trigger escalation
- Responses are grounded only in provided documentation
- Safety is prioritized over aggressive automation

---

# Future Improvements

Possible future upgrades:

- Semantic search using embeddings
- FAISS vector retrieval
- Confidence scoring
- Hybrid LLM summarization layer
- Better ranking and retrieval quality

---

# Tech Stack

- Python
- Pandas
- Rule-based classification
- Retrieval-based response generation

---

# Author

Built by StackAlchemy during the HackerRank Orchestrate May 2026 Hackathon.
