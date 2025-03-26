import json
import requests
import pandas as pd
import streamlit as st
import plotly.express as px
from io import StringIO
from streamlit_plotly_events import plotly_events

# Настройка страницы
st.set_page_config(layout="wide", page_title="Анализ рекламных объявлений", page_icon="📊")


@st.cache_data
def fetch_data():
    url = "http://127.0.0.1:8000/ads/8"
    headers = {
        "accept": "application/json",
        "Cookie": f"ads_analyzer={st.secrets["token"]}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        clustered_df = pd.read_json(StringIO(response.json().get("clustered_df")))
        clustered_df["cluster_id"] = clustered_df["cluster_id"].apply(lambda x: x + 1)
        return {
            "clustered_df": clustered_df,
            "bad_segments": json.loads(response.json().get("bad_segments"))
        }
    else:
        st.warning("Ошибка загрузки данных.")
        return None


# Загрузка данных
data = fetch_data()
if data is None:
    st.stop()

cluster_info = data.get("clustered_df")
bad_segments = data.get("bad_segments", {})

# Сайдбар с аналитикой
with st.sidebar:
    st.header("📈 Ключевые метрики")
    total_clusters = cluster_info['cluster_id'].nunique()
    st.metric("Всего кластеров", total_clusters)

    avg_cluster_size = round(cluster_info['cluster_id'].value_counts().mean(), 1)
    st.metric("Средний размер кластера", avg_cluster_size)

    problem_clusters = sum(1 for seg in bad_segments.values() if seg != "не выявлено")
    st.metric("Кластеров с проблемами", f"{problem_clusters}/{total_clusters}")

# Основная панель
st.title("Анализ эффективности рекламных объявлений")
st.markdown("""
Визуализация кластеров похожих объявлений и выявление проблемных сегментов аудитории.
""")

# Вкладки для разных видов анализа
tab1, tab2, tab3 = st.tabs(["📊 Кластеры объявлений", "🔍 Детализация кластеров", "⚠ Проблемные сегменты"])

with tab1:
    st.header("Распределение объявлений по кластерам")
    col1, col2 = st.columns([2, 1])
    with col1:
        # Интерактивная карта кластеров
        fig = px.scatter(
            cluster_info,
            x="pca_1",
            y="pca_2",
            color="cluster_id",
            hover_data=cluster_info.columns,
            labels={"x": "Главная компонента 1", "y": "Главная компонента 2"},
            title="Карта кластеров объявлений",
            size_max=10,
            opacity=0.7,
        )
        st.plotly_chart(fig)
    with col2:
        # Статистика по кластерам
        st.subheader("Размеры кластеров")
        cluster_stats = cluster_info['cluster_id'].value_counts().reset_index()
        cluster_stats.columns = ['Кластер', 'Количество объявлений']
        st.dataframe(cluster_stats, height=300)
    st.divider()
    st.markdown("""
    **Зачем мы группируем объявления в кластеры?**  

    Кластеризация помогает выявить скрытые закономерности в вашей рекламной кампании, которые не видны при ручном анализе:

    🔍 **1. Понимание структуры кампании**  
    Автоматически находим группы объявлений с похожими характеристиками:
    - Похожие аудитории
    - Схожие показатели эффективности (CTR, конверсии)
    - Одинаковые проблемы или успешные стратегии

    🎯 **2. Точная оптимизация бюджета**  
    Вместо точечной правки каждого объявления вы можете:
    - Массово улучшать целые группы
    - Отключать неэффективные кластеры
    - Увеличивать бюджет для успешных групп

    📊 **3. Выявление лучших практик**  
    Анализ самых успешных кластеров покажет:
    - Какие креативы работают лучше
    - Какие аудитории дают максимум конверсий
    - Какие связки "текст+изображение" эффективны

    ⚠ **4. Обнаружение скрытых проблем**  
    Проблемные кластеры сразу показывают:
    - Какие сегменты аудитории не реагируют на рекламу
    - Какие объявления "сливают" бюджет
    - Какие подходы требуют срочного изменения

    *Пример:* Если все объявления в кластере с женщинами 55+ имеют низкий CTR — это сигнал пересмотреть креативы для этой аудитории.
    """)

with tab2:
    st.header("Детальный анализ кластеров")
    # Распределение характеристик по кластерам
    st.subheader("Распределение параметров по кластерам")
    metric = st.selectbox(
        "Выберите параметр для анализа:",
        options=['ctr', 'conversion_rate', 'spend']  # Замените на реальные колонки
    )
    st.write("todo")
    #
    # fig = px.box(
    #     cluster_info,
    #     x="cluster_id",
    #     y=metric,
    #     color="cluster_id",
    #     title=f"Распределение {metric} по кластерам"
    # )
    # st.plotly_chart(fig, use_container_width=True)
    #
    # # Heatmap корреляции
    # st.subheader("Корреляция параметров")
    # numeric_cols = cluster_info.select_dtypes(include=['float64', 'int64']).columns
    # corr_matrix = cluster_info[numeric_cols].corr()
    # fig = px.imshow(
    #     corr_matrix,
    #     text_auto=True,
    #     aspect="auto",
    #     color_continuous_scale=px.colors.diverging.RdBu_r
    # )
    # st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.header("Анализ проблемных сегментов")
    st.warning("Эти сегменты показывают низкую эффективность и требуют оптимизации")

    for cluster_id, segments in bad_segments.items():
        with st.expander(f"🔴 Кластер {cluster_id}", expanded=True):
            if segments == "не выявлено":
                st.success("✅ Нет проблемных сегментов")
            else:
                st.error("**Проблемные аудитории:**")
                for segment in segments:
                    col1, col2 = st.columns([1, 3])
                    with col1:
                        st.metric("Сегмент", segment.split(":")[0])
                    with col2:
                        st.metric("Параметр", segment.split(":")[1] if ":" in segment else segment)

                # Рекомендации по оптимизации
                st.info("**Рекомендации:**")
                st.markdown("""
                - Рассмотрите возможность исключения этого сегмента из компании
                """)

# Интерактивность - вывод данных при клике
st.sidebar.markdown("---")
