import os
import sqlite3
import webbrowser
import streamlit as st
from yandexid import YandexOAuth, YandexID

from settings import settings

# Инициализация YandexOAuth
yandex_oauth = YandexOAuth(
    client_id=settings.CLIENT_ID,
    client_secret=settings.CLIENT_SECRET,
    redirect_uri=settings.REDIRECT_URI
)
# Подключение к базе данных SQLite
conn = sqlite3.connect("./sqlite/users.db", check_same_thread=False)
cursor = conn.cursor()

# Создание таблицы, если она не существует
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id TEXT PRIMARY KEY,
    token TEXT,
    username TEXT,
    email TEXT
)
""")
conn.commit()


# Функция для открытия страницы авторизации Яндекс
def open_yandex_page_with_token():
    webbrowser.open(yandex_oauth.get_authorization_url())


# Функция для сохранения данных пользователя в базу данных
def save_user_data(user_id, token, username, email):
    cursor.execute("""
    INSERT OR REPLACE INTO users (user_id, token, username, email)
    VALUES (?, ?, ?, ?)
    """, (user_id, token, username, email))
    conn.commit()


# Функция для получения данных пользователя из базы данных
def get_user_data(user_id):
    cursor.execute("SELECT token, username, email FROM users WHERE user_id = ?", (user_id,))
    return cursor.fetchone()


# Инициализация session_state
if "user_id" not in st.session_state:
    st.session_state.user_id = "user123"
if "token" not in st.session_state:
    st.session_state.token = None
if "username" not in st.session_state:
    st.session_state.username = None
if "email" not in st.session_state:
    st.session_state.email = None

# Проверка, есть ли данные пользователя в базе данных
user_data = get_user_data(st.session_state.user_id)
if user_data:
    st.session_state.token, st.session_state.username, st.session_state.email = user_data

print(get_user_data(st.session_state.user_id))

# Основной интерфейс
st.write("# 📰 AdsCompanyAnalyzer")
st.divider()

# Если токен не установлен
if not st.session_state.token:
    st.button("Get Yandex OAuth-token", on_click=open_yandex_page_with_token)
    secret = st.text_input("Введите секретный код:")

    if secret:
        try:
            # Получение токена по коду
            token = yandex_oauth.get_token_from_code(secret).access_token
            yandex_id = YandexID(token)
            user_payload = yandex_id.get_user_info_json()

            # Сохранение данных в session_state и базе данных
            st.session_state.token = token
            st.session_state.username = user_payload.first_name
            st.session_state.email = user_payload.default_email
            save_user_data(st.session_state.user_id, token, user_payload.first_name, user_payload.default_email)

            st.success("Авторизация успешна!")
        except Exception as e:
            st.error(f"Ошибка при получении токена: {e}")
else:
    # Если токен установлен, показываем данные пользователя
    st.write(f"👤 Имя пользователя: **{st.session_state.username}**")
    st.write(f"📧 Почта: **{st.session_state.email}**")

# Ссылка на другую страницу
st.page_link("pages/1_📈_Analyzer.py", label="Проанализировать компанию", icon="📈")
