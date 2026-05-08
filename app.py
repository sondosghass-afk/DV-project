import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.express as px

# قراءة البيانات
df = pd.read_csv("retail_store_sales.csv")
print(df.columns)
# إنشاء التطبيق
app = Dash(__name__)
server = app.server

# تصميم الصفحة
app.layout = html.Div([

    html.H1("Retail Store Sales Dashboard"),

    dcc.Dropdown(
        id='category-dropdown',
        options=[
            {'label': cat, 'value': cat}
            for cat in df['Category'].unique()
        ],
        value=df['Category'].unique()[0],
        clearable=False
    ),

    dcc.Graph(id='line-chart'),

    dcc.Graph(id='scatter-chart')

])

df['Transaction Date'] = pd.to_datetime(
    df['Transaction Date'],
    dayfirst=True
)

monthly_sales = df.groupby(
    df['Transaction Date'].dt.to_period('M')
)['Total Spent'].sum().reset_index()

monthly_sales['Transaction Date'] = monthly_sales['Transaction Date'].astype(str)

# Callback
@app.callback(
    [Output('line-chart', 'figure'),
     Output('scatter-chart', 'figure')],
    [Input('category-dropdown', 'value')]
)

def update_graphs(selected_category):

    filtered_df = df[df['Category'] == selected_category]

    # تجميع شهري
    filtered_monthly = filtered_df.groupby(
        filtered_df['Transaction Date'].dt.to_period('M')
    )['Total Spent'].sum().reset_index()

    filtered_monthly['Transaction Date'] = filtered_monthly['Transaction Date'].astype(str)

    # Line Chart
    line_fig = px.line(
        filtered_monthly,
        x='Transaction Date',
        y='Total Spent',
        title='Monthly Revenue Trend',
        markers=True
    )

    # Scatter Plot
    scatter_fig = px.scatter(
        filtered_df,
        x='Price Per Unit',
        y='Total Spent',
        color='Payment Method',
        hover_data=['Quantity']
    )

    return line_fig, scatter_fig

# تشغيل التطبيق
if __name__ == '__main__':
    app.run(debug=True)
