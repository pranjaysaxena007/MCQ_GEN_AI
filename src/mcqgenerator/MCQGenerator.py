import pandas as pd
import os
import json
import traceback
from dotenv import load_dotenv
load_dotenv()

from src.mcqgenerator.utils import read_file,get_table_data
from src.mcqgenerator.looger import logging

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage,HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

llm = ChatGoogleGenerativeAI(
    model = "gemini-2.5-flash",
    google_api_key = os.getenv("GOOGLE-API-KEY"),
    temperature = 0.7,
)

quiz_generation_prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessage(
            content = "You are an expert MCQ quiz maker. You have to create the quiz based on user input and given instructions."
        ),
        HumanMessage(
            content = """
                Please create {number} muliple choice questions in a {tone} tone based on the following text.
                **Text:**
                {text}
                
                **Instructions:**
                1. Ensure that all questions are from given text only.
                2. Ensure that the questions are not repeated.
                3. Format your entire response as a JSON object that strictly follows below given scheme.
                {response_json}
            """
        )
    ]    
)

quiz_chain = quiz_generation_prompt | llm | StrOutputParser()

review_prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessage(
            content ="You are an expert English grammarian and writer. You have to evaluate the given quiz as per instructions given below"
        ),
        HumanMessage(
            content="""Please review the multiple choice quiz intendede for {subject} sy=tudents.
                **Quiz for review:**
                '''json
                {quiz}
                '''

                **Your Task:**
                1. Evaluate the compleity of the questions.
                2. Assess if the quiz is appropriate for students cognitive and quantitatib=ve ability.
                3. If the quiz is not suitable, then rewrite the questions and adjust the tone to perfectly fit students abilities.
                4. Provide a brief analysis of your changes or your approval of the original quiz.
                
            """
        )
    ]
)

review_chain = review_prompt | llm | StrOutputParser()

genereate_evaluate_chain =(
    RunnablePassthrough.assign(quiz = quiz_chain) | 
    RunnablePassthrough.assign(review = review_chain)
)

