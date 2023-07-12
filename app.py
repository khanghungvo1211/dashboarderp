import pandas as pd
import numpy as np
import streamlit as st
import matplotlib as mpl
import calendar

import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objs as go

from streamlit_option_menu import option_menu

import warnings
warnings.filterwarnings("ignore")

st.set_page_config(
    page_title="Sales Dashboard",
    page_icon=":bar_chart:",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------- Colors -----------
colors = {}
def colorFader(c1, c2, mix=0):
    c1 = np.array(mpl.colors.to_rgb(c1))
    c2 = np.array(mpl.colors.to_rgb(c2))
    return mpl.colors.to_hex((1 - mix) * c1 + mix * c2)

c1 = '#FAA831'
c2 = '#9A4800'
n = 9
for x in range(n + 1):
    colors['level' + str(n - x + 1)] = colorFader(c1, c2, x / n)
colors['background'] = '#232425'
colors['text'] = '#fff'

# --------- READ EXCEL --------
data = pd.read_csv('ldata.csv')

# ------ HEADER -------
with st.container():
    st.markdown('<div class="header">', unsafe_allow_html=True)
    st.markdown('<h1>Sales Dashboard</h1>', unsafe_allow_html=True)
    st.markdown('<h2>Explore Sales Insights</h2>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Apply custom CSS styles
st.markdown('<link href="style.css" rel="stylesheet">', unsafe_allow_html=True)

# -------- NAVBAR ------------

selected = option_menu(
    menu_title="Sales Dashboard",
    options=["Home", "Timely Sales", 'Filter'],
    icons=['building', 'calendar3', 'filter-circle-fill'],
    menu_icon="bar-chart-line-fill",
    default_index=0,
    orientation="horizontal",
    styles="text-align-center navbar"
)


# ---- SIDEBAR ----

if selected == 'Filter':
    st.sidebar.header("Please Filter Here:")

    city = st.sidebar.multiselect(
        "Select the city:",
        options=data['city'].unique(),
        default=data['city'].unique()
    )

    state = st.sidebar.multiselect(
        "Select the state:",
        options=data['state'].unique(),
        default=data['state'].unique()
    )

    store_type = st.sidebar.multiselect(
        "Select the type:",
        options=data['store_type'].unique(),
        default=data['store_type'].unique()
    )

    data = data.query(
        "city == @city & state == @state & store_type == @store_type"
    )

# -------- Main Page ----------

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# TOP KPI's
# TOP KPI's
stores = int(data["store_nbr"].nunique())
cities = int(data["city"].nunique())
states = int(data["state"].nunique())
store_types = int(data["store_type"].nunique())
products = int(data["family"].nunique())
cluster = int(data["cluster"].nunique())

col1, col2, col3, col4, col5, col6 = st.columns(6)

with col1:
    st.markdown(
        f'<div class="kpi-box"><div class="kpi-label">STORES</div><div class="kpi-value">{stores}</div></div>',
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        f'<div class="kpi-box"><div class="kpi-label">CITIES</div><div class="kpi-value">{cities}</div></div>',
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        f'<div class="kpi-box"><div class="kpi-label">STATES</div><div class="kpi-value">{states}</div></div>',
        unsafe_allow_html=True
    )

with col4:
    st.markdown(
        f'<div class="kpi-box"><div class="kpi-label">TYPES</div><div class="kpi-value">{store_types}</div></div>',
        unsafe_allow_html=True
    )

with col5:
    st.markdown(
        f'<div class="kpi-box"><div class="kpi-label">PRODUCTS</div><div class="kpi-value">{products}</div></div>',
        unsafe_allow_html=True
    )

with col6:
    st.markdown(
        f'<div class="kpi-box"><div class="kpi-label">CLUSTER</div><div class="kpi-value">{cluster}</div></div>',
        unsafe_allow_html=True
    )




# ------ BEST SELLING PRODUCTS --------

df_fa_sa = data.groupby('family').agg({"sales": "mean"}).reset_index().sort_values(by='sales', ascending=False)[:10]
df_fa_sa['color'] = ['#FAA831', '#F9AE49', '#F8B661', '#F7BE79', '#F6C591',
                     '#F5CCAA', '#F4D3C2', '#F3DADC', '#F2E1F4', '#F1E8FC']

fig1 = go.Figure(data=[go.Bar(
    x=df_fa_sa['sales'],
    y=df_fa_sa['family'],
    marker=dict(color=df_fa_sa['color']),
    name='Family',
    orientation='h',
    text=df_fa_sa['sales'].astype(int),
    textposition='auto',
    hoverinfo='text',
    hovertext=
    '<b>Family</b>: ' + df_fa_sa['family'] + '<br>' +
    '<b>Sales</b>: $' + df_fa_sa['sales'].astype(int).astype(str) + '<br>',
)])

fig1.update_layout(
    title={
        'text': 'The 10 Best-Selling Products',
        'x': 0.5,
        'y': 0.95,
        'xanchor': 'center',
        'yanchor': 'top',
        'font': {
            'size': 20,
            'color': colors['text']
        }
    },
    paper_bgcolor=colors['background'],
    plot_bgcolor=colors['background'],
    font=dict(size=14, color=colors['text']),
)

fig1.update_xaxes(showgrid=True, gridcolor='#dddddd', tickprefix='$')
fig1.update_yaxes(showgrid=False, categoryorder='total ascending', showline=True, linecolor='#dddddd')

fig1.update_traces(marker_line_color='#ffffff', marker_line_width=0.5)
fig1.update_layout(legend=dict(font=dict(color=colors['text'])))


# -------- AVERAGE SALES VS STORE TYPES -------------

df_st_sa = data.groupby('store_type').agg({"sales": "mean"}).reset_index().sort_values(by='sales', ascending=False)

fig2 = go.Figure(data=[go.Pie(
    labels=df_st_sa['store_type'],
    values=df_st_sa['sales'],
    hole=0.7,
    hoverinfo='label+percent+value',
    textinfo='label',
    marker=dict(colors=[colors['level1'], colors['level3'], colors['level5'], colors['level7'], colors['level9']]),
)])

fig2.update_layout(
    title={
        'text': 'The Average Sales Vs Store Types',
        'x': 0.5,
        'y': 0.95,
        'xanchor': 'center',
        'yanchor': 'top',
        'font': {
            'size': 20,
            'color': colors['text']
        }
    },
    paper_bgcolor=colors['background'],
    plot_bgcolor=colors['background'],
    font=dict(size=14, color=colors['text']),
    margin=dict(t=100),
)

fig2.update_traces(
    textfont=dict(color=colors['text']),
    marker=dict(line=dict(color='#ffffff', width=1))
)

fig2.update_layout(legend=dict(font=dict(color=colors['text'])))

# ------------- CLUSTER VS SALES ---------------

df_cl_sa = data.groupby('cluster').agg({"sales": "mean"}).reset_index().sort_values(by='sales', ascending=False)
df_cl_sa['color'] = colors['level10']
df_cl_sa['color'][:1] = colors['level1']
df_cl_sa['color'][1:2] = colors['level2']
df_cl_sa['color'][2:3] = colors['level3']
df_cl_sa['color'][3:4] = colors['level4']
df_cl_sa['color'][4:5] = colors['level5']
fig3 = go.Figure(data=[go.Bar(
    y=df_cl_sa['sales'],
    x=df_cl_sa['cluster'],
    marker=dict(color=df_cl_sa['color']),
    name='Cluster',
    text=df_cl_sa['sales'].astype(int),
    textposition='auto',
    hoverinfo='text',
    hovertext=
    '<b>Cluster</b>:' + df_cl_sa['cluster'].astype(str) + '<br>' +
    '<b>Sales</b>:' + df_cl_sa['sales'].astype(int).astype(str) + '<br>',
)])

fig3.update_layout(
    title_text='Clusters Vs Sales',
    paper_bgcolor=colors['background'],
    plot_bgcolor=colors['background'],
    font=dict(size=14, color='white')
)

fig3.update_xaxes(tickmode='array', tickvals=df_cl_sa.cluster)
fig3.update_yaxes(showgrid=False)

# ------------ AVERAGE SALES VS CITIES -------------

df_city_sa = data.groupby('city').agg({"sales": "mean"}).reset_index().sort_values(by='sales', ascending=False)
df_city_sa['color'] = colors['level10']
df_city_sa['color'][:1] = colors['level1']
df_city_sa['color'][1:2] = colors['level2']
df_city_sa['color'][2:3] = colors['level3']
df_city_sa['color'][3:4] = colors['level4']
df_city_sa['color'][4:5] = colors['level5']

fig4 = go.Figure(data=[go.Bar(
    y=df_city_sa['sales'],
    x=df_city_sa['city'],
    marker=dict(color=df_city_sa['color']),
    name='State',
    text=df_city_sa['sales'].astype(int),
    textposition='auto',
    hoverinfo='text',
    hovertext=
    '<b>City</b>:' + df_city_sa['city'] + '<br>' +
    '<b>Sales</b>:' + df_city_sa['sales'].astype(int).astype(str) + '<br>',
)])

fig4.update_layout(
    title_text='The Average Sales Vs Cities',
    paper_bgcolor=colors['background'],
    plot_bgcolor=colors['background'],
    font=dict(size=14, color='#ffffff')
)

fig4.update_yaxes(showgrid=False, categoryorder='total ascending')

# ---------- AVERAGE SALES VS STATES ---------------

df_state_sa = data.groupby('state').agg({"sales": "mean"}).reset_index().sort_values(by='sales', ascending=False)
df_state_sa['color'] = colors['level10']
df_state_sa['color'][:1] = colors['level1']
df_state_sa['color'][1:2] = colors['level2']
df_state_sa['color'][2:3] = colors['level3']
df_state_sa['color'][3:4] = colors['level4']
df_state_sa['color'][4:5] = colors['level5']

fig5 = go.Figure(data=[go.Bar(
    y=df_state_sa['sales'],
    x=df_state_sa['state'],
    marker=dict(color=df_state_sa['color']),
    name='State',
    text=df_state_sa['sales'].astype(int),
    textposition='auto',
    hoverinfo='text',
    hovertext=
    '<b>State</b>: ' + df_state_sa['state'] + '<br>' +
    '<b>Sales</b>: $' + df_state_sa['sales'].astype(int).astype(str) + '<br>',
)])

fig5.update_layout(
    title={
        'text': 'The Average Sales Vs States',
        'x': 0.5,
        'y': 0.95,
        'xanchor': 'center',
        'yanchor': 'top',
        'font': {
            'size': 20,
            'color': colors['text']
        }
    },
    paper_bgcolor=colors['background'],
    plot_bgcolor=colors['background'],
    font=dict(size=14, color=colors['text']),
)

fig5.update_yaxes(showgrid=False, categoryorder='total ascending', showline=True, linecolor='#dddddd')

fig5.update_traces(marker_line_color='#ffffff', marker_line_width=0.5)
fig5.update_layout(legend=dict(font=dict(color=colors['text'])))


# ---------- AVERAGE DAILY SALES --------------

df_day_sa = data.groupby('date').agg({"sales": "mean"}).reset_index()
fig6 = go.Figure(data=[go.Scatter(
    x=df_day_sa['date'],
    y=df_day_sa['sales'],
    fill='tozeroy',
    fillcolor='#FAA831',
    line_color='#bA6800'
)])

fig6.update_layout(
    title={
        'text': 'The Average Daily Sales',
        'font': {'color': 'white'}
    },
    height=300,
    paper_bgcolor='#232425',
    plot_bgcolor='#232425',
    font=dict(size=12, color='white')
)

fig6.update_xaxes(showgrid=False)
fig6.update_yaxes(showgrid=False)

# ---------- Quarter-wise avg sale ------------

import plotly.graph_objects as go

df_q_sa = data.groupby('quarter').agg({"sales": "mean"}).reset_index()

fig7 = go.Figure(data=[go.Pie(
    values=df_q_sa['sales'],
    labels=df_q_sa['quarter'],
    name='Quarter',
    marker=dict(colors=[colors['level1'], colors['level3'], colors['level5'], colors['level7'], colors['level9']]),
    hole=0.7,
    hoverinfo='label+percent+value',
    textinfo='label'
)])

# Styling
fig7.update_layout(
    title={
        'text': 'Quarter-wise Average Sales Analysis',
        'font': {'color': 'white'}
    },
    height=300,
    paper_bgcolor='#232425',
    plot_bgcolor='#232425',
    font=dict(size=12, color='white')
)

fig7.update_xaxes(showgrid=False)
fig7.update_yaxes(showgrid=False)


# ---------- AVERAGE MONTHLY SALES -------------

import plotly.graph_objects as go

df_mon_sa = data.groupby('month').agg({"sales": "mean"}).reset_index()

fig8 = go.Figure(data=[go.Scatter(
    x=df_mon_sa['month'],
    y=df_mon_sa['sales'],
    fill='tozeroy',
    fillcolor='#FAA831',
    line_color='#BA6800',
    mode='lines+markers'
)])

fig8.update_layout(
    title={
        'text': 'Average Monthly Sales',
        'font': {'color': 'white'}
    },
    height=300,
    paper_bgcolor='#232425',
    plot_bgcolor='#232425',
    font=dict(size=12, color='white')
)

fig8.update_yaxes(showgrid=False)
fig8.update_xaxes(showgrid=False, tickmode='array', tickvals=df_mon_sa['month'])



# ------------ AVERAGE QUARTERLY SALES ----------------

import plotly.graph_objects as go

df_qu_sa = data.groupby('quarter').agg({"sales": "mean"}).reset_index()

fig9 = go.Figure(data=[go.Scatter(
    x=df_qu_sa['quarter'],
    y=df_qu_sa['sales'],
    fill='tozeroy',
    fillcolor='#FAA831',
    line_color='#BA6800',
    mode='lines+markers'
)])

fig9.update_layout(
    title={
        'text': 'Average Quarterly Sales',
        'font': {'color': 'white'}
    },
    height=300,
    paper_bgcolor='#232425',
    plot_bgcolor='#232425',
    font=dict(size=12, color='white')
)

fig9.update_yaxes(showgrid=False)
fig9.update_xaxes(showgrid=False, tickmode='array', tickvals=df_qu_sa['quarter'])



# ------------ AVERAGE ANNUAL SALES -----------------

import plotly.graph_objects as go

df_y_sa = data.groupby('year').agg({"sales": "mean"}).reset_index()

fig10 = go.Figure(data=[go.Scatter(
    x=df_y_sa['year'],
    y=df_y_sa['sales'],
    fill='tozeroy',
    fillcolor='#FAA831',
    line_color='#BA6800',
    mode='lines+markers'
)])

fig10.update_layout(
    title={
        'text': 'Average Annual Sales',
        'font': {'color': 'white'}
    },
    height=300,
    paper_bgcolor='#232425',
    plot_bgcolor='#232425',
    font=dict(size=12, color='white')
)

fig10.update_yaxes(showgrid=False)
fig10.update_xaxes(showgrid=False, tickmode='array', tickvals=df_y_sa['year'])



# ----------- SALES - STATES & CITIES ---------------

df_c_s_sa = data.groupby(['state', 'city']).agg({"sales": "mean"}).reset_index()
df_c_s_sa = df_c_s_sa[df_c_s_sa.sales > 0]
fig11 = px.sunburst(df_c_s_sa, path=['state', 'city'],
                    values='sales',
                    color='sales',
                    color_continuous_scale='Viridis',
                    color_continuous_midpoint=np.average(df_c_s_sa['sales'])
)

fig11.update_layout(
    title={
        'text': 'States & Cities',
        'x': 0.5,
        'y': 0.95,
        'xanchor': 'center',
        'yanchor': 'top',
        'font': {
            'size': 20,
            'color': '#ffffff'
        }
    },
    width=500,
    paper_bgcolor=colors['background'],
    plot_bgcolor=colors['background'],
    font=dict(color=colors['text']),
)

fig11.update_traces(
    hovertemplate='<b>State</b>: %{id}<br><b>Sales</b>: $%{value}',
    hoverlabel=dict(bgcolor=colors['background'], font=dict(color=colors['text']))
)


# ------------- BOARDS -----------------

if selected == 'Home' or selected == 'Filter':
    col7, col8 = st.columns([1, 2])

    with col7:
        st.plotly_chart(fig2, True)
    with col8:
        st.plotly_chart(fig1, True)

    col9, col10 = st.columns([3, 2])

    with col9:
        st.plotly_chart(fig5, True)
    with col10:
        st.plotly_chart(fig11, True)

    st.plotly_chart(fig4, True)

if selected == 'Timely Sales':
    col11, col12 = st.columns([1, 2])

    with col11:
        st.plotly_chart(fig7, True)
    with col12:
        st.plotly_chart(fig9, True)

    st.plotly_chart(fig10, True)
    st.plotly_chart(fig8, True)
    st.plotly_chart(fig6, True)

# Apply custom CSS styles
st.markdown('<link href="style.css" rel="stylesheet">', unsafe_allow_html=True)

# Your Streamlit code here...

# ------ FOOTER -------
with st.container():
    st.markdown('<div class="footer-container">', unsafe_allow_html=True)
    st.markdown('<div class="footer">', unsafe_allow_html=True)
    st.markdown('<p>Created by Khang</p>', unsafe_allow_html=True)
    st.markdown('<p>ERP Project</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
