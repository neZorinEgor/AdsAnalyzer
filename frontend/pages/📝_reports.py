import streamlit as st
import requests
import json
from time import sleep


# Настройки страницы
st.set_page_config(
    page_title="Reports Analyzer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

from utils import controller

# CSS стили
st.markdown("""
    <style>
        .stExpander {
            border-radius: 10px;
            border: 1px solid rgba(49, 51, 63, 0.2);
            margin-bottom: 1rem;
        }
        .stExpander:hover {
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
        }
        .report-header {
            font-size: 1.1rem !important;
            font-weight: 600 !important;
        }
        .ready-badge {
            background-color: #28a745 !important;
            color: white !important;
            padding: 3px 10px;
            border-radius: 12px;
            font-size: 0.8rem;
            font-weight: 500;
        }
        .processing-badge {
            background-color: #ffc107 !important;
            color: black !important;
            padding: 3px 10px;
            border-radius: 12px;
            font-size: 0.8rem;
            font-weight: 500;
        }
        .stButton>button {
            border-radius: 8px;
            padding: 8px 16px;
            transition: all 0.3s;
        }
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        .bad-segment {
            background-color: #fff8e1;
            padding: 8px 12px;
            border-radius: 6px;
            margin: 4px 0;
            border-left: 4px solid #ffc107;
        }
        .file-path {
            font-family: monospace;
            background-color: #f5f5f5;
            padding: 6px 10px;
            border-radius: 4px;
            font-size: 0.9em;
        }
    </style>
""", unsafe_allow_html=True)

# Заголовок страницы с описанием
st.title("📊 Анализ рекламных отчетов")
st.markdown("Просмотр и управление результатами анализа рекламных кампаний")


# Индикатор загрузки
@st.fragment
def show_loading():
    with st.empty():
        for i in range(3):
            st.write("Загрузка данных" + "." * (i + 1))
            sleep(0.5)
        st.success("Данные успешно загружены!")


# Функция для получения данных
@st.cache_data(ttl=60, show_spinner=False)
def fetch_reports(limit=10, offset=0):
    url = f"http://127.0.0.1:8000/ads/reports/paginate?limit={limit}&offset={offset}"
    try:
        response = requests.get(
            url,
            headers={
                "accept": "application/json",
                "Cookie": f"ads_analyzer={controller.get('ads_token')}"
            },
            timeout=10
        )
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Ошибка сервера: {response.status_code}")
            print(controller.get("ads_token"))
            return []
    except requests.exceptions.RequestException as e:
        st.error(f"Ошибка соединения: {str(e)}")
        return []


# Фильтры в сайдбаре
with st.sidebar:
    st.header("Фильтры")
    status_filter = st.selectbox(
        "Статус отчета",
        ["Все", "Готов", "В обработке"],
        index=0
    )
    company_id_filter = st.text_input("Фильтр по ID компании")

    st.markdown("---")
    st.markdown("**Статистика**")
    if st.button("Обновить данные", use_container_width=True):
        st.cache_data.clear()

# Получаем данные с индикатором загрузки
with st.spinner("Загрузка отчетов..."):
    reports = fetch_reports()
    if reports:
        show_loading()

# Отображение данных с фильтрацией
if reports:
    # Применяем фильтры
    filtered_reports = reports
    if status_filter != "Все":
        filtered_reports = [r for r in filtered_reports if
                            (r['is_ready'] and status_filter == "Готов") or
                            (not r['is_ready'] and status_filter == "В обработке")]

    if company_id_filter:
        filtered_reports = [r for r in filtered_reports if company_id_filter in str(r['company_id'])]

    if not filtered_reports:
        st.warning("Нет отчетов, соответствующих выбранным фильтрам")
    else:
        # Статистика вверху
        ready_count = sum(1 for r in filtered_reports if r['is_ready'])
        total_count = len(filtered_reports)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Всего отчетов", total_count)
        with col2:
            st.metric("Готовых отчетов", ready_count)
        with col3:
            st.metric("В обработке", total_count - ready_count)

        st.divider()

        # Отображение отчетов
        for report in filtered_reports:
            status_badge = (
                'Готов' if report['is_ready']
                else 'В обработке'
            )

            with st.expander(
                    f"📋 **Отчет #{report['id']}** &nbsp;&nbsp;|&nbsp;&nbsp; "
                    f"🏢 **Компания {report['company_id']}** &nbsp;&nbsp;|&nbsp;&nbsp; "
                    f"{status_badge}",
                    expanded=False
            ):
                col1, col2 = st.columns([1, 1.5])

                with col1:
                    st.markdown("#### 📌 Основная информация")
                    st.markdown(f"**📧 Email:** {report['user_email']}")
                    st.markdown(f"**🆔 ID компании:** `{report['company_id']}`")

                    if report['is_ready']:
                        st.markdown(f"**✅ Статус:** <span class='ready-badge'>Готов</span>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"**⏳ Статус:** <span class='processing-badge'>В обработке</span>",
                                    unsafe_allow_html=True)

                    st.markdown(f"**ℹ️ Информация:** {report['info']}")

                with col2:
                    st.markdown("#### 🔍 Детали анализа")

                    # Обработка bad_segments
                    try:
                        bad_segments = json.loads(report['bad_segments'])
                        if isinstance(bad_segments, dict):
                            st.markdown("**⚠️ Проблемные сегменты:**")
                            for key, value in bad_segments.items():
                                st.markdown(
                                    f"<div class='bad-segment'>"
                                    f"<strong>Кластер {key}:</strong> {value}"
                                    f"</div>",
                                    unsafe_allow_html=True
                                )
                        else:
                            st.markdown(f"**⚠️ Проблемные сегменты:** {bad_segments}")
                    except:
                        st.markdown(f"**⚠️ Проблемные сегменты:** {report['bad_segments']}")

                if report['is_ready']:
                    st.divider()
                    st.markdown("#### 🚀 Действия")
                    st.html(f'''
                        <a href="/statistic?report_id={report['id']}" role="button" target="_blank">
                            Visit Page
                        </a>
                    ''',)
else:
    st.warning("Нет данных для отображения. Проверьте подключение к серверу.")