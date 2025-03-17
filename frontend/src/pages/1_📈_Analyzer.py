import requests
import streamlit as st

st.set_page_config(
    page_title="Analyzer",
    page_icon="📈",
)


def upload_file_into_server():
    if upload_file is None:
        st.warning("Please, select file.", icon="⚠️")
    else:
        try:
            # Отправка файла на сервер
            files = {'company_df': (upload_file.name, upload_file, 'application/json')}
            response = requests.post(
                'http://localhost:8001/ads/upload',
                headers={'accept': 'application/json'},
                files=files
            )
            # Проверка ответа от сервера
            if response.status_code == 200:
                st.success("File uploaded successfully!", icon="✅")
                st.text(response.text)
            else:
                st.error(f"Failed to upload file. Status code: {response.status_code}", icon="❌")
        except Exception as e:
            st.error(f"An error occurred: {e}")


upload_file = st.file_uploader("Upload company statistic")
st.button("Upload", on_click=upload_file_into_server)


