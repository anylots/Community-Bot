from langchain.chains import LLMChain
from langchain import OpenAI
from langchain import PromptTemplate
from langchain.chains import ConversationalRetrievalChain
from langchain.vectorstores import SupabaseVectorStore
import streamlit as st
from langchain.memory import ConversationBufferMemory
import time

openai_api_key = st.secrets.openai_api_key
memory = ConversationBufferMemory(
    memory_key="chat_history", return_messages=True)


sectionsTitle = ["Introduction", "Background"]
sections = ["""- Introduce the concept of Ethereum layer2 and its importance.
- Briefly introduce optimal rollup technology and its advantages.""", 
"""- Explain the current state of Ethereum and its limitations (such as high gas fees and slow transaction throughput).
- Introduce layer2 solutions and their benefits.
- Explain how optimal rollup technology fits into the layer2 landscape."""]

def generate_Article_Steps(vector_store: SupabaseVectorStore, stats_db):
    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []
        
    st.text_area("## Please enter a project description")
    button = st.button("Generate")

    if button:
        prompt = """
        Please read the following whitepaper outline for the Ethereum Layer2 project 
        and write specific content for Part {section}, 
        which must be technically professional. The whitepaper outline:
        ```{brief}```
        CONTENT:
        """
        # generate_prompt = generate_prompt.replace("ACTION", brief)
        # prompt_template = PromptTemplate(
        #     template=prompt, input_variables=["section", "brief"])
        
        # generate_llm = OpenAI(
        #     temperature=0.5, openai_api_key="openai_api_key")
        
        # chain = LLMChain(llm=generate_llm, prompt=prompt_template)

        chain = ConversationalRetrievalChain.from_llm(
                        OpenAI(
                            model_name=st.session_state['model'], openai_api_key=openai_api_key, 
                            temperature=st.session_state['temperature'], max_tokens=st.session_state['max_tokens']), 
                            vector_store.as_retriever(), memory=memory, verbose=True)

        # response = 'Morphism: A Next-Generation Layer2 Platform'
        # response += "\n"
        # response += "\n"
        st.markdown("### <center>Optimism: A Next-Generation Layer2 Platform</center>")
        for i in range (0,len(sections)):
            # question = "Please"
            # response += section
            # response += "\n"
            st.session_state['chat_history'].append(("You", sections[i]))
            # print("question")
            # print(sections[i])
            # return

            model_response = chain({"question": sections[i]})
            # response += model_response["answer"]
            result = model_response["answer"]
            # st.session_state['chat_history'].append((section, model_response["answer"]))
            st.markdown(f"###<center> {sectionsTitle[i]}")
            st.markdown(f"{result}")
            # result = chain.run({"section": section, "brief": brief})
            # print(result)
            # response += "\n"



def generate_Article_full(vector_store: SupabaseVectorStore, stats_db):
    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []
        
    # value = "Please write a white paper about Ethereum layer2, with the technical key being the first Optimistic ZK-Rollup Solution for Ethereum, where the challenger uses zk rollup as proof of fraud"
    # value ="What is the outline of the white paper on Ethereum Layer 2 using optimistic zk-rollup technology?"
    value = "I want to write a white paper on the Ethereum layer2 network, which is based on optimistic zk-rollup technology. Please help me write an outline first"
    question = st.text_area("Please enter a project description", value = value)
    
    button = st.button("Generate")

    if button:
        prompt = """
        Please read the following whitepaper outline for the Ethereum Layer2 project 
        and write specific content for Part {section}, 
        which must be technically professional. The whitepaper outline:
        ```{brief}```
        CONTENT:
        """

        chain = ConversationalRetrievalChain.from_llm(
                        OpenAI(
                            model_name="gpt-3.5-turbo", openai_api_key=openai_api_key, 
                            temperature=1, max_tokens=1800), 
                            vector_store.as_retriever(), memory=memory, verbose=True)
        
        st.markdown(f"### <center> Optimism: A Next-Generation Layer2 Platform", unsafe_allow_html=True)
        st.session_state['chat_history'].append(("You", question))
        with st.spinner('Wait for OpenAI and vector store to process ...'):
            model_response = chain({"question": question})
            # model_response ={"answer":"development in progress"}
        result = model_response["answer"]
        # st.markdown(f"### <center>{sectionsTitle[i]}")
        # st.markdown(f"### Introduction")
        # st.markdown(f"Explain how optimal rollup technology fits into the layer2 landscape <Generated by fakeLLM>")
        # st.markdown(f"### Background")
        st.markdown(f"{result}")
        # progress_text = "Operation in progress. Please wait."
        # my_bar = st.progress(0, text=progress_text)
        # for percent_complete in range(100):
        #     time.sleep(0.1)
        #     my_bar.progress(percent_complete + 1, text=progress_text)
        st.balloons()

        # st.snow()


