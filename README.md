# DMX-RAG: Lighting Equipment Specification Assistant

A tool that crawls lighting equipment manufacturers' websites, extracts product specifications from PDFs, and provides an intelligent query interface using RAG (Retrieval-Augmented Generation).

## Features

- Web crawling of major lighting equipment manufacturers
- PDF specification document extraction
- Vector-based document retrieval
- Natural language query interface using LLaMA2
- Local document storage and embedding

## Supported Manufacturers

- American DJ (ADJ)
- Chauvet Professional
- Elation Lighting
- Martin Professional
- ENTTEC
- ETC (Electronic Theatre Controls)

## Prerequisites

- Python 3.10 or higher
- macOS 12.3 or higher (for MPS support)
- Ollama with LLaMA2 model installed

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/dmx-rag.git
cd dmx-rag
```

2. Create and activate a Conda environment:
```bash
conda create -n spec-rag-env python=3.10
conda activate spec-rag-env
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Install Ollama and download the LLaMA2 model:
```bash
brew install ollama
ollama pull llama2
```

## Usage

1. Crawl specification documents:
```bash
python main.py --crawl
```

2. Process PDFs and start the query interface:
```bash
python main.py --process
```

3. Interactive query mode:
```bash
python main.py
```

## Project Structure

```
dmx-rag/
├── crawler/
│   ├── spiders.py      # Scrapy spider for PDF collection
│   └── pipelines.py    # Custom file handling pipeline
├── processors/
│   └── pdf_extractor.py # PDF text extraction
├── rag/
│   └── query_engine.py  # RAG implementation
├── main.py             # Main application entry
└── requirements.txt    # Project dependencies
```

## Configuration

- `CRAWL`: Set to `True` to enable web crawling
- `PROCESS_PDFS`: Set to `True` to process PDFs and index documents
- `DOWNLOAD_DIR`: Directory for storing downloaded PDFs (default: 'downloads')
- 