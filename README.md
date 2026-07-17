# Tri9T Assignment

A backend system for document versioning and AI-powered test case generation. The project ingests PDF documents, tracks changes across document versions, and generates test cases for selected document sections using an LLM.

---

# Prerequisites

- Python 3.10+
- SQLite
- MongoDB (running locally)
- OpenRouter API Key
- Google Gemini API Key

---

# Installation

## 1. Clone the repository

```bash
git clone <repository-url>
cd <repository-folder>
```

## 2. Create a virtual environment

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

# Environment Variables

Create a `.env` file in the project root.

Example:

```env
OPENROUTER_API_KEY=your_openrouter_api_key
GEMINI_API_KEY=your_gemini_api_key

SQLITE_DATABASE=database.db
MONGODB_URI=mongodb://localhost:27017
MONGODB_DATABASE=tri9t
```

Ensure MongoDB is running before generating test cases.

---

# Running the Backend

Start the FastAPI server:

```bash
python -m uvicorn main:app --reload
```

or

```bash
python3 -m uvicorn main:app --reload
```

Swagger UI:

```
http://127.0.0.1:8000/docs
```

---

# Project Workflow

The project is intended to be used in the following order.

## Step 1 - Ingest a Document

Run the document ingestion pipeline manually.

To ingest a document the cli command is :
    python3 ingest_document.py data/{doc_name}

The ingestion process:

- Reads the PDF
- Extracts sections and tables
- Builds the document tree
- Computes hashes
- Stores the document in SQLite
- Automatically assigns a version number

After ingestion, the document becomes available through the APIs.

---

## Step 2 - Browse the Document

### List document sections

```
GET /documents/{document_name}/sections
```

### List all nodes

Latest version:

```
GET /documents/{document_name}/nodes
```

Specific version:

```
GET /documents/{document_name}/nodes?version=1
```

### Search document

```
GET /documents/{document_name}/search
```

### View a node

```
GET /nodes/{node_id}
```

---

## Step 3 - Compare Document Versions

Compare two versions of the same document.

```
GET /documents/{document_name}/diff
```

Required parameters:

- document_name
- old_version
- new_version
- node_id

The response indicates whether the selected section is:

- Added
- Removed
- Modified
- Unchanged

---

## Step 4 - Create a Selection

Create a reusable selection of document sections.

```
POST /selections
```

Example request:

```json
{
    "name": "Authentication",
    "node_ids": [5, 6, 7]
}
```

The API returns a `selection_id`.

---

## Step 5 - Generate Test Cases

Generate AI-powered test cases for a selection.

```
POST /qa/generate
```

Example request:

```json
{
    "selection_id": 1
}
```

The generated test suite is stored in MongoDB.

---

## Step 6 - Retrieve Generated Test Suites

Latest generated test suite:

```
GET /qa/{selection_id}
```

Generation history:

```
GET /qa/{selection_id}/history
```

Retrieve test suites containing a specific node:

```
GET /qa/node/{node_id}
```

---

# Testing the APIs

Once the server is running:

1. Open

```
http://127.0.0.1:8000/docs
```

2. Expand any endpoint.

3. Click **Try it out**.

4. Enter the required parameters.

5. Click **Execute**.

All APIs can be tested directly from the Swagger interface.

---

# Testing Versioning (v1 → v2 Re-ingestion)

The system automatically versions documents that share the same document name.

### Create Version 1

1. Place the initial PDF in the input location used by the ingestion pipeline.
2. Run the ingestion script.
3. The document is stored as **Version 1**.

### Create Version 2

1. Modify the original PDF (add, remove, or edit some content).
2. Save it using the **same document name**.
3. Run the ingestion script again.
4. The system detects the existing document and stores the new copy as **Version 2**.

You can verify this by calling:

```
GET /documents/{document_name}/nodes?version=1
```

and

```
GET /documents/{document_name}/nodes?version=2
```

To compare both versions:

```
GET /documents/{document_name}/diff
```

using:

- `old_version = 1`
- `new_version = 2`

---

# Notes

- Document ingestion is performed manually.
- The latest document version is returned by default.
- A specific version can be requested where supported.
- Generated test suites are stored in MongoDB.
- Swagger UI is available for testing all APIs.

- to create the sqlite db after deletion cli command is:
    python3 create_db.py
- ingest_document.py create_db.py check_staleness.py compare_versions.py create_selection.py generate_qa.py retirieve_qa.py view_qa.py. these are all cli runnable files that also perform the tasks.

---
