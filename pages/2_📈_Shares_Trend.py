import streamlit as st
import time
import os
import akshare as ak
import numpy as np
import pandas as pd


st.set_page_config(page_title="Shares Trend", page_icon="📈")

st.markdown("# Shares Trend")
st.sidebar.header("Shares Trend")


pd_codename = "data/shares_code.csv"
if os.path.isfile(pd_codename):
    df_code = pd.read_csv(pd_codename, dtype={'code': str, 'name': str})
else:
    df_code = pd.DataFrame(columns=['code', 'name'])

st.write(
    """This page shows the share's price trend current time. You can
    assign any stock.Enjoy!"""
)

tag = {'6': "sh", '0': "sz", '3': "sz", '8': "bj", '4': "bj"}
inputcode = ''
code = st.text_input('share code:', inputcode)
sh_button = st.button('show')

if sh_button:
    # 使用 st.image()显示图片
    # urllib.request.urlretrieve(
    #     f"http://image.sinajs.cn/newchart/min/n/{tag[code[0]]}{code}.gif", "pics/min"+code+".gif")
    # urllib.request.urlretrieve(
    #     f"http://image.sinajs.cn/newchart/daily/n/{tag[code[0]]}{code}.gif", "pics/daily"+code+".gif")
    # min_image = Image.open("pics/min"+code+".gif")
    # st.image(min_image)
    # daily_image = Image.open("pics/daily"+code+".gif")
    # st.image(daily_image)

    # 判断是否编码
    df = ak.stock_zh_a_spot_em()
    if (df is None or df.shape[0] < 1000):  # 真正的行情数据不会小于1000
        st.error("获取实时行情失败！")
    else:
        df.fillna(0.0, inplace=True)
        # 是否股票代码
        res_list = []
        code = code.strip()
        if code.isdigit():
            df1 = df[df["代码"] == code]
            if df1.shape[0] == 1:  # 股票代码存在
                # 使用markdown+html
                min_gif = f"http://image.sinajs.cn/newchart/min/n/{tag[code[0]]}{code}.gif"
                min_html = '<img src="{}" />'.format(min_gif)
                st.markdown(min_html, unsafe_allow_html=True)

                daily_gif = f"http://image.sinajs.cn/newchart/daily/n/{tag[code[0]]}{code}.gif"
                daily_html = '<img src="{}" />'.format(daily_gif)
                st.markdown(daily_html, unsafe_allow_html=True)

                df2 = df_code[df_code["code"] == code]
                if df2.shape[0] == 0:  # 新代码添加到代码列表里
                    name = df1.iloc[0]["名称"]
                    newrow = pd.DataFrame({'code': [code], 'name': [name]})
                    df_code = pd.concat([newrow, df_code],
                                        axis=0, ignore_index=True)
                    df_code.to_csv(pd_codename, index=False)
            else:  # 代码模糊查询
                # df.query(f'"{code}" in 代码')
                result1 = df.loc[df['代码'].str.contains(
                    code), ["代码", "名称", "最新价", "市盈率-动态"]]
                f"Inquery return {result1.shape[0]} result:"
                result1
        else:  # 名称模糊查询
            result2 = df.loc[df['名称'].str.contains(
                code), ["代码", "名称", "最新价", "市盈率-动态"]]
            f"Inquery return {result2.shape[0]} result:"
            result2
        "----------history inquery share--------------"
        df.loc[df["代码"].isin(df_code['code'].tolist()), [
            "代码", "名称", "最新价", "涨跌幅", "最高", "最低", "市盈率-动态"]]
st.button("Re-run")
