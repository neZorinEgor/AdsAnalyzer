import streamlit as st


with st.sidebar:
    st.write("This code will be printed to the sidebar.")

st.write("# 📰 AdsCompanyAnalyzer")

st.page_link("pages/1_📈_Analyzer.py", label="Проанализировать компанию", icon="📈")

