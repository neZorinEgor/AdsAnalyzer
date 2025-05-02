import streamlit as st
import requests
import json
from time import sleep
from datetime import datetime

# Настройки страницы
st.set_page_config(
    page_title="Reports Analyzer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Стили CSS для улучшения визуального восприятия
st.markdown("""
    <style>
    .report-card {
        border-radius: 10px;
        padding: 1.5em;
        margin-bottom: 1em;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    .report-card:hover {
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        transform: translateY(-2px);
    }
    .status-ready {
        border-left: 5px solid #2ecc71;
    }
    .status-processing {
        border-left: 5px solid #f39c12;
    }
    .badge {
        display: inline-block;
        padding: 0.25em 0.6em;
        font-size: 75%;
        font-weight: 700;
        line-height: 1;
        text-align: center;
        white-space: nowrap;
        vertical-align: baseline;
        border-radius: 10px;
    }
    .badge-ready {
        color: white;
        background-color: #2ecc71;
    }
    .badge-processing {
        color: white;
        background-color: #f39c12;
    }
    .progress-container {
        height: 10px;
        background-color: #f1f1f1;
        border-radius: 5px;
        margin: 10px 0;
    }
    .progress-bar {
        height: 100%;
        border-radius: 5px;
        background-color: #4CAF50;
        width: 0%;
        transition: width 0.5s;
    }
    </style>
""", unsafe_allow_html=True)

# Заголовок страницы с пояснением
st.title("📊 Анализ рекламных отчетов")
st.markdown("""
    <div style="color: #666; margin-bottom: 2em;">
    На этой странице вы можете отслеживать статус обработки ваших рекламных кампаний и просматривать готовые отчеты.
    Используйте фильтры в боковой панели для удобной навигации.
    </div>
""", unsafe_allow_html=True)


# Индикатор загрузки с анимацией
@st.fragment
def show_loading():
    with st.empty():
        progress_bar = st.progress(0)
        status_text = st.empty()

        for i in range(1, 101):
            progress_bar.progress(i)
            status_text.text(f"Загрузка данных... {i}%")
            sleep(0.02)

        progress_bar.empty()
        status_text.success("✅ Данные успешно загружены!")
        sleep(1)
        status_text.empty()


# Получение данных с обработкой ошибок
@st.cache_data(ttl=60, show_spinner=False)
def fetch_reports(limit=100, offset=0):
    url = f"{st.secrets['api_url']}/ads/reports/paginate?limit={limit}&offset={offset}"
    try:
        with st.spinner("⌛ Получаем данные с сервера..."):
            response = requests.get(
                url,
                headers={
                    "accept": "application/json",
                    "Cookie": f"ads_analyzer={st.session_state.get('token', '')}"
                },
                timeout=15
            )

        if response.status_code == 200:
            return response.json()
        elif response.status_code == 401:
            st.error("⚠️ Ошибка авторизации. Пожалуйста, войдите снова.")
            return []
        else:
            st.error(f"⚠️ Ошибка сервера: {response.status_code} - {response.text}")
            return []
    except requests.exceptions.RequestException as e:
        st.error(f"⚠️ Ошибка соединения: {str(e)}")
        return []


# Фильтры в боковой панели с улучшенной организацией
with st.sidebar:
    st.header("🔍 Фильтры и настройки")

    with st.expander("📌 Фильтры отчетов", expanded=True):
        status_filter = st.selectbox(
            "Статус отчета",
            ["Все", "Готов", "В обработке"],
            help="Фильтрация отчетов по статусу обработки"
        )

        company_id_filter = st.text_input(
            "ID компании",
            placeholder="Введите ID компании",
            help="Поиск отчетов по конкретной компании"
        )

        date_filter = st.date_input(
            "Период создания",
            [],
            help="Фильтр по дате создания отчета"
        )

    st.divider()

    with st.expander("📊 Статистика", expanded=True):
        if st.button("🔄 Обновить данные", use_container_width=True, help="Обновить данные с сервера"):
            st.cache_data.clear()
            st.rerun()

        if 'reports' in locals():
            total_reports = len(reports)
            ready_reports = sum(1 for r in reports if r['is_ready'])

            st.metric("Всего отчетов", total_reports)
            st.metric("Готово",
                      f"{ready_reports} ({ready_reports / total_reports * 100:.0f}%)" if total_reports else "0")
            st.progress(ready_reports / total_reports if total_reports else 0)

# Загрузка данных с визуальной обратной связью
if 'reports' not in st.session_state or st.sidebar.button("Обновить данные"):
    reports = fetch_reports()
    if reports:
        show_loading()
        st.session_state.reports = reports

reports = st.session_state.get('reports', [])

# Основное отображение с карточками отчетов
if reports:
    # Применение фильтров
    filtered_reports = reports.copy()

    if status_filter != "Все":
        filtered_reports = [
            r for r in filtered_reports if
            (r['is_ready'] and status_filter == "Готов") or
            (not r['is_ready'] and status_filter == "В обработке")
        ]

    if company_id_filter:
        filtered_reports = [r for r in filtered_reports if company_id_filter.lower() in str(r['company_id']).lower()]

    # Статистика по фильтрованным отчетам
    if filtered_reports:
        ready_count = sum(1 for r in filtered_reports if r['is_ready'])
        total_count = len(filtered_reports)

        st.subheader("📈 Общая статистика")
        cols = st.columns(4)
        cols[0].metric("Найдено отчетов", total_count)
        cols[1].metric("Готово", ready_count)
        cols[2].metric("В работе", total_count - ready_count)
        cols[3].metric("Прогресс", f"{ready_count / total_count * 100:.0f}%" if total_count else "0%")

        with cols[3]:
            st.progress(ready_count / total_count if total_count else 0)

        st.divider()
        st.subheader("📋 Список отчетов")

        # Отображение каждого отчета в виде карточки
        for report in filtered_reports:
            status_label = "Готов" if report['is_ready'] else "В обработке"
            status_class = "ready" if report['is_ready'] else "processing"
            badge_class = "badge-ready" if report['is_ready'] else "badge-processing"

            # Форматирование даты
            created_at = datetime.fromisoformat(report.get('created_at', '')).strftime("%d.%m.%Y %H:%M") if report.get(
                'created_at') else "Не указано"

            with st.container():
                st.markdown(f"""
                    <div class="report-card status-{status_class}">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <h3 style="margin: 0;">Отчет #{report['id']}</h3>
                            <span class="badge {badge_class}">{status_label}</span>
                        </div>
                        <div style="margin: 0.5em 0; color: #666;">Создан: {created_at}</div>
                        <div style="display: flex; gap: 2em; margin-top: 1em;">
                            <div>
                                <strong>Компания:</strong> {report['company_id']}<br>
                                <strong>Пользователь:</strong> {report['user_email']}
                            </div>
                            <div>
                                <strong>Статус:</strong> {report['info'] or 'Нет информации'}
                            </div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)

                # Детали отчета в раскрывающемся блоке
                with st.expander("🔍 Показать детали", expanded=False):
                    col1, col2 = st.columns([1, 1.5])

                    with col1:
                        st.markdown("**📌 Основная информация**")
                        st.markdown(f"""
                            - **ID отчета:** `{report['id']}`
                            - **Компания:** `{report['company_id']}`
                            - **Статус:** `{status_label}`
                            - **Создан:** `{created_at}`
                            - **Пользователь:** `{report['user_email']}`
                        """)

                    with col2:
                        st.markdown("**🔍 Неэффективные сегменты**")
                        try:
                            bad_segments = json.loads(report['bad_segments'])
                            if isinstance(bad_segments, dict):
                                for key, value in bad_segments.items():
                                    st.warning(f"**Кластер {key}:** {value}")
                            else:
                                st.warning(f"**Проблемные сегменты:** {bad_segments}")
                        except:
                            st.warning(f"**Проблемные сегменты:** {report['bad_segments']}")

                    if report['is_ready']:
                        st.divider()
                        if st.button(
                            "📊 Просмотреть полный отчет",
                            key=f"view_{report['id']}",
                            help="Открыть детализированный отчет с графиками и анализом",
                            on_click=lambda r=report: st.session_state.update({
                                "last_report_id": r['id'],
                                "last_company_id": r['company_id']
                            })):
                            st.session_state["last_report_id"] = report['id']
                            st.page_link("pages/📈_statistic.py")

                st.divider()
    else:
        st.warning("🚫 Нет отчетов, соответствующих выбранным фильтрам")
        st.image("https://cdn-icons-png.flaticon.com/512/4076/4076478.png", width=150)
else:
    # Пустое состояние с подсказками
    st.markdown("""
        <div style="text-align: center; padding: 3em; color: #666;">
            <img src="https://cdn-icons-png.flaticon.com/512/4076/4076478.png" width="150" style="margin-bottom: 1em;">
            <h3>У вас пока нет запросов на анализ</h3>
            <p>Начните с создания нового анализа рекламных кампаний</p>
            <button class="stButton" style="margin-top: 1em;">Создать новый анализ</button>
        </div>
    """, unsafe_allow_html=True)