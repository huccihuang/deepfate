import datetime
import streamlit as st
from src.core.fate_calculator import FateCalculator
from src.config.prompts import system_prompt, user_prompt

name = st.text_input("姓名")
sex = st.selectbox('性别', ['男', '女', '非二元性别'])
birthdate = st.date_input("出生日期", min_value=datetime.date(1900, 1, 1))
birthtime = st.time_input("出生时间")
birth_city = st.text_input("出生地点")
start_btn = st.button("开始算命")
result = st.empty()

calculator = FateCalculator()

if start_btn:
    response = calculator.calculate(name, sex, birthdate, birthtime, birth_city, system_prompt, user_prompt)
    result.markdown(response)