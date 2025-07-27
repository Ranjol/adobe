Adobe India Hackathon 2025 - Round 1A
Setup

Install dependencies: pip install -r requirements.txt
Place PDFs in input/ directory.
Run: python process_pdf.py
Outputs saved to output/ directory.

Files

process_pdf.py: Main script for extracting title and headings.
Dockerfile: Container setup for offline execution.
requirements.txt: Dependencies (pdfminer.six).
approach_explanation.md: Methodology explanation.

Docker
docker build -t pdf-extractor-1a .
docker run -v /path/to/input:/app/input -v /path/to/output:/app/output pdf-extractor-1a
