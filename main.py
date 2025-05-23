import os
import datetime
from pathlib import Path

import streamlit as st

from src.core.fate_calculator import FateCalculator
from src.core.image_generator import ImageGenerator
from src.config.prompts import system_prompt, user_prompt

st.set_page_config(page_title="DeepFate", page_icon=Path(__file__).parent.parent.parent / 'assets' / 'deepfate_icon.svg')

if 'response' not in st.session_state:
    st.session_state.response = None
if 'share_clicked' not in st.session_state:
    st.session_state.share_clicked = False

name = st.text_input("姓名")
sex = st.selectbox('性别', ['男', '女', '非二元性别'])
birthdate = st.date_input("出生日期", min_value=datetime.date(1900, 1, 1))
birthtime = st.time_input("出生时间")
birth_city = st.text_input("出生地点")
start_btn = st.button("开始算命")
result = st.empty()
share_btn = st.empty()
share_pic = st.empty()

calculator = FateCalculator()
generator = ImageGenerator()

if start_btn:
    response = calculator.calculate(name, sex, birthdate, birthtime, birth_city, system_prompt, user_prompt)
    st.session_state.response = response    
    st.session_state.share_clicked = False
    
# 如果有结果，显示结果和分享按钮
if st.session_state.response and not st.session_state.share_clicked:
    result.markdown(st.session_state.response)
    share_popover = share_btn.popover("分享")

    temp_image_path = generator.generate_image(st.session_state.response)
    share_popover.image(temp_image_path, caption="右键保存图片")
    os.unlink(temp_image_path)
