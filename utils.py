# import required libraries

from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chains.question_answering import load_qa_chain
from langchain.vectorstores import FAISS
from langchain.llms import HuggingFaceHub
from PyPDF2 import PdfReader
from docx import Document


def process_text(text):
    #  Processing the given text by splitting it into chunks and converting these chunks into embedding to form knowledge base  

    #inatilize a text splitter to divide the text into manageable chunks
    text_splitter = CharacterTextSplitter(
        separator = '\n',
        chunk_size = 1000,
        chunk_overlap=200,
        length_function = len
    )

    chunks = text_splitter.split_text(text)  # split the text into chunks

    #loading a model for generating embedding from Hugging Face
    embeddings = HuggingFaceEmbeddings(model_name = 'sentence-transformers/all-MiniLM-L6-v2')

    #create a FAISS index from the text chunks using the embedding
    knowledge_base = FAISS.from_texts(chunks, embeddings)

    return knowledge_base



def extract_text_from_pdf(pdf):
    pdf_reader = PdfReader(pdf)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() or ""
    return text



def extract_text_from_docx(docx):
    doc = Document(docx)
    text = ""
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text



def doc_Summarizer(file_content, file_type):

    if file_content is not None:
        if file_type == 'pdf':
            text = extract_text_from_pdf(file_content)
        elif file_type == 'docx':
            text = extract_text_from_docx(file_content)
        else:
            raise ValueError("Unsupported file type. Please use 'pdf' or 'docx'.")
    

        #Creating a knowledgebase using the extracted text
        knowledge_base = process_text(text)

        #Define a query for summarization
        query = "Summarize the content of the uploaded PDF file covering all the important information"

        if query:

            # perform a similarity search in the knowledgebase using the query
            docs = knowledge_base.similarity_search(query)

            #Specify the model used to generate the summary 
            llm = HuggingFaceHub(model_name='facebook/opt-2.7b', temperature = 0.2)

            # load a question answering chain with the specified model
            chain = load_qa_chain(llm, chain_type = 'stuff') #stuff provide a straight forward answer
            
            
            # run the chain to get a response 
            response = chain.run(input_documents = docs, question= query)
        
            return response # return the generated summary 




     