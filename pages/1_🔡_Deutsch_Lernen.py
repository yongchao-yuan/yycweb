import streamlit as st
import time
import numpy as np
import pandas as pd
import urllib.request
import re
import os
import random
import json
import requests
from hashlib import md5


def bd_get_word_sound(text, lan='de'):
    """
    lan : uk or en uk英音 en美音, de德语, jp日语, zh中文
    """
    spd = '2'  # default is 3 数字越小越慢
    urllib.request.urlretrieve("https://fanyi.baidu.com/gettts?lan=" +
                               lan+"&text="+text+"&spd="+spd+"&source=web", "sounds/"+text+".mp3")


def bd_trans(query, fromlang="zh", tolang="de"):
    # Set your own appid/appkey.
    appid = '20240113001939683'
    appkey = 'FqwW2FJSGxug8jKJf7zM'

    # For list of language codes, please refer to `https://api.fanyi.baidu.com/doc/21`
    from_lang = fromlang  # 'en'
    to_lang = tolang  # 'zh'

    endpoint = 'http://api.fanyi.baidu.com'
    path = '/api/trans/vip/translate'
    url = endpoint + path

    # query = 'Hello World! This is 1st paragraph.\nThis is 2nd paragraph.'

    # Generate salt and sign
    def make_md5(s, encoding='utf-8'):
        return md5(s.encode(encoding)).hexdigest()

    salt = random.randint(32768, 65536)
    sign = make_md5(appid + query + str(salt) + appkey)

    # Build request
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    payload = {'appid': appid, 'q': query, 'from': from_lang,
               'to': to_lang, 'salt': salt, 'sign': sign}

    # Send request
    r = requests.post(url, params=payload, headers=headers)
    result = r.json()

    # Show response
    # print(json.dumps(result, indent=4, ensure_ascii=False))
    if "error_code" in result:
        return None, result["error_msg"]
    else:
        return result["trans_result"][0]["src"], result["trans_result"][0]["dst"]


def search_word(word):
    # 根据德语单词查找所在行号
    values = df['Deutsch']
    return [i for i in range(len(values)) if values[i] == word]


st.set_page_config(page_title="Deutsch Lernen", page_icon="🔡")

st.markdown("# Deutsch Lernen")
st.sidebar.header("Deutsch Lernen")

pd_histfilename = "data/de_history.csv"
if os.path.isfile(pd_histfilename):
    df_hist = pd.read_csv(pd_histfilename, delimiter="|")
else:
    df_hist = pd.DataFrame(columns=['From', 'To'])

my_tolang = st.sidebar.selectbox("to which language?",
                                 ("zh", "de", "en", "jp"))
inputword = ''
word = st.sidebar.text_input('source text', inputword)
sd_my_slot = st.sidebar.empty()
sd_button = st.sidebar.button('translate')
if sd_button:
    sd_dstr, sd_zstr = bd_trans(word, fromlang="auto", tolang=my_tolang)
    sd_my_slot.text(sd_zstr)
    if (sd_dstr != sd_zstr):
        newdata = {'From': [sd_dstr], 'To': [sd_zstr]}
        newrow = pd.DataFrame(newdata)
        df_hist = pd.concat([newrow, df_hist], axis=0, ignore_index=True)
        df_hist.to_csv(pd_histfilename, index=False, sep="|")

st.write(
    """Sie können nach deutschen Wörtern suchen, Wörter eingeben,
    Wörter überprüfen oder den gesamten Satz übersetzen. 
    Die Ergebnisse der Worteingabe und Übersetzung werden 
    für die zukünftige Überprüfung gespeichert!"""
)

# load data from csv file
pd_filename = "data/de_words.csv"
if os.path.isfile(pd_filename):
    df = pd.read_csv(pd_filename)
else:
    df = pd.DataFrame(
        columns=['Deutsch', 'Chinesisch', 'Aussprache', 'Frequenz'])

with st.form(key='suchen'):
    inputword = ''
    word = st.text_input('Eingabewörter', inputword)
    my_slot = st.empty()
    submit_button = st.form_submit_button(label='bestätigen')

if submit_button:
    dstr, zstr = bd_trans(word, fromlang="de", tolang="zh")
    my_slot.text(zstr)
    if len(word.split()) <= 1:
        ret = search_word(word)
        if len(ret) == 0:
            bd_get_word_sound(word, lan='de')
            newdata = {'Deutsch': [word], 'Chinesisch': [zstr],
                       'Aussprache': [f"{word}.mp3"], 'Frequenz': [1]}
            newrow = pd.DataFrame(newdata)
            df = pd.concat([newrow, df], axis=0, ignore_index=True)
        else:
            row = df.iloc[ret[0]]
            if row['Chinesisch'] == "":
                row['Chinesisch'] = zstr
            if row['Aussprache'] == "":
                row['Aussprache'] = f"{word}.mp3"
            row['Frequenz'] += 1
            df.loc[ret[0]] = row
        st.audio(open(f"sounds/{word}.mp3", 'rb').read(), format='audio/mp3')
        df.to_csv(pd_filename, index=False)

df
"------------------------------"
"sentence translate history...."
df_hist
