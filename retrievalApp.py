from langchain.chains import RetrievalQA
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.llms import OpenAI
import streamlit as st
from langchain.vectorstores import SupabaseVectorStore
from supabase import Client, create_client
from langchain.prompts import PromptTemplate

supabase_url = st.secrets.supabase_url
supabase_key = st.secrets.supabase_service_key
openai_api_key = st.secrets.openai_api_key
anthropic_api_key = st.secrets.anthropic_api_key
supabase: Client = create_client(supabase_url, supabase_key)
self_hosted = st.secrets.self_hosted

embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
vector_store = SupabaseVectorStore(
    supabase, embeddings, table_name="documents")



prompt_template = """Use the following pieces of context to answer the question at the end. Don't try to make up an answer,Under the premise of ensuring accuracy, 
the answers should be as rich as possible.

{context}

Question: {question}
Answer in Chinese(include necessary English terminology):"""
PROMPT = PromptTemplate(
    template=prompt_template, input_variables=["context", "question"]
)


chain_type_kwargs = {"prompt": PROMPT} 
qa = RetrievalQA.from_chain_type(llm=OpenAI(model_name='gpt-3.5-turbo', temperature=0.4, max_tokens=1024, openai_api_key=openai_api_key), chain_type="stuff", retriever=vector_store.as_retriever(),chain_type_kwargs=chain_type_kwargs)
# qa = RetrievalQA.from_llm(llm=OpenAI(model_name='gpt-3.5-turbo', temperature=0.4, max_tokens=1024, openai_api_key=""), retriever=vector_store.as_retriever(),prompt=PROMPT)

# query = "什么是desoc"
# res = qa.run(query)
# print(res)

def search_and_llm(query):
    res = qa.run(query)
    return {"answer": res}