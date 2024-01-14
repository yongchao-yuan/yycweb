import streamlit as st
import pandas as pd
import time
import os
import akshare as ak
from datetime import datetime
from openpyxl import load_workbook

st.set_page_config(page_title="memorandum", page_icon="📃")

st.markdown("# memorandum")
st.sidebar.header("memorandum")
st.write(
    """This page show a memorandum function"""
)

pd_diary = "data/diary_book.xlsx"
if os.path.isfile(pd_diary):
    df_diary = pd.read_excel(pd_diary)
else:
    df_diary = pd.DataFrame(columns=['date', 'title', 'content'])

i_date = datetime.now().strftime("%Y-%m-%d")
i_title = ''
t_date = st.text_input('date:', i_date)
t_title = st.text_input('title:', i_title)
t_content = st.text_area('content:')

save_button = st.button('save')
if save_button:
    df1 = pd.DataFrame({'date': [t_date], 'title': [
                       t_title], 'content': [t_content]})
    with pd.ExcelWriter(pd_diary) as writer:
        rows = df_diary.shape[0]
        df1.to_excel(writer, index=False,
                     header=rows == 0, startrow=rows, startcol=0)
    st.success("saved!")

inq_button = st.button('inquery')

if inq_button:
    df2 = pd.read_excel(pd_diary)
    t_date = t_date.strip()
    t_title = t_title.strip()
    t_content = t_content.strip()
    if len(t_date) > 0:
        df2 = df2.loc[df2['date'].str.contains(t_date)]
    if len(t_title) > 0:
        df2 = df2.loc[df2['title'].str.contains(t_title)]
    if len(t_content) > 0:
        df2 = df2.loc[df2['content'].str.contains(t_content)]
    f"inquery retrive {df2.shape[0]} results"
    df2
