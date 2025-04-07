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

# Заголовок страницы
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

# Получение данных
@st.cache_data(ttl=60, show_spinner=False)
def fetch_reports(limit=10, offset=0):
    url = f"http://127.0.0.1:8000/ads/reports/paginate?limit={limit}&offset={offset}"
    try:
        response = requests.get(
            url,
            headers={
                "accept": "application/json",
                "Cookie": f"ads_analyzer={st.session_state['token']}"
            },
            timeout=10
        )
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Ошибка сервера: {response.status_code}")
            return []
    except requests.exceptions.RequestException as e:
        st.error(f"Ошибка соединения: {str(e)}")
        return []

# Фильтры в боковой панели
with st.sidebar:
    st.header("Фильтры")
    status_filter = st.selectbox("Статус отчета", ["Все", "Готов", "В обработке"])
    company_id_filter = st.text_input("Фильтр по ID компании")

    st.markdown("---")
    st.markdown("**Статистика**")
    if st.button("Обновить данные", use_container_width=True):
        st.cache_data.clear()

# Загрузка данных
with st.spinner("Загрузка отчетов..."):
    reports = fetch_reports()
    if reports:
        show_loading()

# Основное отображение
if reports:
    filtered_reports = reports
    if status_filter != "Все":
        filtered_reports = [
            r for r in filtered_reports if
            (r['is_ready'] and status_filter == "Готов") or
            (not r['is_ready'] and status_filter == "В обработке")
        ]

    if company_id_filter:
        filtered_reports = [r for r in filtered_reports if company_id_filter in str(r['company_id'])]

    if not filtered_reports:
        st.warning("Нет отчетов, соответствующих выбранным фильтрам")
    else:
        ready_count = sum(1 for r in filtered_reports if r['is_ready'])
        total_count = len(filtered_reports)

        col1, col2, col3 = st.columns(3)
        col1.metric("Всего отчетов", total_count)
        col2.metric("Готовых отчетов", ready_count)
        col3.metric("В обработке", total_count - ready_count)

        st.divider()

        # Отображение каждого отчета
        for report in filtered_reports:
            status_label = "Готов" if report['is_ready'] else "В обработке"

            with st.expander(
                f"📋 Отчет #{report['id']} | Компания {report['company_id']} | {status_label}"
            ):
                col1, col2 = st.columns([1, 1.5])

                with col1:
                    st.subheader("📌 Основная информация")
                    st.markdown(f"Создатель РК: {report['user_email']}")
                    st.text(f"ID компании: {report['company_id']}")
                    st.text(f"Готовность: {status_label}")
                    st.markdown(f"Сообщение от сервера: `{report['info']}`")

                with col2:
                    st.subheader("🔍 Детали анализа")
                    try:
                        bad_segments = json.loads(report['bad_segments'])
                        if isinstance(bad_segments, dict):
                            for key, value in bad_segments.items():
                                st.warning(f"Кластер {key}: {value}")
                        else:
                            st.warning(f"Проблемные сегменты: {bad_segments}")
                    except:
                        st.warning(f"Проблемные сегменты: {report['bad_segments']}")

                if report['is_ready']:
                    if st.button("Посмотреть результат", key=f"btn_{report['id']}"):
                        st.session_state["last_report_id"] = report['id']
                        st.success(f"Выбран отчет #{report['id']} (Компания: {report['company_id']})")
                        st.page_link("pages/📈_statistic.py")
else:
    st.warning("У вас пока что нету запросов на анализ эффективности рекламных компаний")
