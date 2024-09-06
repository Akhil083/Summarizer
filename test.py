import streamlit as st
import os
from utils import *
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('HUGGINGFACE_API_KEY')
# Setting the  HuggingFace API Key as an enviornment Variable 
os.environ['HUGGINGFACEHUB_API_TOKEN'] = api_key


def main():
    #Setting the page configuration
    st.set_page_config(page_title = "Document Summarizer")

    #Page Layout
    st.title("Document Summarizer ")
    st.write("Summarize your file in just few seconds")
    st.divider()


    st.info("Please upload a document before clicking 'Generate Summary'.")


    #creating a file uploder
    uploaded_file = st.file_uploader("Upload your Document", type = ["pdf","docx"])


    #Creating a button to submit the document for summarization
    submit = st.button("Generate Summary")


   
    if submit and uploaded_file is not None:

        file_type = uploaded_file.type.split('.')[1]
        file_type = file_type.lower()
        print(file_type)
        file_content = uploaded_file.read()
        response = doc_Summarizer(file_content, uploaded_file)

        #Displaying the summary
        st.subheader('Summay of the file')
        st.write(response)
        
        



#Python script for execution

if __name__ == '__main__':
    main( )


