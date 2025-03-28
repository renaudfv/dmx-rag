import os
from scrapy.crawler import CrawlerProcess
from crawler.spiders import SpecSheetSpider
from processors.pdf_extractor import PDFProcessor
from rag.query_engine import RAGEngine
from rag.evaluator import RAGEvaluator
import argparse

CRAWL = False
PROCESS_PDFS = False

def main():
    # Configuration
    WEBSITES = [
        'https://www.adj.com/',
        'https://www.chauvetprofessional.com/',
        'https://www.elationlighting.com/',
        'https://www.martin.com/',
        'https://www.enttec.com/',
        'https://www.etcconnect.com/',
    ]
    DOWNLOAD_DIR = 'downloads'
    
    # Step 1: Web Crawling
    if CRAWL:
        process = CrawlerProcess(settings={
            'ITEM_PIPELINES': {
                'crawler.pipelines.CustomFilesPipeline': 1,  # Use the custom pipeline
            },
            'FILES_STORE': DOWNLOAD_DIR,  # Directory to store downloaded files
            'LOG_LEVEL': 'ERROR',  # Set log level to INFO for better visibility
        })

        process.crawl(
            SpecSheetSpider, 
            start_urls=WEBSITES, 
            download_dir=DOWNLOAD_DIR
        )
        process.start()

    
    # Step 2: PDF Processing
    rag_engine = RAGEngine()
    if PROCESS_PDFS:
        processed_docs = PDFProcessor.process_pdf_directory(DOWNLOAD_DIR)
        print('Processed docs')
    
        # Index documents
        document_texts = [doc['text'] for doc in processed_docs]
        rag_engine.index_documents(document_texts)
    
    # Add evaluation mode
    parser = argparse.ArgumentParser()
    parser.add_argument('--evaluate', action='store_true', help='Run RAG evaluation')
    args = parser.parse_args()

    if args.evaluate:
        # Sample evaluation questions
        eval_questions = [
            "What is the DMX channel count of the latest Martin fixture?",
            "Compare the power consumption between ADJ and Chauvet fixtures",
            "What are the beam angles available in ETC's latest LED profile?"
        ]
        
        evaluator = RAGEvaluator()
        contexts = []
        answers = []
        
        # Get responses for evaluation
        for question in eval_questions:
            result = rag_engine.query(question)
            # Get retrieved contexts from the last query
            contexts.append(rag_engine.last_context)
            answers.append(result)
        
         # Run evaluation
        eval_results = evaluator.evaluate(
            questions=eval_questions,
            contexts=contexts,
            answers=answers
        )
        
        print("\nRAG Evaluation Results:")
        print(f"Context Relevance: {eval_results.context_relevance:.2f}")
        print(f"Answer Similarity: {eval_results.answer_similarity:.2f}")
        print(f"Coverage Score: {eval_results.coverage_score:.2f}")
        return

    # Interactive Query Loop
    while True:
        query = input("Enter your product specification query (or 'exit' to quit): ")
        
        if query.lower() == 'exit':
            break
        
        result = rag_engine.query(query)
        print("\nRAG Response:")
        print(result)
        print("\n" + "-"*50 + "\n")

if __name__ == '__main__':
    main()