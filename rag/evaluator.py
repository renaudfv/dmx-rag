from sentence_transformers import SentenceTransformer, util
from dataclasses import dataclass
from typing import List, Dict
import torch

@dataclass
class EvaluationResult:
    context_relevance: float
    answer_similarity: float
    coverage_score: float

class RAGEvaluator:
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)
        # Use MPS if available
        self.device = "mps" if torch.backends.mps.is_available() else "cpu"
        self.model.to(self.device)

    def evaluate(self, 
                questions: List[str],
                contexts: List[List[str]], 
                answers: List[str]) -> EvaluationResult:
        """
        Evaluate RAG system performance using semantic similarity
        
        Args:
            questions: List of question strings
            contexts: List of context strings for each question
            answers: List of generated answer strings
        Returns:
            EvaluationResult containing similarity scores
        """
        # Calculate context relevance
        context_scores = []
        for question, context_list in zip(questions, contexts):
            # Encode question and contexts
            q_embedding = self.model.encode(question, convert_to_tensor=True)
            c_embeddings = self.model.encode(context_list, convert_to_tensor=True)
            
            # Calculate similarities
            similarities = util.pytorch_cos_sim(q_embedding, c_embeddings)
            context_scores.append(float(similarities.mean()))

        # Calculate answer similarity to context
        answer_scores = []
        for answer, context_list in zip(answers, contexts):
            a_embedding = self.model.encode(answer, convert_to_tensor=True)
            c_embeddings = self.model.encode(context_list, convert_to_tensor=True)
            
            similarities = util.pytorch_cos_sim(a_embedding, c_embeddings)
            answer_scores.append(float(similarities.mean()))

        # Calculate coverage (how much of the context is used in the answer)
        coverage_scores = []
        for answer, context_list in zip(answers, contexts):
            answer_tokens = set(answer.lower().split())
            context_tokens = set(" ".join(context_list).lower().split())
            coverage = len(answer_tokens.intersection(context_tokens)) / len(answer_tokens)
            coverage_scores.append(coverage)

        return EvaluationResult(
            context_relevance=sum(context_scores) / len(context_scores),
            answer_similarity=sum(answer_scores) / len(answer_scores),
            coverage_score=sum(coverage_scores) / len(coverage_scores)
        )