import pandas as pd
import requests
import streamlit as st
import plotly.express as px
import plotly.figure_factory as ff

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
                num_clusters = response_data["optimal_cluster"]
                bad_segments = response_data["bad_company_segments"]
                scatter_data = pd.read_json(response_data["scatter_data"])

                # Преобразуем cluster_id в строку для корректного отображения в plotly
                scatter_data["cluster_id"] = scatter_data["cluster_id"].astype(str)

                st.write("# Отчёт по эффективности рекламной кампании")
                st.write(f"Модуль анализа определил **{num_clusters} кластеров** рекламных объявлений, объединенных по схожим характеристикам.")
                st.write("### Визуализация кластеров")
                fig = px.scatter(
                    scatter_data,
                    x="x",
                    y="y",
                    color="cluster_id",  # Цвет точек по кластерам
                    hover_data=scatter_data.columns,  # Все данные для отображения при наведении
                    labels={"x": "Первая главная компонента", "y": "Вторая главная компонента"},
                    size_max=0.4,
                    opacity=0.7,
                )
                st.plotly_chart(fig)
                # Распределение кластеров
                st.text("Распределение кластеров:")
                st.dataframe(scatter_data["cluster_id"].value_counts())
                st.write("Первичная статистика эффективного кластера **#3**:")
                st.dataframe(scatter_data.query("cluster_id=='3'").describe())
                st.divider()
                # Неэффективные сигменты
                st.write("### Неэффективные сегменты")
                st.write("В ходе анализа были выявлены сегменты, которые демонстрируют низкую эффективность. Рекомендуется отключить показ рекламы для следующих сегментов:")
                bad_segments_formatted = "\n".join([f"* {segment}" for segment in bad_segments])
                st.write(bad_segments_formatted)
                st.write("**Рекомендации:** Пересмотрите стратегию показа рекламы для выявленных неэффективных сегментов, чтобы оптимизировать бюджет и повысить общую эффективность кампании.")
                group = scatter_data.query("cluster_id=='3'").groupby(["Пол", "Возраст"])[
                    ["CTR (%)", "Ср. цена клика (руб.)", "Отказы (%)", "Глубина (стр.)", "Расход (руб.)",
                     'Взвешенные показы', 'Клики']
                ].quantile(0.5)

                # Сброс индекса для удобства отображения
                group = group.reset_index()

                # Вывод результата
                st.dataframe(group)
            else:
                st.error(f"Failed to upload file. Status code: {response.status_code}", icon="❌")
        except Exception as e:
            st.error(f"An error occurred: {e}")


st.write("# ⚙️ AutoML")
st.write("Upload your company stat from yandex and get analysis!")
upload_file = st.file_uploader("Upload company statistic")
st.button("Upload", on_click=upload_file_into_server)
