from langchain.chains import LLMChain
from langchain import OpenAI
from langchain import PromptTemplate
from langchain.chains import ConversationalRetrievalChain
from langchain.vectorstores import SupabaseVectorStore
import streamlit as st
from langchain.memory import ConversationBufferMemory
import time
from sectionsLoader import getSections,sectionTxtTest

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

    if 'result' not in st.session_state:
        st.session_state['result'] = ""

    if "detailMsg" not in st.session_state:
        st.session_state["detailMsg"] = []
        
    if "showDetail" not in st.session_state:
        st.session_state["showDetail"] = False

    if "sections" not in st.session_state:
        st.session_state["sections"] = []
    

    detailNew = False
    # value = "Please write a white paper about Ethereum layer2, with the technical key being the first Optimistic ZK-Rollup Solution for Ethereum, where the challenger uses zk rollup as proof of fraud"
    # value ="What is the outline of the white paper on Ethereum Layer 2 using optimistic zk-rollup technology?"
    value = "I want to write a white paper on the Ethereum layer2 network, which is based on optimistic zk-rollup technology. Please help me write an outline first"
    question = st.text_area("Please enter the project description you want", value = value)
    
    button = st.button("Generate",type = "primary")

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
        
        # st.markdown(f"### <center> ZkOptimism: A Next-Generation Layer2 Platform", unsafe_allow_html=True)
        st.session_state['chat_history'].append(("You", question))

        progress_text = "Operation in progress. Please wait."
        my_bar = st.progress(0, text=progress_text)

        for percent_complete in range(3):
            my_bar.progress(20*(percent_complete+1), text=progress_text)
            time.sleep(0.4)
            
        with st.spinner('Waiting for OpenAI and vector store to process ...'):
            # model_response = chain({"question": question})
            # model_response ={"answer":"This feature is in active development"}
            time.sleep(1)
            my_bar.progress(80, text=progress_text)
            my_bar.progress(100, text="generate complete")
            model_response = {"answer":"This feature is in active development"}
            sections = getSections("sectionTxt")
            st.session_state["sections"] = sections

        result = model_response["answer"]
        st.session_state['result'] =result
        st.balloons()
        st.session_state["showDetail"]= True
        # st.snow()

# Print the session state to make it easier to see what's happening
    if st.session_state["showDetail"]:
        st.markdown(f"### <center> ZkOptimism: A Next-Generation Layer2 Platform", unsafe_allow_html=True)

    # st.markdown(st.session_state["result"])
    sections = st.session_state["sections"]
    for info in sections:
        st.markdown(info)
    st.markdown("---\n\n")
    if st.session_state["showDetail"]:
       if st.button("GenerateDetail", type = "primary"):
            st.session_state["detailMsg"] = []
            chain = ConversationalRetrievalChain.from_llm(
                OpenAI(
                    model_name="gpt-3.5-turbo", openai_api_key=openai_api_key, 
                    temperature=1, max_tokens=1800), 
                    vector_store.as_retriever(), memory=memory, verbose=True)

            sectionTxt = st.session_state["result"]
            sections = getSections(sectionTxt)
            for section in sections:
                title = str(section).split("\n")[1]
                with st.spinner('Waiting for OpenAI and vector store to process ...'):
                    promot = ",Please reply as detailed as possible"
                    detail = chain({"question": str(section).strip()+promot})
                    # detail ={"answer":"This feature is in active development"}
                    detailNew = True
                    st.session_state["detailMsg"].append((title,detail["answer"]))
                    st.markdown("#### "+title)
                    st.markdown(detail["answer"])
                    st.button("ReGenerate",key = title,disabled = True)
                    st.markdown("\n\n\n")
                # st.snow()


    if detailNew == False:
        for title, content in st.session_state["detailMsg"]:
            st.markdown("#### " + title)
            st.markdown(content)
            st.button("ReGenerate",key = title,disabled =True)
            st.markdown("\n\n\n")


