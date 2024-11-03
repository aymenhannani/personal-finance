# widgets/visualizations.py

import streamlit as st
import plotly.express as px

def plot_bar_chart(data, x, y, title, labels=None):
    fig = px.bar(data, x=x, y=y, title=title, labels=labels)
    st.plotly_chart(fig, use_container_width=True)

def plot_line_chart(data, x, y, title, labels=None):
    fig = px.line(data, x=x, y=y, title=title, labels=labels)
    st.plotly_chart(fig, use_container_width=True)

def plot_pie_chart(data, names, values, title):
    fig = px.pie(data, names=names, values=values, title=title)
    st.plotly_chart(fig, use_container_width=True)
