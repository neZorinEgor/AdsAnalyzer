import streamlit as st
import requests
from utils import controller

st.write(st.query_params)

if "code" in st.query_params:
    code = st.query_params["code"]
    params = {"code": code}
    response = requests.get("http://127.0.0.1:8000/callback", params=params)
    if response.status_code == 200:
        token = response.text
        controller.set('ads_token', token)
    else:
        st.write("Expire token. Try again latter")

