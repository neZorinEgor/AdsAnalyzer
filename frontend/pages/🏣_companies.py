import streamlit as st
import requests

# Настройки страницы
st.set_page_config(layout="wide", page_title="Рекламные кампании", page_icon="🏣")
st.title("Мои рекламные кампании")

# Словарь типов кампаний
company_types = {
    "TEXT_CAMPAIGN": "Текстово-графические",
    "UNIFIED_CAMPAIGN": "Перфоманс",
    "SMART_CAMPAIGN": "Смарт-баннеры"
}


# Получение данных
@st.cache_data
def get_data():
    try:
        response = requests.post(
            "http://127.0.0.1:8000/ads/companies",
            headers={
                "accept": "application/json",
                "Cookie": f"ads_analyzer={st.session_state["token"]}"
            }
        )
        return response.json()["result"]["Campaigns"] if response.status_code == 200 else None
    except Exception as e:
        return None


data = get_data()


# Фильтры в сайдбаре
with st.sidebar:
    st.subheader("Фильтры")

    # Выбор типа кампании
    type_filter = st.multiselect(
        "Тип кампании",
        options=list(company_types.values()),
        default=list(company_types.values())
    )

    # Фильтр по бюджету
    budget_filter = st.slider(
        "Диапазон расходов (руб)",
        min_value=-10000000,
        max_value=10000000,
        value=(-10000000, 10000000),
        step=1000
    )

# Отображение данных
if not data:
    st.warning("Данные не загружены")
else:
    # Общая статистика
    total = len(data)
    total_spend = sum(c.get("Funds", {}).get("SharedAccountFunds", {}).get("Spend", 0) / 1000000 for c in data)

    col1, col2 = st.columns(2)
    col1.metric("Всего кампаний", total)
    col2.metric("Общие расходы", f"{total_spend:,.2f} руб")

    st.divider()

    # Список кампаний
    for campaign in data:
        # Применяем фильтры
        camp_type = company_types.get(campaign.get("Type"), "Другой")
        spend = campaign.get("Funds", {}).get("SharedAccountFunds", {}).get("Spend", 0) / 1000000

        if camp_type not in type_filter:
            continue
        if not (budget_filter[0] <= spend <= budget_filter[1]):
            continue

        # Отображаем карточку кампании
        with st.expander(f"{campaign.get('Name')} (ID: {campaign.get('Id')})"):
            col1, col2 = st.columns(2)

            with col1:
                st.write(f"**Тип:** {camp_type}")
                st.write(f"**Статус:** {campaign.get('Status', '—')}")

            with col2:
                st.write(f"**Расходы:** {spend:,.2f} руб")
                daily = campaign.get("DailyBudget", {})
                if daily:
                    st.write(f"**Бюджет:** {daily.get('Amount', 0) / 1000000:,.2f} руб/день")

            # Детали стратегии
            strategy = campaign.get("TextCampaign", {}).get("BiddingStrategy", {})
            if strategy:
                st.write("**Стратегия ставок:**")
                st.json(strategy)  # Просто показываем сырые данные для простоты
            if st.button("Проанализировать", key=campaign.get('Id')):
                response = requests.post(
                    url=f"http://127.0.0.1:8000/ads/report/create?company_id={campaign.get('Id')}",
                    headers={
                        "accept": "application/json",
                        "Cookie": f"ads_analyzer={st.session_state['token']}"
                    }
                )
                st.success(response.status_code)
