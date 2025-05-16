
# 🚀 Codeforces Assistant with CodeBERT for Competitive Programming

## 🌟 Overview
Codeforces Assistant is an intelligent AI-powered tool designed to aid competitive programmers with Codeforces problems. Utilizing **CodeBERT** and **Retrieval-Augmented Generation (RAG)**, the system fetches relevant problem statements, editorials, and metadata to provide insightful responses.

### 🔥 Key Features
- **Advanced Retrieval System**: Leverages FAISS for efficient similarity search using problem embeddings.
- **CodeBERT-Powered Embeddings**: Transforms Codeforces problems and editorials into rich vector representations.
- **Intelligent Query Understanding**: Detects problem tags, difficulty levels, and query intent (e.g., explanation, clarification).
- **Seamless User Interaction**: Offers a command-line interface for real-time, context-aware assistance.
- **Optimized Vector Search**: Combines HNSW and IVF indexing in FAISS for speed and accuracy.

## 🛠 Installation & Setup

### Prerequisites
- Python 3.8+
- PyTorch
- FAISS
- Required Python packages

### 🔧 Installation
Clone the repository and install dependencies:
```bash
git clone https://github.com/Paras20222/ChatBot_For_CP.git
cd ChatBot_For_CP
pip install -r requirements.txt
```

## 🚀 Usage

### 1️⃣ Start the Assistant
```bash
python main.py
```

### 2️⃣ Test CodeBERT Embeddings
```python
from src.embeddings import CodeBERTEmbedder

embedder = CodeBERTEmbedder()
text = "Find the maximum subarray sum"
embedding = embedder.generate_embedding(text)
print(f"Embedding shape: {embedding.shape}")
```

### 3️⃣ Sample Interaction Flow
```python
from src.embeddings import CodeBERTEmbedder
from src.vectorstore import VectorStore
from src.retriever import RAGRetriever
from src.assistant import CPAssistant

embedder = CodeBERTEmbedder()
vector_store = VectorStore()
retriever = RAGRetriever(embedder, vector_store)

system_message = '''I'm working on a Codeforces problem and need help understanding its editorial.
Please help me clarify any doubts I have. Avoid writing or debugging code.'''

assistant = CPAssistant(retriever, system_message)
response = assistant.chat("How to solve problem C from Contest #792?")
print(response)
```

## ⚙️ How It Works

### 1️⃣ Embedding Generation
- Uses **CodeBERT** to convert problems and editorials into dense vectors.

### 2️⃣ Vector Store with FAISS
- Stores embeddings in FAISS with **HNSW** and **IVF** indexing for fast and scalable retrieval.

### 3️⃣ Query Detection & Filtering
- Analyzes query for type, difficulty, and topic using metadata and keyword analysis.
- Retrieves and ranks the most relevant contexts using similarity scores.

### 4️⃣ User Interaction
- Returns context-aware suggestions and explanations to enhance understanding of Codeforces problems.

