flowchart TB
  subgraph UI[Frontend UI - Streamlit]
    U1[Upload Video]
    U2[Processing Status]
    U3[Ask Question]
    U4[Video Player + Click-to-Timestamp Results]
  end

  subgraph API[Backend API - FastAPI]
    A1[POST /videos/upload]
    A2[POST /videos/:id/process]
    A3[GET /videos/:id/status]
    A4[POST /query]
    A5[GET /videos/:id/stream]
  end

  subgraph JOBS[Background Worker - local]
    J1[Transcription Job]
    J2[Indexing Job]
  end

  subgraph PIPE[AI Pipeline]
    P1[faster-whisper: transcript segments<br/>start/end timestamps]
    P2[Chunker: create text chunks<br/>with start,end]
    P3[Embeddings: sentence-transformers]
    P4[Vector Index: FAISS]
    P5[RAG Retriever: top-k chunks + sources]
    P6[Optional LLM: local Ollama OR extractive answer]
  end

  subgraph STORE[Storage Layer]
    S1[(Filesystem: storage/videos)]
    S2[(Filesystem: storage/transcripts)]
    S3[(Filesystem: storage/index)]
    S4[(SQLite: metadata + job status)]
  end

  U1 --> A1 --> S1
  U2 <-- A3 --> S4

  U1 --> A2 --> J1 --> P1 --> S2 --> S4
  J1 --> J2 --> P2 --> P3 --> P4 --> S3 --> S4

  U3 --> A4 --> P5 --> P4
  P5 --> S2
  P5 --> P6
  P5 --> A4 --> U4

  U4 --> A5 --> S1