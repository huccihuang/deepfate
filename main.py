import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

from prompts import system_prompt, user_prompt

load_dotenv()

name = st.text_input("姓名")
sex = st.selectbox('性别', ['男', '女', '非二元性别'])
birthdate = st.date_input("出生日期", min_value=st.datetime.date(1900, 1, 1))
birthtime = st.time_input("出生时间")
birth_city = st.text_input("出生地点")

start_btn = st.button("开始算命")

result = st.empty()

if start_btn:
    client = OpenAI(
        base_url="https://api.deepseek.com"
    )
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': user_prompt.format(user_name=name, sex=sex, birthdate=birthdate, birthtime=birthtime, birth_city=birth_city)},
        ]
    )
    result.markdown(response.choices[0].message.content)
