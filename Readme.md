# 🚀 Codeforces Chatbot with CodeBERT for Competitive Programming

## 🌟 Overview
Codeforces Chatbot is an intelligent AI assistant designed to help competitive programmers with Codeforces problems. Powered by **CodeBERT** and **Retrieval-Augmented Generation (RAG)**, this chatbot retrieves problem statements, editorials, and metadata to provide insightful responses.

### 🔥 Key Features
- **Advanced Retrieval**: Uses a vector database to efficiently fetch relevant problems and solutions.
- **CodeBERT Embeddings**: Generates high-quality embeddings for problem texts and editorials.
- **Smart Query Analysis**: Detects problem difficulty, topics, and type of query (e.g., explanation vs. solution request).
- **Seamless Chatbot Interface**: Enables real-time interaction for competitive programming assistance.
- **Highly Optimized Vector Search**: Uses FAISS-based **HNSW** and **IVF** indexing for fast retrieval.


## 🛠 Installation & Setup
### Prerequisites
- Python 3.8+
- PyTorch (for CodeBERT)
- FAISS (for vector storage)
- Required Python packages

### 🔧 Installation
Clone the repository and install dependencies:
```bash
git clone https://github.com/yourrepo/codeforces-chatbot.git
cd codeforces-chatbot
pip install -r requirements.txt
```

## 🚀 Usage
### **1️⃣ Running the Chatbot**
Run `main.py` to start the chatbot interface:
```bash
python main.py
```

### **2️⃣ Testing CodeBERT Embeddings**
```python
from src.embeddings import CodeBERTEmbedder

# Test single embedding
embedder = CodeBERTEmbedder()
test_text = "Find the maximum subarray sum"
embedding = embedder.generate_embedding(test_text)
print(f"Embedding shape: {embedding.shape}")
```

### **3️⃣ Example Chatbot Interaction**
```python
from src.embeddings import CodeBERTEmbedder
from src.vectorstore import VectorStore
from src.retriever import RAGRetriever
from src.chatbot import CPChatbot

# Initialize components
embedder = CodeBERTEmbedder()
vector_store = VectorStore()
retriever = RAGRetriever(embedder, vector_store)

# Create chatbot
system_message = '''I am solving a competitive programming problem and need help understanding its editorial.
Answer my questions regarding the editorial. Let me know if I'm misunderstanding anything.
Do not write or debug code.'''
chatbot = CPChatbot(retriever, system_message)

# Chat
response = chatbot.chat("How do I solve problem C from Contest #792?")
print(response)
```

## 📌 How It Works
### **1️⃣ Embedding Generation**
- Uses **CodeBERT** to convert problem texts and editorials into embeddings.

### **2️⃣ Efficient Retrieval with FAISS**
- Stores embeddings in a **vector database** (FAISS) for fast search.
- Uses **HNSW** and **IVF** indexing to optimize similarity search.

### **3️⃣ Query Processing & Filtering**
- Detects **query type** (solution request, explanation request, etc.).
- Filters results based on **difficulty level** and **problem topics**.
- Returns the most relevant context with **confidence scores**.

### **4️⃣ Chatbot Interaction**
- Processes user queries and provides **context-aware** responses.
- Helps users understand **problem-solving strategies** and **editorial insights**.

## 🚀 Future Enhancements
- 🔹 **GPT-powered response refinement**
- 🔹 **Fine-tuned models for competitive programming**
- 🔹 **Web-based UI for chatbot interaction**
- 🔹 **Integration with Codeforces API for real-time updates**

## 📜 License
This project is licensed under the MIT License.

## 💡 Acknowledgments
- **CodeBERT** for embedding generation
- **FAISS** for efficient vector search
- **Competitive programming community** for inspiration

---
_🔥 Elevate your competitive programming skills with AI! 🚀_

