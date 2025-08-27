from setuptools import find_packages,setup

setup(
    name="mcqgenerator",
    version="0.0.1",
    author="Pranjay",
    author_email="psaxena2411@gmail.com",
    install_requirements=["google-generativeai","langchain","streamlit","python-dotenv","PyPDF2"],
    packages=find_packages()
)