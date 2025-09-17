# Solution Advisory Agent (AIE) — Starter

This starter shows how the **Solution Advisory Agent** fits into your 5-agent architecture and provides a working scaffold:
- RAG index builder over **Regulations** + **Syllabus** PDFs
- Advisory agent that retrieves context + reads **student record** (dummy JSON)
- Minimal **orchestrator API** and a **UI subpage** to ask questions

## Where this fits
- **UI Layer** → `ui/static/advisory.html` (Solution Advisory subpage in myAmrita clone)
- **Orchestrator** → `orchestrator/orchestrator.py` (exposes `/advisory/ask`)
- **Solution Advisory Agent** → `agents/solution_advisory.py`
- **Communications** → `comms/comms.py` (stub ready for integration)
- **Monitoring** → later will call the same advisory API for proactive suggestions

## Quick start
1) Install dependencies (suggested):
```
pip install fastapi uvicorn pydantic sentence-transformers chromadb pypdf requests
# For local LLM, install Ollama and pull a model:
#   https://ollama.com/download
#   ollama pull llama3:instruct
```
2) Place your PDFs:
- Regulations PDF in `./data/policies/`
- AIE syllabus PDF in `./data/syllabus/`

3) Build the vector index:
```
python rag/index_builder.py --config ./configs/config.yaml
```

4) Run the server (UI + API):
```
uvicorn ui.server:app --reload
# Open http://localhost:8000/advisory.html
```

5) Try a query with student ID `AIE23A001`:
- Example: "I have a backlog in Data Structures. What is the best way to clear it?"

## Notes
- Intent classification + advisory reasoning use your local **Ollama** model (edit `configs/config.yaml`).
- The agent returns structured JSON; the UI renders key parts.
- Add FA approval + email by importing `comms.send_email(...)` where needed.

## Next steps
- Add **policy-aware rules** (e.g., only 1 contact course allowed) as code checks before LLM.
- Add **Monitoring Agent** to proactively call `/advisory/ask` when backlogs are detected.
- Log each advisory case to a DB for auditing.
