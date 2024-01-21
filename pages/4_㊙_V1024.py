import streamlit as st
import pandas as pd
import time
import os
from datetime import datetime
from openpyxl import load_workbook

st.set_page_config(page_title="explore 1024", page_icon="📃")

st.markdown("# explore1024")
st.sidebar.header("explore1024")
st.write(
    """This page tranfer 1024 pages"""
)
url = 'https://t66y.com/index.php'
st.write(
    f'<iframe src="{url}" width="700" height="500"></iframe>', unsafe_allow_html=True)
