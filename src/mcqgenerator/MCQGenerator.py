import pandas as pd
import os
import json
import traceback
from dotenv import load_dotenv()
load_dotenv()

from mcqgenerator.utils import read_files,get_table_data
from mcqgenerator.looger import logging

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.runnables import RunnableLambda,RunnableSequence,RunnablePassthrough,RunnableParallel

