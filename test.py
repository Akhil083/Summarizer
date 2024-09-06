import streamlit as st
import os



def main():
    #Setting the page configuration
    st.set_page_config(page_title = "Document Summarizer")

    #Page Layout
    st.title("Document Summarizer ")
    st.write("Summarize your file in just few seconds")
    st.divider()


    #creating a file uploder
    uploded_file = st.file_uploader("Upload your Document", type = ["pdf","docx"])


    #Creating a button to submit the document for summarization
    submit = st.button("Generate Summary")


#Python script for execution

if __name__ == '__main__':
    main( )


