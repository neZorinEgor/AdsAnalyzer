import json
import numpy as np
import requests
import pandas as pd
import streamlit as st
import plotly.express as px
from io import StringIO
from streamlit_cookies_controller import CookieController

# Настройка страницы
st.set_page_config(layout="wide", page_title="Анализ рекламных объявлений", page_icon="📊")
controller = CookieController()


@st.cache_data
def fetch_data(report_id):
    url = f"http://127.0.0.1:8000/ads/report/{report_id}"
    headers = {
        "accept": "application/json",
        "Cookie": f"ads_analyzer={controller.get("ads_token")}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        clustered_df = pd.read_json(StringIO(response.json().get("clustered_df")))
        impact_info_df = pd.read_json(StringIO(response.json().get("impact_df")))
        impact_info_df = impact_info_df.rename(columns={'Unnamed: 0': 'Метрика'})
        # impact_df.col
        return {
            "clustered_df": clustered_df,
            "impact_df": impact_info_df,
            "bad_segments": json.loads(response.json().get("bad_segments"))
        }
    else:
        st.warning("Ошибка загрузки данных.")
        print(response.text)
        return None


# Загрузка данных
data = fetch_data(report_id=st.query_params["report_id"])
if data is None:
    st.stop()

cluster_info = data.get("clustered_df")
impact_df = data.get("impact_df")
bad_segments = data.get("bad_segments", {})
clusters_id = list(set(cluster_info["cluster_id"]))

# Сайдбар с аналитикой
with st.sidebar:
    st.header("📈 Ключевые метрики")
    total_clusters = cluster_info['cluster_id'].nunique()
    st.metric("Всего кластеров", total_clusters)

    # avg_cluster_size = round(cluster_info['cluster_id'].value_counts().mean(), 1)
    # st.metric("Средний размер кластера", avg_cluster_size)

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
        st.subheader("Количество кластеров")
        cluster_stats = cluster_info['cluster_id'].value_counts().reset_index()
        cluster_stats.columns = ['Кластер', 'Количество объявлений']
        st.dataframe(cluster_stats, height=150)
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
    # print(impact_df)
    # препроцессинг данных в "длинный" формат для plotly
    df_melted = impact_df.melt(id_vars='Метрика', var_name='Кластер', value_name='SHAP Impact')
    # интерактивный график
    st.title('Вклад кластеров в метрики рекламной кампании')
    st.write("SHAP Impact каждого кластера по метрикам")
    # выбор типа графика (надо ли?)
    chart_type = st.selectbox("Bar Chart (накопленный)",
                             ["Bar Chart (накопленный)", "Bar Chart (сгруппированный)", "Line Chart"])
    if chart_type == "Bar Chart (сгруппированный)":
        fig = px.bar(df_melted, x='Метрика', y='SHAP Impact', color='Кластер',
                     barmode='group', title='Вклад кластеров по метрикам (сгруппированный)')
    elif chart_type == "Bar Chart (накопленный)":
        fig = px.bar(df_melted, y='Метрика', x='SHAP Impact', color='Кластер', barmode='stack', title='Вклад кластеров по метрикам (накопленный)' )
    else:
        fig = px.line(df_melted, x='Метрика', y='SHAP Impact', color='Кластер', title='Вклад кластеров по метрикам (линейный график)')
    # Настройка внешнего вида
    fig.update_layout(
        xaxis_title='Метрика',
        yaxis_title='SHAP Impact',
        hovermode='x unified',
        xaxis={'categoryorder':'total descending'}
    )
    fig.update_xaxes(tickangle=45)
    st.plotly_chart(fig, use_container_width=True)
    # SHAP Impact table
    st.subheader("Таблица SHAP Impact")
    st.dataframe(impact_df, height=len(impact_df.columns) * 101)
    # Вредные советы...


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
