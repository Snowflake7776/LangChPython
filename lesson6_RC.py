# Retrieval Chain : load the document from website and split the document.
# load to wordembedding model and vertorstores.

from dotenv import load_dotenv
load_dotenv()

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores.faiss import FAISS



def  get_document_from_web(url):
    loader = WebBaseLoader(url)
    docs = loader.load()
    
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=200,
        chunk_overlap=20,
    )
    splitDocs = splitter.split_documents(docs)
    # print(len(splitDocs))

    return splitDocs

def create_db(docs):
    embedding = OpenAIEmbeddings()
    vectorStore = FAISS.from_documents(docs, embedding = embedding) 
    return vectorStore

docs = get_document_from_web("https://python.langchain.com/v0.1/docs/expression_language/")
vectorStore = create_db(docs)


# Initialize the ChatGroq object
llm = ChatGroq(
    #model="llama-3.2-3b-preview",
    model ="llama3-groq-8b-8192-tool-use-preview",
    temperature=0,
)

prompt = ChatPromptTemplate.from_template(""" 
    Answer the user's question:
    Context :  {context}
    User Question : {input}
""")

# chain = prompt | llm

chain = create_stuff_documents_chain(
    llm =llm,
    prompt = prompt
    )

response = chain.invoke({
    'input':"What is LCEL",
    'context': docs
})
print(response)