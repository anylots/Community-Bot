import streamlit as st
import time


def deploy_contract():
    st.markdown("#### "+ "Write Contract")
    st.text_area("Describe the contract:",value ="Please help me write an erc20 contract, and token transfers require a 0.4% tax")
    st.button("Write By GPT & Compile", type = "primary")

    st.markdown("---\n")
    contract_call = st.button("Generate Call function By GPT With ABI", type="primary")

    if contract_call:
        with st.spinner('Waiting for OpenAI generate the scripts of contract call ...'):
            time.sleep(1.5)
            columns = st.columns(3)
            with columns[0]:
                st.button("Approve", type = "secondary")
            with columns[1]:
                st.button("Transfer", type='secondary')
            with columns[2]:
                st.button("Transfer From", type='secondary')

    st.markdown("---\n")
    st.markdown("#### "+ "Contract Deploy")
    st.text_area("ByteCode:",placeholder="0x60806040")
    st.button("Deploy on layer2", type = "primary")
    st.markdown("Contract Address:"+"0x7759e73e9b29eB76476b1B0a21c6608fEDc8C16C")


