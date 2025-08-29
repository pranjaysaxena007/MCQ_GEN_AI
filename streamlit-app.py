import os
import json
import traceback
import streamlit as st
import pandas as pd
from src.mcqgenerator.utils import read_file,get_table_data
from src.mcqgenerator.MCQGenerator import genereate_evaluate_chain
from src.mcqgenerator.looger import logging
from langchain_google_genai.callbacks import invoke_with_cost_logging
from dotenv import load_dotenv
load_dotenv()

with open('Response.json','r') as file:
    RESPONSE_JSON = json.loads(file)

st.title("MCQ generator using LangChain")

with st.form("user_inputs"):
    uploaded_file = st.file_uploader("Upload a PDF or TEXT file")
    mcq_count = st.number_input("No. of MCQ",min_value=3,max_value=50)
    subject = st.text_input("Enter subject",max_chars=20)
    tone = st.text_input("Complexity level of Questions",max_chars=20,placeholder="Simple")
    button = st.form_submit_button("Create MCQ")


if button and uploaded_file is not None and mcq_count and subject and tone:
    with st.spinner("Loading...."):
        try:
            text = read_file(uploaded_file)
            with invoke_with_cost_logging() as cb:
                response = genereate_evaluate_chain.invoke(
                    {
                        "text": text,
                        "number":mcq_count,
                        "subject": subject,
                        "tone":tone,
                        "response_json": RESPONSE_JSON
                    }
                )
        except Exception as e:
            traceback.print_exception(type(e),e,e.__traceback__)
            st.error("Error")

        else:
            print(f"Total Tokens Used: {cb.total_tokens}")
            print(f"Prompt Tokens: {cb.prompt_tokens}")
            print(f"Completion Tokens: {cb.completion_tokens}")
            print(f"Total Cost (USD): ${cb.total_cost:.4f}")
            if isinstance(response,dict):
                quiz = response.get("quiz",None)    
                if quiz is not None:
                    table_data = get_table_data(quiz)
                    if table_data is not None:
                        df = pd.DataFrame(table_data)
                        df.index += 1
                        st.table(df)
                        st.text_area(label="Review",value=response["review"])
                    else:
                        st.error("Error in the table data")
            else:
                st.write(response)
                