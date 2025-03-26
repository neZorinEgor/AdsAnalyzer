import streamlit as st
from datetime import datetime

# Настройка страницы
st.set_page_config(
    page_title="Домашний аналитик",
    page_icon="🏠",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Стили для уютного интерфейса
st.markdown("""
<style>
    .main {
        background-color: #f8f9fa;
        padding: 2rem;
    }
    .header {
        color: #2c3e50;
        padding-bottom: 1rem;
    }
    .sidebar .sidebar-content {
        background-color: #e9ecef;
    }
    .metric-card {
        background: white;
        border-radius: 10px;
        padding: 1rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    .stButton>button {
        background-color: #4a6fa5;
        color: white;
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# Сайдбар с навигацией
with st.sidebar:
    st.title("🍵 Меню")
    menu_choice = st.radio(
        "Разделы:",
        ["Главная", "Аналитика", "Настройки"],
        index=0
    )

    st.divider()
    st.caption(f"Сегодня: {datetime.now().strftime('%d.%m.%Y')}")
    st.caption("Версия 1.0")

# Главная страница
if menu_choice == "Главная":
    st.title("🏠 Добро пожаловать домой!")
    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        ### Ваши данные:
        Здесь вы можете быстро посмотреть основные метрики 
        и перейти к анализу.
        """)

    with col2:
        st.markdown("""
        ### Быстрые действия:
        - Обновить данные
        - Создать отчет
        - Проверить статус
        """)

    st.markdown("---")

    # Карточки с метриками
    st.subheader("📊 Краткая статистика")
    col1, col2, col3 = st.columns(3)
    with col1:
        with st.container(border=True):
            st.metric("Всего кампаний", "23", "+2 за неделю")
    with col2:
        with st.container(border=True):
            st.metric("Средний CTR", "3.2%", "-0.1%")
    with col3:
        with st.container(border=True):
            st.metric("Общий бюджет", "124,500 ₽", "12%")

    # Секция с последними действиями
    st.markdown("---")
    st.subheader("🕒 Последние события")
    with st.container(border=True):
        st.write("🔹 Сегодня в 09:30 - Обновлены данные кампаний")
        st.write("🔹 Вчера в 18:15 - Создан отчет за апрель")
        st.write("🔹 12.05 в 14:00 - Изменен бюджет кампании #1452")

# Другие страницы (заглушки)
elif menu_choice == "Аналитика":
    st.title("📈 Аналитика")
    st.write("Раздел в разработке...")

elif menu_choice == "Настройки":
    st.title("⚙️ Настройки")
    with st.expander("Токен доступа"):
        st.code(f"Токен: {st.secrets['token']}", language="text")
    st.write("Другие настройки будут доступны позже")

# Подвал
st.markdown("---")
st.caption("© 2024 AdsAnalyzer | С любовью к данным")
