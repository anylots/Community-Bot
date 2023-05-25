# main.py
import os
import tempfile

import streamlit as st
from files import file_uploader, url_uploader
from question import chat_with_doc
from brain import brain
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import SupabaseVectorStore
from supabase import Client, create_client
from explorer import view_document
from stats import get_usage_today
from generateArticle import generate_Article_full

supabase_url = st.secrets.supabase_url
supabase_key = st.secrets.supabase_service_key
openai_api_key = st.secrets.openai_api_key
anthropic_api_key = st.secrets.anthropic_api_key
supabase: Client = create_client(supabase_url, supabase_key)
self_hosted = st.secrets.self_hosted

embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
vector_store = SupabaseVectorStore(
    supabase, embeddings, table_name="documents")
models = ["gpt-3.5-turbo", "gpt-4"]
if anthropic_api_key:
    models += ["claude-v1", "claude-v1.3",
               "claude-instant-v1-100k", "claude-instant-v1.1-100k"]

# Set the theme
st.set_page_config(
    page_title="Langchain",
    layout="wide",
    initial_sidebar_state="expanded",
)


st.title("🤖 Layer2Langchain - GenerativeAI About Layer2 🤖")
st.markdown("Store your data in a vector store and generate info with OpenAI's GPT-3/4.")
if self_hosted == "false":
    st.markdown('**📢 Note: In the public demo, access to functionality is restricted. You can only use the GPT-3.5-turbo model and upload files up to 1Mb. To use more models and upload larger files, consider self-hosting Quivr.**')

# st.markdown("---\n\n")

st.session_state["overused"] = False
if self_hosted == "false":
    usage = get_usage_today(supabase)
    if usage > st.secrets.usage_limit:
        st.markdown(
            f"<span style='color:red'>You have used {usage} tokens today, which is more than your daily limit of {st.secrets.usage_limit} tokens. Please come back later or consider self-hosting.</span>", unsafe_allow_html=True)
        st.session_state["overused"] = True
    else:
        st.markdown(f"<span style='color:blue'>Usage today: {usage} tokens out of {st.secrets.usage_limit}</span>", unsafe_allow_html=True)
    st.write("---")
    



# Initialize session state variables
if 'model' not in st.session_state:
    st.session_state['model'] = "gpt-3.5-turbo"
if 'temperature' not in st.session_state:
    st.session_state['temperature'] = 0.0
if 'chunk_size' not in st.session_state:
    st.session_state['chunk_size'] = 500
if 'chunk_overlap' not in st.session_state:
    st.session_state['chunk_overlap'] = 0
if 'max_tokens' not in st.session_state:
    st.session_state['max_tokens'] = 256


###################### Sidebar Configuration ######################
# Generate
st.sidebar.title("Inference Configuration")
st.sidebar.markdown(
    "Choose your model and temperature for asking questions.")
if st.secrets.self_hosted != "false":
    st.session_state['model'] = st.sidebar.selectbox(
    "Select Model", models, index=(models).index(st.session_state['model']))
else:
    st.sidebar.write("**Model**: gpt-3.5-turbo")
    st.sidebar.write("**Self Host to unlock more models such as claude-v1 and GPT4**")
    st.session_state['model'] = "gpt-3.5-turbo"
st.session_state['temperature'] = st.sidebar.slider(
    "Select Temperature", 0.0, 1.0, st.session_state['temperature'], 0.1)
if st.secrets.self_hosted != "false":
    st.session_state['max_tokens'] = st.sidebar.slider(
        "Select Max Tokens", 256, 2048, st.session_state['max_tokens'], 2048)
else:
    st.session_state['max_tokens'] = 256

# Vector Store Manage
st.sidebar.title("Vector Configuration")
st.sidebar.markdown(
    "Choose your chunk size and overlap for adding knowledge.")
st.session_state['chunk_size'] = st.sidebar.slider(
    "Select Chunk Size", 100, 1000, st.session_state['chunk_size'], 50)
st.session_state['chunk_overlap'] = st.sidebar.slider(
    "Select Chunk Overlap", 0, 100, st.session_state['chunk_overlap'], 10)


###################### Sidebar Configuration ######################
tab1, tab2, tab3 = st.tabs(["Generate", "Vector Store Manage", "Dog"])
with tab1:
#    st.sidebar.empty()
   st.header("Generate")
#    st.image("https://static.streamlit.io/examples/cat.jpg", width=200)
   generate_choice = st.radio(
    "", ('GenerateArticle','Chat with AI about Layer2'))
   if generate_choice == 'Chat with AI about Layer2':

        chat_with_doc(st.session_state['model'], vector_store, stats_db=supabase)

   else:
        generate_Article_full(vector_store, stats_db=supabase)



with tab2:
   st.header("Vector Store Manage")
   store_choice = st.radio(
    "Choose an action", ('Add Knowledge', 'Forget', "Explore"))

#    st.image("https://static.streamlit.io/examples/dog.jpg", width=200)
   if store_choice == 'Add Knowledge':
        # Display chunk size and overlap selection only when adding knowledge
        
        # Create two columns for the file uploader and URL uploader
      col1, col2 = st.columns(2)
        
      with col1:
            file_uploader(supabase, openai_api_key, vector_store)
      with col2:
            url_uploader(supabase, openai_api_key, vector_store)

   elif store_choice == 'Forget':
        brain(supabase)

   elif store_choice == 'Explore':
        view_document(supabase)

with tab3:
   st.header("A dog")
   st.image("https://static.streamlit.io/examples/dog.jpg", width=200)



# Create a radio button for user to choose between adding knowledge or asking a question



st.markdown("---\n\n")
