import pandas as pd 
import streamlit as st 
import plotly.express as px
import plotly.figure_factory as ff

st.set_page_config(layout='wide',
                  page_title='Shopping Cart Dashboard 🛍️',
                  page_icon='🛒'
                  )

tap1, tap2 = st.tabs(['📈 Descriptive Stats', '📊 Charts'])
df = pd.read_csv('shopping_cart.csv')


num = df.describe()
cat = df.describe(include='O')

# with tap1:

with tap1:
    x = st.sidebar.checkbox('Show Data', False, key=1)
    
    if x:
        st.markdown('<h3 style="text-align: center; color: LightBlue;">Dataset</h3>',
            unsafe_allow_html=True)
        st.dataframe(df.head(100), width=2000)
    
    col1, col2, col3 = st.columns([6, 0.5, 6])
    with col1:
        st.subheader('Numerical Descriptive Statistics')
        st.dataframe(num.T, height=150)

    with col3:
        st.subheader('Categorical Descriptive Statistics')
        st.dataframe(cat.T, height=200)

with tap2:

    gender = st.sidebar.selectbox('Select Gender', df['gender'].unique())
    state = st.sidebar.multiselect('Select state', df['state'].unique())
    category = st.sidebar.multiselect('Select Category', df['category'].unique())

    
    filtered_df = df[
        (df['gender'] == gender) &
        (df['state'].isin(state) if state else True) &
        (df['category'].isin(category)if category else True  )
    ]

    col1, col2, col3 = st.columns([5, 1, 5])

    with col1:
        fig1 =px.bar(df, x="order_month", y="total_price", title="Total price per month".title(),color='category')
        
        st.plotly_chart(fig1, use_container_width=True)

        fig2 = px.strip(
            filtered_df, x='order_date', y='total_price', color='category',
            title="Sales Over Time".title()
        )
        st.plotly_chart(fig2, use_container_width=True)

        fig3=px.box(filtered_df,x='order_year',y='total_price',color='category',
                   title=' Box Plot of  orders year'.title()
                   )
        st.plotly_chart(fig3, use_container_width=True)
    with col3:
        fig4 = px.pie(
            filtered_df, names='category', values='total_price',
            title="Sales Distribution by Category".title()
        )
        st.plotly_chart(fig4, use_container_width=True)

        fig5 = px.histogram(
            filtered_df, x='delivery_day_name', color='category',
            title="Delivery Day Distribution by Category".title(),
            barmode='group'
        )
        st.plotly_chart(fig5, use_container_width=True)
        
        fig6=ff.create_distplot([filtered_df['order_month'].tolist()],['All orders of months in 2021']
                            )
        st.plotly_chart(fig6, use_container_width=True)
