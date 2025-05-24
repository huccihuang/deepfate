from openai import OpenAI
import streamlit as st

class FateCalculator:
    def __init__(self):
        self.client = OpenAI(
            api_key=st.secrets['OPENAI_API_KEY'],
            base_url="https://api.deepseek.com"
        )
    
    def calculate(self, name, sex, birthdate, birthtime, birth_city, system_prompt, user_prompt):
        stream = self.client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {'role':'system', 'content': system_prompt},
                {'role': 'user', 'content': user_prompt.format(
                    user_name=name, 
                    sex=sex, 
                    birthdate=birthdate, 
                    birthtime=birthtime, 
                    birth_city=birth_city
                )},  
            ],
            stream=True  # 启用流式输出
        )
        
        return stream