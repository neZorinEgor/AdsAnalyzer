import streamlit as st
import requests
from time import sleep

# Настройка стиля страницы
st.set_page_config(
    page_title="Аутентификация",
    page_icon="🔒",
    layout="centered"
)

# Скрываем технические детали в query params
if "code" in st.query_params:
    code = st.query_params["code"]

    # Основной контейнер для аутентификации
    with st.container():
        st.title("🔒 Вход в систему")

        # Индикатор прогресса с более дружелюбным сообщением
        progress_bar = st.progress(0)
        status_text = st.empty()

        # Имитация процесса аутентификации
        for percent in range(0, 101, 20):
            sleep(0.3)
            progress_bar.progress(percent)
            status_text.text(f"Проверка ваших данных... {percent}%")

        try:
            response = requests.get(
                "http://127.0.0.1:8000/callback",
                params={"code": code},
                timeout=10
            )

            if response.status_code == 200:
                st.session_state["token"] = response.text

                # Успешная аутентификация - приятное сообщение
                sleep(0.5)
                progress_bar.empty()
                status_text.empty()

                st.balloons()
                st.success("Вход выполнен успешно!")
                st.markdown("""
                <div style="background:#f0f2f6;padding:20px;border-radius:10px;margin-top:20px">
                    <h3 style="color:#2e7d32">Добро пожаловать!</h3>
                    <p>Теперь вы можете использовать все возможности системы.</p>
                    <p style="font-size:0.9em;color:#666">Перенаправление на главную страницу...</p>
                </div>
                """, unsafe_allow_html=True)

                # Имитация перенаправления
                sleep(2)
                st.switch_page("pages/🏣_companies.py")

            else:
                raise Exception("Ошибка аутентификации")

        except Exception as e:
            progress_bar.empty()
            status_text.empty()
            print(str(e))
            st.error("Не удалось войти в систему")
            st.markdown("""
            <div style="background:#ffebee;padding:20px;border-radius:10px;margin-top:20px">
                <p>Пожалуйста, попробуйте снова или обратитесь в поддержку.</p>
            </div>
            """, unsafe_allow_html=True)

            if st.button("Попробовать ещё раз", type="primary"):
                st.rerun()

else:
    # Красивый экран ожидания
    with st.container():
        st.title("🔒 Авторизация")
        st.markdown("""
        <div style="background:#f0f2f6;padding:20px;border-radius:10px;margin-top:20px">
            <h3 style="color:#1976d2">Пожалуйста, подождите</h3>
            <p>Идёт процесс проверки ваших данных...</p>
        </div>
        """, unsafe_allow_html=True)

        # Анимация загрузки
        with st.spinner("Связываемся с сервером авторизации..."):
            sleep(3)

        # Если долго нет ответа
        if "code" not in st.query_params:
            st.warning("Процесс занимает больше времени, чем ожидалось")
            if st.button("Проверить снова", key="retry_check"):
                st.rerun()
