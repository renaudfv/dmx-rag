import ollama
import chromadb
from sentence_transformers import SentenceTransformer
import torch

class RAGEngine:
    def __init__(self, 
                 embedding_model='all-MiniLM-L6-v2', 
                 llm_model='llama2'):
        # Initialize embedding model
        self.embedder = SentenceTransformer(embedding_model)
        
        # Initialize ChromaDB
        self.client = chromadb.PersistentClient('./chroma')
        self.collection = self.client.get_or_create_collection("product_specs")
        
        # LLM model
        self.llm_model = llm_model
        self.last_context = None

    def index_documents(self, documents):
        """
        Index documents in ChromaDB
        
        :param documents: List of text documents
        """
        for idx, doc in enumerate(documents):
            # Generate embedding
            embedding = self.embedder.encode(doc).tolist()
            
            # Add to ChromaDB
            self.collection.add(
                embeddings=embedding,
                documents=[doc],
                ids=[f'doc_{idx}']
            )
    
    def query(self, query_text, top_k=3):
        """
        Retrieve and generate response
        
        :param query_text: User's query
        :param top_k: Number of documents to retrieve
        :return: Generated response
        """
        # Embed query
        query_embed = self.embedder.encode(query_text).tolist()
        
        # Retrieve documents
        results = self.collection.query(
            query_embeddings=[query_embed],
            n_results=top_k
        )
        
        # Retrieved context
        context = " ".join(results['documents'][0])
       
        # Store context for evaluation
        self.last_context = context

        # Generate response with Ollama
        response = ollama.chat(model=self.llm_model, messages=[
            {
                'role': 'system', 
                'content': 'You are a helpful product specification assistant.'
            },
            {
                'role': 'user', 
                'content': f'Context: {context}\n\nQuestion: {query_text}'
            }
        ])
        
        return response['message']['content']