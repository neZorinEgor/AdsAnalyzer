import streamlit as st

# Страница входа
st.title("Вход")

url = f"http://0.0.0.0:8000/ads/yandex/oauth/login"
st.markdown(f'[Перейти на страницу авторизации]({url})', unsafe_allow_html=True)
