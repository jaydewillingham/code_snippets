#---------------------------------------------------------------------------------------
#This is a python script that extracts all the comments from an pdf file. 
#I use this to extract Collaborator comments on Documents but can be used for whatever!
#---------------------------------------------------------------------------------------



import fitz  # PyMuPDF
import os
import csv

# Path to pdf folder
folder_path = os.path.expanduser("~/Downloads/PaperComments")

# Output folder for extracted CSVs
output_path = os.path.join(folder_path, "ExtractedComments")
os.makedirs(output_path, exist_ok=True)

# Loop through all PDFs in the folder
for filename in os.listdir(folder_path):
    if filename.lower().endswith(".pdf"):
        pdf_path = os.path.join(folder_path, filename)
        doc = fitz.open(pdf_path)

        comments = []
        for page_num in range(len(doc)):
            page = doc[page_num]
            for annot in page.annots() or []:
                info = annot.info
                comments.append([
                    page_num + 1,                              # Page number
                    info.get("title", "Unknown"),             # Author
                    info.get("content", "").strip(),          # Comment text
                    annot.type[1]                             # Annotation type (e.g. Highlight, Text)
                ])

        # Save comments to CSV
        csv_filename = os.path.splitext(filename)[0] + "_comments.csv"
        csv_path = os.path.join(output_path, csv_filename)

        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Page", "Author", "Comment", "Type"])
            writer.writerows(comments)

        print(f"Extracted {len(comments)} comments from {filename} → {csv_filename}")
