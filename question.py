import anthropic
import streamlit as st
from streamlit.logger import get_logger
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.llms import OpenAI
from langchain.chat_models import ChatAnthropic
from langchain.vectorstores import SupabaseVectorStore
from stats import add_usage
from retrievalApp import search_and_llm


memory = ConversationBufferMemory(
    memory_key="chat_history", return_messages=True)
openai_api_key = st.secrets.openai_api_key
anthropic_api_key = st.secrets.anthropic_api_key
logger = get_logger(__name__)


def count_tokens(question, model):
    count = f'Words: {len(question.split())}'
    if model.startswith("claude"):
        count += f' | Tokens: {anthropic.count_tokens(question)}'
    return count


def chat_with_doc(model, vector_store: SupabaseVectorStore, stats_db):
    
    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []
        
    
    
    question = st.text_area("## Ask a question",value = "What is Ceramic")
    columns = st.columns(3)
    with columns[0]:
        button = st.button("Ask", type = "primary")
    with columns[1]:
        count_button = st.button("Count Tokens", type='secondary')
    with columns[2]:
        clear_history = st.button("Clear History", type='secondary')
    
    
    
    if clear_history:
        st.session_state['chat_history'] = []
        st.experimental_rerun()

    if button:
        qa = None
        if len(question) == 0 or question == None or question.isspace():
            st.empty()
            st.markdown(f"**Quivr:** Please ask a question")
            return

        if not st.session_state["overused"]:
            add_usage(stats_db, "chat", "prompt" + question, {"model": model, "temperature": st.session_state['temperature']})
            if model.startswith("gpt"):
                logger.info('Using OpenAI model %s', model)
                qa = ConversationalRetrievalChain.from_llm(
                    OpenAI(
                        model_name='gpt-3.5-turbo', openai_api_key=openai_api_key, temperature=st.session_state['temperature'], max_tokens=st.session_state['max_tokens']), vector_store.as_retriever(), memory=memory, verbose=True)
            if model.startswith("davinci"):
                logger.info('Using OpenAI model %s', model)
                qa = ConversationalRetrievalChain.from_llm(
                    OpenAI(
                        model_name='text-davinci-003', openai_api_key=openai_api_key, temperature=st.session_state['temperature'], max_tokens=st.session_state['max_tokens']), vector_store.as_retriever(), memory=memory, verbose=True)
            elif anthropic_api_key and model.startswith("claude"):
                logger.info('Using Anthropics model %s', model)
                qa = ConversationalRetrievalChain.from_llm(
                    ChatAnthropic(
                        model=st.session_state['model'], anthropic_api_key=anthropic_api_key, temperature=st.session_state['temperature'], max_tokens_to_sample=st.session_state['max_tokens']), vector_store.as_retriever(), memory=memory, verbose=True, max_tokens_limit=102400)
            
            
            st.session_state['chat_history'].append(("You", question))

            # if is_contain_chinese(question):
            #     question = question+",Please answer in Chinese"
            # Generate model's response and add it to chat history
            with st.spinner('Waiting for OpenAI and vector store to process ...'):
                # model_response = qa({"question": question})
                model_response = search_and_llm(question)

            logger.info('Result: %s', model_response)

            st.session_state['chat_history'].append(("LLM", model_response["answer"]))

            # Display chat history
            st.empty()
            for speaker, text in st.session_state['chat_history']:
                st.markdown(f"**{speaker}:** {text}")
                
            st.balloons()
        else:
            st.error("You have used all your free credits. Please try again later or self host.")
        
    if count_button:
        st.write(count_tokens(question, model))



def chat_with_doc_zh(model, vector_store: SupabaseVectorStore, stats_db):
    
    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []
        
    
    
    question = st.text_area("## Ask a question",value = "What is the ZK-rollups")
    columns = st.columns(3)
    with columns[0]:
        button = st.button("Ask", type = "primary")
    with columns[1]:
        count_button = st.button("Count Tokens", type='secondary')
    with columns[2]:
        clear_history = st.button("Clear History", type='secondary')
    
    
    
    if clear_history:
        st.session_state['chat_history'] = []
        st.experimental_rerun()

    if button:
        qa = None
        if not st.session_state["overused"]:
            add_usage(stats_db, "chat", "prompt" + question, {"model": model, "temperature": st.session_state['temperature']})
            if model.startswith("gpt"):
                logger.info('Using OpenAI model %s', model)
                qa = ConversationalRetrievalChain.from_llm(
                    OpenAI(
                        model_name='gpt-3.5-turbo', openai_api_key=openai_api_key, temperature=0.8, max_tokens=512), vector_store.as_retriever(), memory=memory, verbose=True)
            elif anthropic_api_key and model.startswith("claude"):
                logger.info('Using Anthropics model %s', model)
                qa = ConversationalRetrievalChain.from_llm(
                    ChatAnthropic(
                        model=st.session_state['model'], anthropic_api_key=anthropic_api_key, temperature=st.session_state['temperature'], max_tokens_to_sample=st.session_state['max_tokens']), vector_store.as_retriever(), memory=memory, verbose=True, max_tokens_limit=102400)
            
            
            st.session_state['chat_history'].append(("You", question))
            question=question+",请使用中文回答"

            # Generate model's response and add it to chat history
            with st.spinner('Waiting for OpenAI and vector store to process ...'):
                model_response = qa({"question": question})
            logger.info('Result: %s', model_response)

            st.session_state['chat_history'].append(("Quivr", model_response["answer"]))

            # Display chat history
            st.empty()
            for speaker, text in st.session_state['chat_history']:
                st.markdown(f"**{speaker}:** {text}")
                
            st.balloons()
        else:
            st.error("You have used all your free credits. Please try again later or self host.")
        
    if count_button:
        st.write(count_tokens(question, model))


def is_contain_chinese(check_str):
    for ch in check_str:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
    return False