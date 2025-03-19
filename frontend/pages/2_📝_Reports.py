import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(
    page_title="Reports",
    page_icon="📝",
)

# Пример данных
data = {
    "Итерация": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    "WCSS": [100, 80, 60, 45, 35, 25, 20, 15, 12, 10],  # Пример значений WCSS
    "Время обучения (сек)": [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0],  # Пример времени обучения
}
df = pd.DataFrame(data)

# Оптимальное количество кластеров (для примера)
optimal_num_cluster = 4

# Создание графика с двумя осями Y
fig = go.Figure()

# Добавление линии для WCSS
fig.add_trace(
    go.Scatter(
        x=df["Итерация"],
        y=df["WCSS"],
        mode="lines+markers",
        name="WCSS",
        line=dict(color="blue"),
        yaxis="y1",
    )
)

# Добавление линии для времени выполнения
fig.add_trace(
    go.Scatter(
        x=df["Итерация"],
        y=df["Время обучения (сек)"],
        mode="lines+markers",
        name="Время обучения (сек)",
        line=dict(color="red", dash="dash"),
        yaxis="y2",
    )
)

# Добавление вертикальной линии для оптимального кластера
fig.add_shape(
    type="line",
    x0=optimal_num_cluster,
    x1=optimal_num_cluster,
    y0=0,
    y1=max(df["WCSS"]),
    line=dict(color="indianred", width=2, dash="dash"),
    name="Оптимальный кластер",
)

# Настройка осей
fig.update_layout(
    title="Выбор оптимального количества кластеров методом локтя",
    xaxis=dict(title="Количество кластеров"),
    yaxis=dict(title="WCSS", tickfont=dict(color="blue")),
    yaxis2=dict(
        title="Время обучения (сек)",
        tickfont=dict(color="red"),
        overlaying="y",
        side="right",
    ),
    legend=dict(x=0.1, y=1.1),
)

# Отображение графика в Streamlit
st.plotly_chart(fig)