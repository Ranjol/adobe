import os
import json
import logging
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextBoxHorizontal, LTTextLineHorizontal
from collections import defaultdict

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def is_potential_heading(text, font_size, avg_font_size):
    text = text.strip()
    if not text or len(text.split()) > 10:
        return False
    return (text[0].isdigit() and "." in text[:5]) or font_size > avg_font_size

def get_font_size(element):
    sizes = []
    try:
        for line in element:
            if isinstance(line, LTTextLineHorizontal):
                for char in line:
                    if hasattr(char, 'size'):
                        sizes.append(char.size)
        if sizes:
            return sum(sizes) / len(sizes)
    except (AttributeError, TypeError):
        pass
    return 0

def process_pdf(pdf_path, output_path):
    logging.info(f"Processing PDF: {pdf_path}")
    outline = []
    title = None
    font_sizes = []
    
    try:
        for page_layout in extract_pages(pdf_path):
            page_num = page_layout.pageid
            page_text = []
            
            for element in page_layout:
                if isinstance(element, LTTextBoxHorizontal):
                    text = element.get_text().strip()
                    font_size = get_font_size(element)
                    if font_size > 0:
                        page_text.append((text, font_size))
                        font_sizes.append(font_size)
            
            if page_num == 1 and not title and page_text:
                title = page_text[0][0] if page_text[0][0].strip() else "Untitled"
        
        if font_sizes:
            avg_font_size = sum(font_sizes) / len(font_sizes)
            font_sizes.sort(reverse=True)
            size_thresholds = list(dict.fromkeys(font_sizes))[:3]
            
            for page_layout in extract_pages(pdf_path):
                page_num = page_layout.pageid
                for element in page_layout:
                    if isinstance(element, LTTextBoxHorizontal):
                        text = element.get_text().strip()
                        font_size = get_font_size(element)
                        if is_potential_heading(text, font_size, avg_font_size):
                            if len(size_thresholds) >= 1 and font_size >= size_thresholds[0]:
                                level = "H1"
                            elif len(size_thresholds) >= 2 and font_size >= size_thresholds[1]:
                                level = "H2"
                            elif len(size_thresholds) >= 3 and font_size >= size_thresholds[2]:
                                level = "H3"
                            else:
                                continue
                            outline.append({"level": level, "text": text, "page": page_num})
        
        result = {
            "title": title or "Untitled",
            "outline": outline
        }
        
        output_dir = os.path.dirname(output_path)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        logging.info(f"Saved output to {output_path}")
        
    except Exception as e:
        logging.error(f"Error processing {pdf_path}: {str(e)}")
        raise

if __name__ == "__main__":
    input_dir = "./input"
    output_dir = "./output"
    os.makedirs(input_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)
    
    for filename in os.listdir(input_dir):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(input_dir, filename)
            json_path = os.path.join(output_dir, filename.replace(".pdf", ".json"))
            try:
                process_pdf(pdf_path, json_path)
                print(f"Processed {filename} -> {json_path}")
            except Exception as e:
                print(f"Error processing {filename}: {str(e)}")
                
