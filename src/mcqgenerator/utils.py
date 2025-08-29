import os
import PyPDF2
import json
import traceback

def read_file(file):
    if file.name.endswith(".pdf"):
        try:
            pdf_reader = PyPDF2.PdfFileReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            return text
        
        except Exception as e:
            raise Exception("Error reading PDF File.")
        
    elif file.name.endswith(".txt"):
        return file.read().decode("utf-8")
    
    else:
        raise Exception(
            "Unsupported File Format! Only PDF and TEXT files supported."
        )
        
def get_table_data(quiz_str):
    try:
        # Clean the string from markdown formatting
        cleaned_str = quiz_str.strip().lstrip("```json").rstrip("```").strip()
        
        # This variable will be a list of dictionaries
        quiz_list = json.loads(cleaned_str) 
        quiz_table_data = []

        # Iterate directly over the list
        for item in quiz_list:
            mcq = item.get("question")
            options = " || ".join(item.get("options", []))
            answer = item.get("answer")
            
            quiz_table_data.append({"MCQ": mcq, "Choices": options, "Answer": answer})

        return quiz_table_data

    except Exception as e:
        traceback.print_exc()
        return False