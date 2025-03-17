import pandas as pd
import requests
import streamlit as st

st.set_page_config(
    page_title="Analyzer",
    page_icon="📈",
)

with st.sidebar:
    st.write("Тут будет описание анализатора, пока что лень.")


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
                response_data = response.json()
                # st.json(response_data)
                # cluster_img = response_data["cluster_image_ling"]
                num_clusters = response_data["optimal_cluster"]
                bad_segments = response_data["bad_company_segments"]
                scatter_data = pd.read_json(response_data["scatter_data"])
                scatter_data["cluster_id"] = scatter_data["cluster_id"].astype(str)
                st.write("# Отчёт по эффективности рекламной кампании")
                st.write(f"Модуль анализа определил **{num_clusters} кластеров** рекламных объявлений, объединенных по схожим характеристикам.")
                st.write("### Неэффективные сегменты")
                st.write("В ходе анализа были выявлены сегменты, которые демонстрируют низкую эффективность. Рекомендуется отключить показ рекламы для следующих сегментов:")
                bad_segments_formatted = "\n".join([f"* {segment}" for segment in bad_segments])
                st.write(bad_segments_formatted)
                st.write("### Визуализация кластеров")
                # st.image(cluster_img)
                st.scatter_chart(data=scatter_data, x="0", y="1", color="cluster_id", x_label="Первая главная компонента", y_label="Вторая главная компонента")
                st.write("**Рекомендации:** Пересмотрите стратегию показа рекламы для выявленных неэффективных сегментов, чтобы оптимизировать бюджет и повысить общую эффективность кампании.")
            else:
                st.error(f"Failed to upload file. Status code: {response.status_code}", icon="❌")
        except Exception as e:
            st.error(f"An error occurred: {e}")


st.write("# ⚙️ AutoML")
st.write("Upload your company stat from yandex and get analysis!")
upload_file = st.file_uploader("Upload company statistic")
st.button("Upload", on_click=upload_file_into_server)


