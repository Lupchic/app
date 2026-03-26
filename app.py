import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("📊 Дашборд судових справ")

uploaded_file = st.file_uploader("Завантаж CSV файл", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.write("### 🔍 Дані")
    st.dataframe(df)

    # 🔹 Перевірка колонок
    required_cols = ["region", "category", "date"]
    if not all(col in df.columns for col in required_cols):
        st.error(f"CSV має містити колонки: {required_cols}")
    else:
        # 🔹 Перетворення дати
        df["date"] = pd.to_datetime(df["date"])
        df["year"] = df["date"].dt.year

        # 🔹 ФІЛЬТРИ
        st.sidebar.header("Фільтри")

        regions = st.sidebar.multiselect(
            "Оберіть регіон",
            options=df["region"].unique(),
            default=df["region"].unique()
        )

        categories = st.sidebar.multiselect(
            "Оберіть категорію",
            options=df["category"].unique(),
            default=df["category"].unique()
        )

        date_range = st.sidebar.date_input(
            "Діапазон дат",
            [df["date"].min(), df["date"].max()]
        )

        # 🔹 Фільтрація
        filtered_df = df[
            (df["region"].isin(regions)) &
            (df["category"].isin(categories)) &
            (df["date"] >= pd.to_datetime(date_range[0])) &
            (df["date"] <= pd.to_datetime(date_range[1]))
        ]

        st.write("### 📌 Відфільтровані дані")
        st.dataframe(filtered_df)

        # 🔹 ДІАГРАМА (кількість справ за категоріями)
        st.write("### 📊 Кількість справ за категоріями")

        category_counts = filtered_df["category"].value_counts()

        fig1, ax1 = plt.subplots()
        ax1.bar(category_counts.index, category_counts.values)
        ax1.set_xlabel("Категорія")
        ax1.set_ylabel("Кількість справ")
        ax1.set_title("Справи за категоріями")

        st.pyplot(fig1)

        # 🔹 АНАЛІЗ ТРЕНДІВ ПО РОКАХ
        st.write("### 📈 Тренди по роках")

        yearly_trend = filtered_df.groupby("year").size()

        fig2, ax2 = plt.subplots()
        ax2.plot(yearly_trend.index, yearly_trend.values, marker='o')
        ax2.set_xlabel("Рік")
        ax2.set_ylabel("Кількість справ")
        ax2.set_title("Динаміка по роках")

        st.pyplot(fig2)

else:
    st.info("⬆️ Завантаж CSV файл для початку")