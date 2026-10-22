# StudyOS — AI-Powered PDF Study Assistant

StudyOS is a full-stack web application that helps students study PDF documents using AI. Upload a document, read it in the browser, and ask questions grounded in relevant content retrieved from your PDFs.

Built with React, FastAPI, PostgreSQL, pgvector, and LiteLLM, StudyOS explores how retrieval-augmented generation (RAG) can make learning from documents more interactive.

## Architecture

![StudyOS Complete Architecture](files/StudyOS%20AI%20PDF%20Study%20Workflow.png)

## Demo

**Demo video:** [Watch StudyOS in action](https://www.youtube.com/watch?v=w26d7C3KgVw)

## Features

- **PDF uploads:** Upload and manage study documents.
- **In-browser PDF viewer:** Read documents directly in the application.
- **PDF processing:** Extract text and organize content by page and paragraph.
- **Semantic search:** Retrieve relevant document passages using vector embeddings.
- **AI document chat:** Ask questions about uploaded PDFs and receive context-grounded answers.
- **Page references:** Locate relevant document pages to help verify AI responses.
- **Authentication:** Protect user-specific operations using JWT-based authentication and HTTP-only cookies.
- **Configurable AI providers:** Integrate supported language models through LiteLLM.

## Tech Stack

| Component | Technology |
|---|---|
| Frontend | React, Vite, React Router |
| Backend | Python, FastAPI |
| Database | PostgreSQL, SQLAlchemy |
| Vector search | pgvector |
| PDF processing | PyMuPDF |
| Embedding model | BAAI/bge-small-en-v1.5 |
| LLM integration | LiteLLM |
| Authentication | JWT, HTTP-only cookies |

## How It Works

1. **Upload:** An authenticated user uploads a PDF through the frontend.
2. **Extract:** The backend extracts document text and organizes it into searchable passages.
3. **Embed:** The embedding service generates vector representations for eligible passages.
4. **Store:** PostgreSQL stores document metadata, extracted text, and embeddings using pgvector.
5. **Retrieve:** When a user asks a question, the backend searches for relevant passages using vector similarity.
6. **Generate:** Retrieved context is sent to the selected language model through LiteLLM.
7. **Respond:** The application returns an AI-generated answer with relevant page references where available.

## Getting Started

### Prerequisites

- Python 3.12 or a compatible version
- Node.js and npm
- PostgreSQL with the pgvector extension
- Git
- Credentials for a supported language-model provider

### 1. Clone the Repository

```bash
git clone https://github.com/vishwasBelieve/studyOS.git
cd studyOS
```

### 2. Configure PostgreSQL

Create a PostgreSQL database for StudyOS and enable the pgvector extension:

```sql
CREATE EXTENSION IF NOT EXISTS vector;
```

Ensure the database exists and that your PostgreSQL user has permission to access it.

### 3. Configure Environment Variables

Create a `.env` file in the `backend/` directory.

```env
DATABASE_URL=postgresql://USERNAME:PASSWORD@localhost:5432/studyos_db
SECRET_KEY=replace_with_a_secure_random_secret
```

Replace the example database credentials with your actual PostgreSQL configuration.

Generate a secure secret key using Python:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

Copy the generated value into `SECRET_KEY`.

**Security:** Never commit your `.env` file, database password, or secret key to GitHub. Keep `.env` excluded through `.gitignore`.

### 4. Set Up the Backend

From the repository root:

```bash
cd backend
python3 -m venv studyenv
source studyenv/bin/activate
pip install -r requirements.txt
```

Ensure your environment variables are configured before starting the application.

Start the FastAPI backend:

```bash
uvicorn app.main:app --reload
```

The API should be available at:

- API: http://127.0.0.1:8000
- Interactive API documentation: http://127.0.0.1:8000/docs

### 5. Start the Embedding Server

StudyOS requires a locally running embedding server to convert document text into vector embeddings for semantic search.

The server uses `BAAI/bge-small-en-v1.5` through Sentence Transformers. The model is loaded from the local cache (`local_files_only=True`), so **you must have the model downloaded locally before starting the server**.

Open a separate terminal from the project root:

```bash
cd backend/app/embedding_service.py
source studyenv/bin/activate
uvicorn embedding_service:app --host 127.0.0.1 --port 8001

```

Wait until you see:

```text
Loading embedding model...
Embedding model ready
```

Keep this terminal running while using StudyOS. The backend needs this service to generate embeddings.

**Important:** The embedding model must already exist in your local Hugging Face/Sentence Transformers cache. If it hasn't been downloaded, download it once before running the server.



### 6. Set Up the Frontend

Open a third terminal from the repository root:

```bash
cd frontend
npm install
npm run dev
```

Open the local URL displayed by Vite, typically:

http://localhost:5173

Ensure the frontend API URL and backend CORS configuration match your local environment.

### 7. Configure AI Integration

Configure a language-model provider supported by the application through LiteLLM.

Supply any required provider API keys using the configuration expected by your application. Do not hardcode API keys in the source code or commit them to version control.

The embedding model and language model serve different purposes: embeddings support semantic retrieval, while the language model generates answers using retrieved context.

## Engineering Highlights

- Built a full-stack application using React and FastAPI.
- Implemented PDF text extraction and document processing.
- Integrated embedding generation and semantic retrieval.
- Used PostgreSQL and pgvector for vector similarity search.
- Connected retrieved document context to language-model inference through LiteLLM.
- Implemented authenticated operations using JWTs and HTTP-only cookies.
- Associated retrieved passages with document page information to support answer verification.

## Security and Privacy

- Keep API keys, passwords, and authentication secrets out of version control.
- Validate uploaded files and enforce appropriate upload limits.
- Ensure users can access only their own protected documents.
- Avoid committing private PDFs, generated files, or sensitive data.
- Treat retrieved document content as untrusted input when constructing AI prompts.

## Future Improvements

- Docker-based deployment and service orchestration.
- Improved PDF processing progress reporting.
- Retrieval evaluation and answer-quality improvements.
- Page-specific queries and summaries.
- Automated tests for authentication, uploads, and AI endpoints.
- Production deployment with persistent storage and monitoring.
- Personalized AI study assistance.

## License

No license has been specified yet. Unless a license is added, others should not assume they have permission to reuse, modify, or redistribute this project.

---

*StudyOS is a personal project exploring full-stack development, database-backed semantic search, and AI-powered learning applications.*
