import os
import json
import fitz  
from datetime import datetime
from collections import defaultdict
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer

INPUT_ROOT = "input"
OUTPUT_FOLDER = "output"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def extract_text_from_pdf(pdf_path):
    text_by_page = []
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text_by_page.append(page.get_text())
    return text_by_page

def summarize_text(text, sentence_count=6):
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, sentence_count)
    return " ".join(str(sentence) for sentence in summary)

def paraphrase(summary):
    lines = summary.split(". ")
    refined = [f"In essence, {line.strip().capitalize()}." for line in lines if len(line.strip()) > 30]
    return " ".join(refined[:7])

def infer_persona(text):
    text = text.lower()
    if "buffet" in text and "vegetarian" in text:
        return "Food Contractor", "Prepare a vegetarian buffet-style dinner menu for a corporate gathering."
    elif "travel" in text or "itinerary" in text:
        return "Travel Enthusiast", "Design a compact itinerary for a traveler."
    elif "architecture" in text or "monument" in text:
        return "Heritage Explorer", "Summarize heritage sites for a cultural visit."
    elif "developer" in text or "cloud" in text:
        return "Tech Learner", "Summarize development practices for a new tech learner."
    else:
        return "General Reader", "Summarize key insights from the documents."

def process_collection(collection_path, collection_name):
    files = [f for f in os.listdir(collection_path) if f.endswith(".pdf")]
    extracted_sections = []
    subsection_analysis = []
    all_text = ""
    persona, job = "", ""

    for file in files:
        pdf_path = os.path.join(collection_path, file)
        pages = extract_text_from_pdf(pdf_path)
        full_text = "\n".join(pages)

        if not persona:
            persona, job = infer_persona(full_text[:1000])  

        summary = summarize_text(full_text, 6)
        refined = paraphrase(summary)

        extracted_sections.append({
            "document": file,
            "section_title": pages[0].split("\n")[0] if pages else "Untitled",
            "importance_rank": 5,  
            "page_number": 1
        })

        subsection_analysis.append({
            "document": file,
            "refined_text": refined,
            "page_number": 1
        })

    metadata = {
        "input_documents": files,
        "persona": persona,
        "job_to_be_done": job,
        "processing_timestamp": datetime.now().isoformat()
    }

    output = {
        "metadata": metadata,
        "extracted_sections": extracted_sections,
        "subsection_analysis": subsection_analysis
    }

    output_path = os.path.join(OUTPUT_FOLDER, f"{collection_name}_summary.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=4)
    print(f"✅ Processed {collection_name}, output written to {output_path}")

def main():
    for collection in os.listdir(INPUT_ROOT):
        collection_path = os.path.join(INPUT_ROOT, collection)
        if os.path.isdir(collection_path):
            process_collection(collection_path, collection)

if __name__ == "__main__":
    main()
