import streamlit as st
import requests
from datetime import datetime

# Настройки страницы
st.set_page_config(layout="wide", page_title="Рекламные кампании", page_icon="📊")
st.title("📊 Мои рекламные кампании")

# Стили CSS для улучшения внешнего вида
st.markdown("""
    <style>
        .campaign-card {
            border-radius: 10px;
            padding: 1.5rem;
            margin-bottom: 1rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            transition: transform 0.2s;
            background-color: white;
        }
        .campaign-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
        }
        .metric-card {
            border-radius: 10px;
            padding: 1rem;
            background-color: #f8f9fa;
        }
        .header {
            color: #2c3e50;
        }
        .positive {
            color: #27ae60;
        }
        .negative {
            color: #e74c3c;
        }
        .stButton>button {
            border-radius: 8px;
            padding: 0.5rem 1rem;
        }
    </style>
""", unsafe_allow_html=True)

# Словарь типов кампаний с иконками
company_types = {
    "TEXT_CAMPAIGN": ("📝 Текстово-графические", "#3498db"),
    "UNIFIED_CAMPAIGN": ("🚀 Перфоманс", "#9b59b6"),
    "SMART_CAMPAIGN": ("🧠 Смарт-баннеры", "#e67e22"),
    "DYNAMIC_CAMPAIGN": ("🔄 Динамические", "#1abc9c"),
    "MOBILE_CAMPAIGN": ("📱 Мобильные", "#2ecc71")
}


# Получение данных
@st.cache_data(ttl=300)  # Кэшируем на 5 минут
def get_data():
    print(st.session_state['token'])
    try:
        response = requests.post(
            "http://127.0.0.1:8000/ads/companies",
            headers={
                "accept": "application/json",
                "Cookie": f"ads_analyzer={st.session_state['token']}"
            },
            timeout=10
        )
        if response.status_code == 200:
            return response.json()["result"]["Campaigns"]
        st.error(f"Ошибка сервера: {response.status_code}")
        return None
    except Exception as e:
        st.error(f"Ошибка подключения: {str(e)}")
        return None


data = get_data()

# Фильтры в сайдбаре
with st.sidebar:
    st.subheader("🔍 Фильтры")

    # Поиск по названию
    search_query = st.text_input("Поиск по названию", "")

    # Выбор типа кампании
    type_filter = st.multiselect(
        "Тип кампании",
        options=[v[0] for v in company_types.values()],
        default=[v[0] for v in company_types.values()],
        key="type_filter"
    )

    # Фильтр по бюджету
    st.write("**Фильтр по расходам**")
    min_spend, max_spend = st.slider(
        "Диапазон расходов (руб)",
        min_value=0,
        max_value=10000000,
        value=(0, 10000000),
        step=1000,
        format="%d руб",
        label_visibility="collapsed"
    )

    # Сортировка
    sort_option = st.selectbox(
        "Сортировка",
        options=["По названию (А-Я)", "По названию (Я-А)", "По расходам (↑)", "По расходам (↓)", "По ID"],
        index=0
    )

# Отображение данных
if not data:
    st.warning("Данные не загружены. Проверьте подключение к серверу.")
else:
    # Общая статистика
    total = len(data)
    total_spend = sum(c.get("Funds", {}).get("SharedAccountFunds", {}).get("Spend", 0) / 1000000 for c in data)
    avg_spend = total_spend / total if total > 0 else 0

    # Создаем колонки для метрик
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
            <div class="metric-card">
                <h3>Всего кампаний</h3>
                <h2>{total}</h2>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
            <div class="metric-card">
                <h3>Общие расходы</h3>
                <h2>{total_spend:,.2f} ₽</h2>
            </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
            <div class="metric-card">
                <h3>Средние расходы</h3>
                <h2>{avg_spend:,.2f} ₽</h2>
            </div>
        """, unsafe_allow_html=True)

    st.divider()

    # Обработка и сортировка данных
    processed_data = []
    for campaign in data:
        camp_type = campaign.get("Type")
        type_name, type_color = company_types.get(camp_type, (f"❓ {camp_type}", "#95a5a6"))
        spend = campaign.get("Funds", {}).get("SharedAccountFunds", {}).get("Spend", 0) / 1000000
        refund = campaign.get("Funds", {}).get("SharedAccountFunds", {}).get("Refund", 0) / 1000000
        net_spend = spend - refund

        processed_data.append({
            "id": campaign.get("Id"),
            "name": campaign.get("Name"),
            "type": type_name,
            "type_color": type_color,
            "spend": spend,
            "refund": refund,
            "net_spend": net_spend,
            "status": campaign.get("Status", "—"),
            "daily_budget": campaign.get("DailyBudget", {}).get("Amount", 0) / 1000000 if campaign.get(
                "DailyBudget") else 0,
            "strategy": campaign.get("TextCampaign", {}).get("BiddingStrategy", {}),
            "counter_ids": campaign.get("TextCampaign", {}).get("CounterIds", {}).get("Items", [])
        })

    # Применяем фильтры
    filtered_data = [
        c for c in processed_data
        if (search_query.lower() in c["name"].lower()) and
           (c["type"] in type_filter) and
           (min_spend <= c["spend"] <= max_spend)
    ]

    # Применяем сортировку
    if sort_option == "По названию (А-Я)":
        filtered_data.sort(key=lambda x: x["name"])
    elif sort_option == "По названию (Я-А)":
        filtered_data.sort(key=lambda x: x["name"], reverse=True)
    elif sort_option == "По расходам (↑)":
        filtered_data.sort(key=lambda x: x["spend"])
    elif sort_option == "По расходам (↓)":
        filtered_data.sort(key=lambda x: x["spend"], reverse=True)
    elif sort_option == "По ID":
        filtered_data.sort(key=lambda x: x["id"])

    # Показываем количество найденных кампаний
    st.markdown(f"**Найдено кампаний:** {len(filtered_data)}")

    # Отображаем карточки кампаний
    for campaign in filtered_data:
        with st.container():
            st.markdown(f"""
                <div class="campaign-card" style="border-left: 5px solid {campaign['type_color']}">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <h3 style="margin: 0; color: #2c3e50;">{campaign['name']}</h3>
                        <span style="background-color: {campaign['type_color']}; color: white; padding: 0.2rem 0.5rem; border-radius: 12px; font-size: 0.8rem;">
                            {campaign['type']}
                        </span>
                    </div>
                    <div style="margin-top: 0.5rem; color: #7f8c8d; font-size: 0.9rem;">ID: {campaign['id']} | Статус: {campaign['status']}</div>
                </div>
            """, unsafe_allow_html=True)

            # Основная информация о кампании
            col1, col2, col3 = st.columns([2, 2, 1])

            with col1:
                st.markdown("**Финансы**")
                st.markdown(f"""
                    - Общие расходы: <span style="font-weight: bold;">{campaign['spend']:,.2f} ₽</span>
                    - Возвраты: <span class="negative">{campaign['refund']:,.2f} ₽</span>
                    - Чистые расходы: <span class="positive">{campaign['net_spend']:,.2f} ₽</span>
                """, unsafe_allow_html=True)

                if campaign['daily_budget'] > 0:
                    st.markdown(f"**Дневной бюджет:** {campaign['daily_budget']:,.2f} ₽")

            with col2:
                st.markdown("**Счетчики**")
                if campaign['counter_ids']:
                    for counter_id in campaign['counter_ids']:
                        st.markdown(f"- `{counter_id}`")
                else:
                    st.markdown("Нет подключенных счетчиков")

            with col3:
                if st.button("📊 Анализ", key=f"analyze_{campaign['id']}"):
                    with st.spinner("Создание отчета..."):
                        try:
                            response = requests.post(
                                url=f"http://127.0.0.1:8000/ads/report/create?company_id={campaign['id']}",
                                headers={
                                    "accept": "application/json",
                                    "Cookie": f"ads_analyzer={st.session_state['token']}"
                                },
                                timeout=15
                            )
                            if response.status_code == 200:
                                st.success("Отчет поступил в очередь на обработку")
                            else:
                                st.error(f"Ошибка: {response.status_code}")
                        except Exception as e:
                            st.error(f"Ошибка при создании отчета: {str(e)}")

            # Детали стратегии (раскрывающийся блок)
            with st.expander("🔍 Подробнее о стратегии"):
                if campaign['strategy']:
                    st.json(campaign['strategy'])
                else:
                    st.info("Информация о стратегии отсутствует")

            st.divider()
