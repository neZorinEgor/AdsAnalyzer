import json
import random

import requests
import pandas as pd
import streamlit as st
import plotly.express as px
from io import StringIO

st.set_page_config(layout="wide", page_title="Анализ рекламных объявлений", page_icon="📊")


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
            "bad_segments": json.loads(json_data.get("bad_segments")),
            "llm_response": json_data["llm_response"]
        }
    else:
        st.warning("Ошибка загрузки данных.")
        return None


def generate_colors(n):
    return [f"hsl({random.randint(0, 360)}, 100%, 50%)" for _ in range(n)]


data = fetch_data(report_id=st.session_state["last_report_id"])
if data is None:
    st.stop()
    st.warning("Возникли проблемы при загрузке данных")


cluster_info_df = data["clustered_df"]
impact_df = data["impact_df"]
bad_segments = data.get("bad_segments", {})
llm_response = data.get("llm_response")
colors = generate_colors(cluster_info_df['cluster_id'].nunique())
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

# Кластеры
with tab1:
    st.header("Распределение объявлений по кластерам")
    col1, col2 = st.columns([2, 1])
    with col1:
        fig = px.scatter(
            cluster_info_df,
            x="pca_1",
            y="pca_2",
            color="cluster_id",
            color_discrete_sequence=colors,
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

# 🔍 Детализация
with tab2:
    # Подготовка данных
    df_melted = impact_df.melt(id_vars='Метрика', var_name='Кластер', value_name='Влияние')

    # Вычисляем максимальные значения для каждой метрики для нормализации
    max_values = impact_df.set_index('Метрика').max(axis=1)
    min_values = impact_df.set_index('Метрика').min(axis=1)

    st.title('📊 Влияние кластеров на рекламные метрики')
    st.markdown("""
    <div style="background-color:#f0f2f6;padding:15px;border-radius:10px;margin-bottom:20px;">
        Здесь показано, как различные кластеры аудитории <b>влияют на ключевые показатели</b> рекламной кампании.<br>
        👉 <i>Прогресс-бары показывают влияние относительно максимального значения по каждому показателю.</i>
    </div>
    """, unsafe_allow_html=True)

    # Выбор типа графика
    chart_type = st.selectbox("Выберите тип графика",
                              ["📊 Столбчатый (накопленный)",
                               "📊 Столбчатый (по группам)",
                               "📈 Линейный график",
                               "🌡️ Тепловая карта"])

    # Отрисовка выбранного графика
    if chart_type == "📊 Столбчатый (по группы)":
        fig = px.bar(df_melted, x='Метрика', y='Влияние', color='Кластер', barmode='group')
    elif chart_type == "📊 Столбчатый (накопленный)":
        fig = px.bar(df_melted, y='Метрика', x='Влияние', color='Кластер', barmode='stack', orientation='h')
    elif chart_type == "📈 Линейный график":
        fig = px.line(df_melted, x='Метрика', y='Влияние', color='Кластер', markers=True)
    else:  # Тепловая карта
        heat_df = impact_df.set_index('Метрика')
        fig = px.imshow(heat_df, text_auto=True, aspect="auto",
                        color_continuous_scale='RdBu',
                        labels=dict(x="Кластер", y="Метрика", color="Влияние"))

    fig.update_layout(
        xaxis_title='Метрика',
        yaxis_title='Влияние',
        hovermode='x unified',
        height=600
    )
    st.plotly_chart(fig, use_container_width=True)

    # Анализ кластеров
    st.subheader("🔍 Детальный анализ по кластерам")
    clusters = [col for col in impact_df.columns if col != 'Метрика']

    for cluster in clusters:
        with st.expander(f"### 🎯 Кластер {cluster}", expanded=False):
            # Получаем данные для текущего кластера
            cluster_data = cluster_info_df[cluster_info_df["cluster_id"] == int(cluster)]

            # Создаем колонки для макета
            col1, col2, col3 = st.columns([1, 1, 2])

            with col1:
                # Круговая диаграмма по полу
                if "Пол" in cluster_data.columns:
                    gender_dist = cluster_data["Пол"].value_counts(normalize=True) * 100
                    fig_gender = px.pie(
                        values=gender_dist.values,
                        names=gender_dist.index.str.replace('GENDER_', ''),
                        title="Распределение по полу",
                        hole=0.4,
                        color_discrete_sequence=px.colors.qualitative.Pastel
                    )
                    fig_gender.update_layout(showlegend=False, margin=dict(t=40, b=10))
                    st.plotly_chart(fig_gender, use_container_width=True)

            with col2:
                # Круговая диаграмма по возрасту
                if "Возраст" in cluster_data.columns:
                    age_dist = cluster_data["Возраст"].value_counts(normalize=True) * 100
                    fig_age = px.pie(
                        values=age_dist.values,
                        names=age_dist.index.str.replace('AGE_', '').str.replace('_', '-'),
                        title="Распределение по возрасту",
                        hole=0.4,
                        color_discrete_sequence=px.colors.qualitative.Pastel1
                    )
                    fig_age.update_layout(showlegend=False, margin=dict(t=40, b=10))
                    st.plotly_chart(fig_age, use_container_width=True)

            with col3:
                # Ключевые метрики
                cluster_cost = cluster_data["Расход (руб.)"].sum() / 1000000
                avg_ctr = cluster_data["CTR (%)"].mean()
                avg_cpc = cluster_data["Ср. цена клика (руб.)"].mean()/1000000

                st.markdown(f"""
                <div style="background:linear-gradient(135deg, #f8f9fa, #e9ecef);padding:15px;border-radius:10px;margin-bottom:15px;border-left:4px solid #6c757d;">
                    <div style="font-size:16px;color:#6c757d;">Общие затраты</div>
                    <div style="font-size:24px;font-weight:bold;color:#2c3e50;">{cluster_cost:,.1f} ₽</div>
                </div>
                """, unsafe_allow_html=True)

                metric_col1, metric_col2 = st.columns(2)
                with metric_col1:
                    st.markdown(f"""
                    <div style="background:#f8f9fa;padding:10px;border-radius:10px;margin-bottom:10px;text-align:center;box-shadow:0 2px 4px rgba(0,0,0,0.05);">
                        <div style="font-size:14px;color:#6c757d;">Средний CTR</div>
                        <div style="font-size:20px;font-weight:bold;color:#2c3e50;">{avg_ctr:.2f}%</div>
                    </div>
                    """, unsafe_allow_html=True)

                with metric_col2:
                    st.markdown(f"""
                    <div style="background:#f8f9fa;padding:10px;border-radius:10px;margin-bottom:10px;text-align:center;box-shadow:0 2px 4px rgba(0,0,0,0.05);">
                        <div style="font-size:14px;color:#6c757d;">Цена клика</div>
                        <div style="font-size:20px;font-weight:bold;color:#2c3e50;">{avg_cpc:,.1f} ₽</div>
                    </div>
                    """, unsafe_allow_html=True)

            st.markdown("---")

            # Влияние на показатели с нормализованными прогресс-барами
            st.markdown("### 📈 Влияние на показатели (относительно максимума)")
            with st.container():
                st.markdown("""
                <style>
                    .metric-progress {
                        width: 100%;
                        margin-bottom: 15px;
                    }
                    .metric-header {
                        display: flex;
                        justify-content: space-between;
                        margin-bottom: 5px;
                        font-size: 14px;
                    }
                    .metric-name {
                        white-space: nowrap;
                        overflow: hidden;
                        text-overflow: ellipsis;
                        max-width: 70%;
                    }
                    .metric-value {
                        color: #495057;
                        font-weight: bold;
                    }
                    .progress-container {
                        height: 10px;
                        background-color: #e9ecef;
                        border-radius: 5px;
                        overflow: hidden;
                    }
                    .progress-bar {
                        height: 100%;
                        border-radius: 5px;
                    }
                    .metric-comparison {
                        font-size: 12px;
                        color: #6c757d;
                        text-align: right;
                        margin-top: 2px;
                    }
                </style>
                """, unsafe_allow_html=True)

                for metric in impact_df['Метрика'].unique():
                    val = impact_df[impact_df['Метрика'] == metric].iloc[0][cluster]
                    max_val = max_values[metric]
                    min_val = min_values[metric]

                    if max_val > 0:  # Только если есть значения
                        percentage = (val / max_val) * 100
                        color = "#2ecc71" if percentage > 75 else "#3498db" if percentage > 40 else "#f39c12"

                        st.markdown(f"""
                        <div class="metric-progress">
                            <div class="metric-header">
                                <span class="metric-name" title="{metric}">{metric}</span>
                                <span class="metric-value">{val:.3f}</span>
                            </div>
                            <div class="progress-container">
                                <div class="progress-bar" style="width:{percentage}%;background-color:{color};"></div>
                            </div>
                            <div class="metric-comparison">
                                Макс: {max_val:.3f} | Мин: {min_val:.3f}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

            st.markdown("---")

            # Уникальные особенности кластера
            st.markdown("### 🔍 Уникальные особенности")

            unique_features = []
            for metric in impact_df['Метрика'].unique():
                row = impact_df[impact_df['Метрика'] == metric].iloc[0]
                values = row[clusters]
                if values[cluster] == max_values[metric] and max_values[metric] > 0:
                    unique_features.append((metric, values[cluster]))

            if unique_features:
                for metric, val in sorted(unique_features, key=lambda x: x[1], reverse=True):
                    st.markdown(f"""
                    <div style="background:#e8f7f0;padding:12px;border-radius:8px;margin-bottom:10px;border-left:4px solid #2ecc71;">
                        <div style="display:flex;align-items:center;">
                            <span style="margin-right:10px;font-size:20px;">🏆</span>
                            <div>
                                <div style="font-weight:bold;color:#27ae60;">{metric}</div>
                                <div>Наибольшее влияние среди всех кластеров: <b>{val:.3f}</b></div>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div style="background:#f8f9fa;padding:15px;border-radius:8px;text-align:center;color:#6c757d;">
                    Этот кластер не имеет показателей с максимальным влиянием
                </div>
                """, unsafe_allow_html=True)
    st.markdown(llm_response)

# ⚠ Проблемные сегменты
with tab3:
    st.header("🔍 Проблемные сегменты", divider="red")

    if not bad_segments:
        col1, col2, col3 = st.columns([1, 3, 1])
        with col2:
            st.markdown("""
            <div style="text-align: center; padding: 2em; border-radius: 10px; 
                        background-color: #f0f8ff; margin: 1em 0;">
                <h3 style="color: #2e7d32;">🎉 Отличные новости!</h3>
                <p>Все сегменты работают эффективно</p>
                <p style="font-size: 0.9em; color: #666;">
                Нет проблемных кластеров для оптимизации
                </p>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("""
            <div style="text-align: center; margin-top: 1em;">
                <p>Что можно сделать:</p>
                <ul style="display: inline-block; text-align: left;">
                    <li>Проверить общие показатели эффективности</li>
                    <li>Проанализировать динамику изменений</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
    else:
        problematic_found = False
        for cluster, problem in bad_segments.items():
            if problem != "не выявлено":
                problematic_found = True
                with st.container(border=True):
                    # Шапка карточки
                    cols = st.columns([1, 10])
                    with cols[0]:
                        st.markdown(f"### 🏷️ {cluster}")
                    with cols[1]:
                        st.error(f"**Проблема:** {problem}", icon="⚠️")

                    # Рекомендации
                    with st.expander("📌 Рекомендации", expanded=True):
                        if "CTR" in problem:
                            st.markdown("""
                            - **Оптимизация креативов:**
                              - Протестировать новые варианты объявлений
                              - Улучшить релевантность офферов
                            """)

                        if "ставка" in problem or "дорого" in problem:
                            st.markdown("""
                            - **Оптимизация ставок:**
                              - Настроить автоматическое управление ставками
                              - Скорректировать стратегию аукциона
                            """)

                        if "конверсии" in problem:
                            st.markdown("""
                            - **Анализ воронки:**
                              - Проверить UX посадочных страниц
                              - Оптимизировать процесс оформления
                            """)

                    # Кнопка действия
                    st.button(
                        "Убрать сегменты из компании",
                        key=f"fix_{cluster}",
                        help=f"Применить рекомендации для кластера {cluster}",
                        use_container_width=True
                    )
        if not problematic_found:
            st.info("ℹ️ Проблемные сегменты не обнаружены в текущем анализе", icon="ℹ️")