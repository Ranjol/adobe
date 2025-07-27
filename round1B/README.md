 Adobe India Hackathon 2025 – Challenge 1B  
 Persona-Driven Document Intelligence 

 Persona Inference + PDF Summarization + Ranking

This project automatically identifies the underlying persona from a collection of PDFs and generates a ranked summary of the documents based on their relevance to the inferred persona.


 How It Works

1. **Input PDFs** (in `input/` folder) are parsed and analyzed.
2. The system:
   - **Infers the persona** (e.g., Travel Planner, Food Explorer).
   - **Summarizes each PDF** in 2–3 lines.
   - **Ranks PDFs** based on relevance to the inferred persona.
3. A final **`persona_summary.json`** file is generated with all results.



 How to Run

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
  Add Your PDFs

2. Place all input PDFs inside the input/ folder.

Ensure each PDF is 10–15 pages with readable text (non-image-based recommended).

3. Run the Code

bash
Copy
Edit
python main.py
4. Output

A summary file will be created at output/persona_summary.json.

