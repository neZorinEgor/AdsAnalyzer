import json
import numpy as np
import requests
import pandas as pd
import streamlit as st
import plotly.express as px
from io import StringIO

# Настройка страницы
st.set_page_config(layout="wide", page_title="Анализ рекламных объявлений", page_icon="📊")


# Получение данных
def fetch_data(report_id):
    url = f"http://127.0.0.1:8000/ads/report/{report_id}"
    headers = {
        "accept": "application/json",
        "Cookie": f"ads_analyzer={st.session_state['token']}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        json_data = response.json()
        clustered_df = pd.read_json(StringIO(json_data.get("clustered_df")))
        impact_info_df = pd.read_json(StringIO(json_data.get("impact_df")))
        impact_info_df = impact_info_df.rename(columns={'Unnamed: 0': 'Метрика'})
        return {
            "clustered_df": clustered_df,
            "impact_df": impact_info_df,
            "bad_segments": json.loads(json_data.get("bad_segments"))
        }
    else:
        st.warning("Ошибка загрузки данных.")
        return None


# Загрузка
data = fetch_data(report_id=st.session_state["last_report_id"])
if data is None:
    st.stop()

cluster_info_df = data["clustered_df"]
impact_df = data["impact_df"]
bad_segments = data.get("bad_segments", {})
# clusters_id = list(set(cluster_info_df["cluster_id"]))

# Сайдбар
with st.sidebar:
    st.header("📈 Ключевые метрики")
    total_clusters = cluster_info_df['cluster_id'].nunique()
    st.metric("Всего кластеров", total_clusters)

    problem_clusters = sum(1 for seg in bad_segments.values() if seg != "не выявлено")
    st.metric("Кластеров с проблемами", f"{problem_clusters}/{total_clusters}")

# Основной заголовок
st.title("Анализ эффективности рекламных объявлений")
st.markdown("""
Визуализация кластеров похожих объявлений и выявление проблемных сегментов аудитории.
""")

# Вкладки
tab1, tab2, tab3 = st.tabs(["📊 Кластеры объявлений", "🔍 Детализация кластеров", "⚠ Проблемные сегменты"])

# 📊 Кластеры
with tab1:
    st.header("Распределение объявлений по кластерам")
    col1, col2 = st.columns([2, 1])
    with col1:
        fig = px.scatter(
            cluster_info_df,
            x="pca_1",
            y="pca_2",
            color="cluster_id",
            hover_data=cluster_info_df.columns,
            labels={"x": "Главная компонента 1", "y": "Главная компонента 2"},
            title="Карта кластеров объявлений",
            size_max=10,
            opacity=0.7,
        )
        st.plotly_chart(fig)
    with col2:
        st.subheader("Количество кластеров")
        cluster_stats = cluster_info_df['cluster_id'].value_counts().reset_index()
        cluster_stats.columns = ['Кластер', 'Количество объявлений']
        st.dataframe(cluster_stats, height=150)

    st.divider()
    st.markdown("""
    **Зачем мы группируем объявления в кластеры?**

    🔍 **Понимание структуры кампании**  
    🎯 **Точная оптимизация бюджета**  
    📊 **Выявление лучших практик**  
    ⚠ **Обнаружение скрытых проблем**
    """)

# 🔍 Детализация
with tab2:
    df_melted = impact_df.melt(id_vars='Метрика', var_name='Кластер', value_name='Влияние')

    st.title('📊 Влияние кластеров на рекламные метрики')
    st.markdown("""
    Здесь показано, как различные кластеры аудитории **влияют на ключевые показатели** рекламной кампании.

    👉 *Под «влиянием» понимается вклад сегмента в изменение показателя по сравнению с остальными сегментами.*
    """)

    chart_type = st.selectbox("Выберите тип графика", ["📊 Столбчатый (накопленный)", "📊 Столбчатый (по группам)", "📈 Линейный график", "🌡️ Тепловая карта"])

    if chart_type == "📊 Столбчатый (по группам)":
        fig = px.bar(df_melted, x='Метрика', y='Влияние', color='Кластер', barmode='group')
    elif chart_type == "📊 Столбчатый (накопленный)":
        fig = px.bar(df_melted, y='Метрика', x='Влияние', color='Кластер', barmode='stack', orientation='h')
    elif chart_type == "📈 Линейный график":
        fig = px.line(df_melted, x='Метрика', y='Влияние', color='Кластер', markers=True)
    else:  # Тепловая карта
        heat_df = impact_df.set_index('Метрика')
        fig = px.imshow(heat_df, text_auto=True, aspect="auto", color_continuous_scale='RdBu', labels=dict(x="Кластер", y="Метрика", color="Влияние"))

    fig.update_layout(
        xaxis_title='Метрика',
        yaxis_title='Влияние',
        hovermode='x unified',
        xaxis={'categoryorder': 'total descending'},
        height=600
    )
    fig.update_xaxes(tickangle=45)
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("📄 Таблица с влиянием метрик по кластерам")
    st.dataframe(impact_df, height=500, use_container_width=True)

    st.subheader("🔍 Интерпретация кластеров")

    clusters = [col for col in impact_df.columns if col != 'Метрика']
    cluster_descriptions = {cluster: {'особенности': [], 'уникальные_метрики': []} for cluster in clusters}

    for metric in impact_df['Метрика'].unique():
        row = impact_df[impact_df['Метрика'] == metric].iloc[0]
        values = row[clusters]
        non_zero_values = values[values > 0]

        if len(non_zero_values) == 1:
            cluster = non_zero_values.idxmax()
            cluster_descriptions[cluster]['уникальные_метрики'].append(metric)
            continue

        max_val, min_val = values.max(), values.min()
        for cluster in clusters:
            val = values[cluster]
            if val == max_val and val > 0:
                cluster_descriptions[cluster]['особенности'].append(f"Выделяется по метрике **{metric}** (влияние: {val:.3f})")
            if val == min_val and min_val < max_val and val >= 0:
                cluster_descriptions[cluster]['особенности'].append(f"Минимальное влияние по метрике **{metric}** ({val:.3f})")

    for cluster in clusters:
        with st.expander(f"### 🧩 Кластер {cluster}"):

            if cluster_descriptions[cluster]['уникальные_метрики']:
                st.markdown("**Уникальные показатели:**")
                for metric in cluster_descriptions[cluster]['уникальные_метрики']:
                    val = impact_df[impact_df['Метрика'] == metric].iloc[0][cluster]
                    st.markdown(f"- {metric}: {val:.3f} (только этот кластер влияет)")

            if cluster_descriptions[cluster]['особенности']:
                st.markdown("**Основные характеристики:**")
                for desc in cluster_descriptions[cluster]['особенности']:
                    st.markdown(f"- {desc}")
            else:
                st.markdown("_Не выявлены ярко выраженные особенности._")

            recommendations = []
            cluster_data = impact_df.set_index('Метрика')[cluster]

            if 'Прибыль (руб.)' in cluster_data and cluster_data['Прибыль (руб.)'] == cluster_data.max():
                recommendations.append("💡 Рекомендуется увеличить бюджет для этого сегмента")
            if 'Отказы (%)' in cluster_data and cluster_data['Отказы (%)'] == cluster_data.max():
                recommendations.append("🚨 Проверить посадочную страницу (высокий процент отказов)")
            if 'Ср. цена клика (руб.)' in cluster_data and cluster_data['Ср. цена клика (руб.)'] == cluster_data.max():
                recommendations.append("📉 Оптимизировать ставки в аукционе (высокая цена клика)")

            if recommendations:
                st.markdown("**Рекомендации по действиям:**")
                for rec in recommendations:
                    st.markdown(f"- {rec}")

            st.markdown("---")


# ⚠ Проблемные сегменты
with tab3:
    st.header("Проблемные сегменты")
    if not bad_segments:
        st.success("Все сегменты работают стабильно. Проблем не выявлено.")
    else:
        for cluster, problem in bad_segments.items():
            if problem != "не выявлено":
                st.markdown(f"### Кластер {cluster}")
                st.error(f"Обнаружена проблема: {problem}")
                st.markdown("**Рекомендации:**")
                if "CTR" in problem:
                    st.markdown("- Пересмотреть креативы и офферы")
                if "ставка" in problem or "дорого" in problem:
                    st.markdown("- Настроить стратегию оптимизации ставок")
                if "конверсии" in problem:
                    st.markdown("- Проанализировать воронку продаж")
                st.markdown("---")
