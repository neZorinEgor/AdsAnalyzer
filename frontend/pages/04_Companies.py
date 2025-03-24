import streamlit as st
import requests
import pandas as pd

# Заголовок страницы
st.title("Мои компании")

# Словарь для перевода типов кампаний
company_types = {
    "TEXT_CAMPAIGN": "Текстово-графические объявления",
    "UNIFIED_CAMPAIGN": "Единая перфоманс кампания",
    "SMART_CAMPAIGN": "Смарт-баннеры"
}


# Функция для получения данных с API
@st.cache_data(persist="disk")
def fetch_ads_data():
    url = "http://127.0.0.1:8000/ads/companies"
    headers = {
        "accept": "application/json",
        "Cookie": "ads_analyzer=y0__xD-15LEBhiOgjYgu53kyhLbssECE76XIqKImMH2ph83nit1Cw"
    }
    response = requests.post(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Ошибка при получении данных: {response.status_code}")
        return None


# Получение данных
data = fetch_ads_data()

if data:
    # Отрисовка данных для каждой кампании
    for campaign in data:
        st.write(f"### {campaign.get('Name')}")
        # ID кампании
        st.caption(f"{campaign.get('Id')}")
        # Тип кампании
        campaign_type = campaign.get("Type")
        st.write(f"**Тип кампании:** {company_types.get(campaign_type, 'Неизвестный тип')}")

        # Бюджет и расходы
        funds = campaign.get("Funds", {})
        shared_funds = funds.get("SharedAccountFunds", {})
        st.write(f"**Расходы:** {shared_funds.get('Spend', 0) / 1000000:.2f} руб.")
        # Ежедневный бюджет
        daily_budget = campaign.get("DailyBudget", {})
        if daily_budget:
            st.write(
                f"**Ежедневный бюджет:** {daily_budget.get('Amount', 0) / 1000000:.2f} руб. ({daily_budget.get('Mode', 'Неизвестно')})")
        else:
            st.write("**Ежедневный бюджет:** Не установлен")

        # Стратегия ставок
        bidding_strategy = campaign.get("TextCampaign", {}).get("BiddingStrategy", {})
        if bidding_strategy:
            search_strategy = bidding_strategy.get("Search", {})
            network_strategy = bidding_strategy.get("Network", {})

            st.write("**Стратегия ставок (Поиск):**")
            st.write(f"- Тип: {search_strategy.get('BiddingStrategyType', 'Неизвестно')}")
            st.write(f"- Размещение: Поиск: {search_strategy.get('PlacementTypes', {}).get('SearchResults', 'Нет')}, "
                     f"Галерея: {search_strategy.get('PlacementTypes', {}).get('ProductGallery', 'Нет')}, "
                     f"Динамические места: {search_strategy.get('PlacementTypes', {}).get('DynamicPlaces', 'Нет')}")

            st.write("**Стратегия ставок (Сеть):**")
            st.write(f"- Тип: {network_strategy.get('BiddingStrategyType', 'Неизвестно')}")
            if network_strategy.get("BiddingStrategyType") == "WB_MAXIMUM_CLICKS":
                wb_max_clicks = network_strategy.get("WbMaximumClicks", {})
                st.write(f"- Лимит расходов в неделю: {wb_max_clicks.get('WeeklySpendLimit', 0) / 1000000:.2f} руб.")
                st.write(f"- Тип бюджета: {wb_max_clicks.get('BudgetType', 'Неизвестно')}")

        # Счетчики
        counter_ids = campaign.get("TextCampaign", {}).get("CounterIds", {}).get("Items", [])

        # Разделитель между кампаниями
        st.divider()
