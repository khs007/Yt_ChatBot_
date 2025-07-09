from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_community.llms import Ollama
from langchain.docstore.document import Document
from langchain_core.runnables import RunnableParallel,RunnablePassthrough,RunnableLambda
from langchain_core.output_parsers import StrOutputParser
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
from langchain.llms import HuggingFacePipeline
from langchain_groq import ChatGroq
from dotenv import load_dotenv
load_dotenv()

def build_vector_store(transcript_data):
    splitter = RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=200)
    chunks = splitter.create_documents([transcript_data])
    embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    return  FAISS.from_documents(chunks, embedding_model)

def get_answer(vector_store,question):
    retriever=vector_store.as_retriever(search_type="similarity",search_kwargs={"k":4})
    

    def document(retrieved_dox):
        context="\n\n".join(doc.page_content for doc in retrieved_dox)
        return context
    
    prompt = PromptTemplate(
    template="""
      You are a helpful assistant.
      Answer ONLY from the provided transcript context.
      If the context is insufficient, just say you don't know.

      {context}
      Question: {question}
      Give a detailed and specific answer
    """,
    input_variables = ['context', 'question']
)
    
    parallel=RunnableParallel(
    context=retriever|RunnableLambda(document),
    question=RunnablePassthrough()
    )
    
    llm = ChatGroq(
    model_name="llama3-8b-8192"  
    )
    parser=StrOutputParser()
    main_chain=parallel|prompt|llm|parser
    return main_chain.invoke(question)
