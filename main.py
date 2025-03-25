import os
from scrapy.crawler import CrawlerProcess
from crawler.spiders import SpecSheetSpider
from processors.pdf_extractor import PDFProcessor
from rag.query_engine import RAGEngine

CRAWL = False

def main():
    # Configuration
    TARGET_WEBSITE = 'https://www.chauvetprofessional.com/'
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
            start_urls=[TARGET_WEBSITE], 
            download_dir=DOWNLOAD_DIR
        )
        process.start()

        process.crawl(
            SpecSheetSpider, 
            start_urls=['https://www.adj.com/'], 
            download_dir=DOWNLOAD_DIR
        )
        process.start()
    
    # Step 2: PDF Processing
    processed_docs = PDFProcessor.process_pdf_directory(DOWNLOAD_DIR)
    print('Processed docs')
    # # Step 3: Create RAG System
    rag_engine = RAGEngine()
    
    # Index documents
    document_texts = [doc['text'] for doc in processed_docs]
    rag_engine.index_documents(document_texts)
    
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