# AI Support Dialogue Analysis

LLM-powered system for generating and analyzing customer support conversations.

This project simulates realistic support chats and evaluates agent performance using a Large Language Model (LLM).

---

## Features

### Dialogue Generation
- Generates realistic customer–agent conversations
- Controlled scenario simulation:
  - customer intent
  - customer attitude
  - agent behavior
  - case outcome

### Dialogue Analysis
Each dialogue is analyzed to extract:

- **intent** — customer request category
- **satisfaction** — customer satisfaction level
- **quality_score** — agent performance (1–5)
- **agent_mistakes** — detected support mistakes

---


---

## Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
