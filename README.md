# BUILDING END TO END RAG FRAMEWORK

```text
rag_project/
├── app/
│   ├── main.py
│   ├── ui/
│   │   └── streamlit_app.py
│   └── config.py
├── modules/
│   ├── __init__.py
│   ├── loaders/
│   │   ├── __init__.py
│   │   ├── base_loader.py
│   │   ├── file_loader.py
│   │   ├── web_loader.py
│   │   ├── folder_loader.py
│   │   ├── registry.py
│   │   └── normalize.py
│   ├── chunking/
│   │   └── __init__.py
│   ├── embeddings/
│   │   └── __init__.py
│   ├── vectorstore/
│   │   └── __init__.py
│   ├── retrieval/
│   │   └── __init__.py
│   ├── memory/
│   │   └── __init__.py
│   ├── guardrails/
│   │   └── __init__.py
│   └── graph/
│       └── __init__.py
├── data/
│   ├── raw/
│   ├── processed/
│   └── metadata/
├── requirements.txt
├── README.md
└── .env

```
