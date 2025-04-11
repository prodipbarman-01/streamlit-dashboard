import streamlit as st
import pandas as pd
import plotly.express as px

st.title("📊 Cleaned Data Dashboard")

# File uploader
uploaded_file = st.file_uploader("Upload your cleaned CSV file", type=["csv"])

if uploaded_file is not None:
    try:
        # Read the CSV file
        df = pd.read_csv(uploaded_file)
        st.success("✅ File uploaded successfully!")

        # Preview the dataset
        st.subheader("📄 Data Preview")
        st.dataframe(df)

        # ==================== FILTER SECTION ====================
        st.subheader("🔍 Filter Data")

        # Filter by City
        if 'City' in df.columns:
            selected_city = st.selectbox("Filter by City", df['City'].unique())
            df = df[df['City'] == selected_city]

        # Filter by Amount (numeric)
        if 'Amount' in df.columns:
            amount_min = int(df['Amount'].min())
            amount_max = int(df['Amount'].max())
            selected_amount = st.slider("Select Amount Range", amount_min, amount_max, (amount_min, amount_max))
            df = df[(df['Amount'] >= selected_amount[0]) & (df['Amount'] <= selected_amount[1])]

        # Sorting
        sort_col = st.selectbox("Sort by column", df.columns)
        sort_order = st.radio("Sort order", ['Ascending', 'Descending'])
        df = df.sort_values(by=sort_col, ascending=(sort_order == 'Ascending'))

        # Show filtered data
        st.subheader("📊 Filtered & Sorted Data")
        st.dataframe(df)

        # ==================== DOWNLOAD ====================
        st.subheader("⬇️ Download Filtered Data")
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download as CSV",
            data=csv,
            file_name='filtered_data.csv',
            mime='text/csv',
        )

        # ==================== VISUALIZATIONS ====================
        st.subheader("📈 Visualizations")

        # Bar Chart: Orders per City
        if 'City' in df.columns:
            city_counts = df['City'].value_counts().reset_index()
            city_counts.columns = ['City', 'Count']
            fig_city = px.bar(city_counts, x='City', y='Count', title='Number of Orders per City')
            st.plotly_chart(fig_city)

        # Pie Chart: Product distribution
        if 'Product' in df.columns:
            product_counts = df['Product'].value_counts().reset_index()
            product_counts.columns = ['Product', 'Count']
            fig_product = px.pie(product_counts, names='Product', values='Count', title='Product Distribution')
            st.plotly_chart(fig_product)

        # Line Chart: Order Amount over Time
        if 'Order Date' in df.columns and 'Amount' in df.columns:
            df['Order Date'] = pd.to_datetime(df['Order Date'], errors='coerce')
            df_sorted = df.sort_values('Order Date')
            fig_line = px.line(df_sorted, x='Order Date', y='Amount', title='Order Amount Over Time')
            st.plotly_chart(fig_line)

    except Exception as e:
        st.error(f"❌ Failed to process the file: {e}")

else:
    st.info("⬆️ Please upload a CSV file to get started.")
