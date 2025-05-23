import os
import datetime
import streamlit as st
from src.core.fate_calculator import FateCalculator
from src.core.image_generator import ImageGenerator
from src.config.prompts import system_prompt, user_prompt

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
    # response = calculator.calculate(name, sex, birthdate, birthtime, birth_city, system_prompt, user_prompt)
    st.session_state.response = """
    ### Hucci 命理分析（非二元性别 · 空间站特殊时空格局）

    #### 一、八字排盘（空间站时间校准为东八区）
    **八字：乙巳 辛巳 壬辰 己酉**  
    **五行分布：** 木1 火2 土2 金2 水1（日主壬水生于巳月偏弱）  
    **特殊格局：** "火土成势，金水暗藏"的太空悬浮命局

    ---

    ### 二、核心命理解读
    #### 1. 时空格局特质
    - **宇宙印记：** 出生在脱离地球磁场的空间站，形成"无根之水"的特殊命局，象征超越传统框架的生命轨迹
    - **维度融合：** 时柱己酉出现"地外合金"现象（金属性在太空环境强化），预示在科技/跨维度领域有独特天赋

    #### 2. 性格光谱
    - **显性特质：** 巳月双火带来惊人的创造力，壬水智慧呈现量子态波动（时而理性如超级计算机，时而感性如星云）
    - **隐性维度：** 辰土酉金构成"磁力保护层"，表面适应性强，内在保持绝对独立的宇宙观
    - **进化提示：** 需注意火土过旺可能导致"大气层灼热效应"（情绪能量过载）

    #### 3. 事业轨迹
    - **最佳领域：**  
    ✅ 太空科技研发（特别是生命支持系统）  
    ✅ 跨物种/跨维度沟通  
    ✅ 反重力艺术创作  
    - **重大机遇：**  
    2043年"金星-天王星相位"时将出现改写职业规则的契机  
    2051年流年辛亥引发"水星逆行叠加"，慎防AI合约纠纷

    #### 4. 连接模式（传统感情概念的升维）
    - **能量交互：** 日支辰土为"引力井"，会吸引强烈但短暂的能量纠缠（传统婚姻概念不适用）
    - **灵魂共振：** 2027-2029年"柯伊伯带能量潮"期间可能遇见跨星际意识伙伴
    - **注意事项：** 慎防"轨道共振效应"（过度卷入他人命运螺旋）

    #### 5. 财富波动
    - **资源获取：** 酉金偏印显示通过专利/知识产权获利，2046年可能发现新型太空矿物收益
    - **消费黑洞：** 需警惕"曲速消费倾向"（为超前科技概念过度支出）
    - **理财建议：** 配置30%在加密货币，70%投资轨道农业复合体

    #### 6. 健康维护
    - **脆弱系统：** 微重力环境出生的骨骼发育需要持续监测，注意人工大气对肺经的影响
    - **能量补给：** 每月农历初一/十五需进行"地磁模拟沐浴"
    - **关键年份：** 2038年注意神经系统"太阳风敏感症"

    ---

    ### 三、跨维度生存建议
    1. 在火星基地时间（MT）与地球时间（UTC）之间建立个人节律缓冲带  
    2. 随身佩戴钇铝石榴石（YAG）平衡空间辐射  
    3. 当出现"星际迷失感"时，可通过创作分形艺术重组能量场  

    （注：此命盘已考虑空间站轨道高度造成的相对论效应，时区校准误差±0.0003%）
    """
    st.session_state.share_clicked = False
    
# 如果有结果，显示结果和分享按钮
if st.session_state.response and not st.session_state.share_clicked:
    result.markdown(st.session_state.response)
    # 显示分享按钮并捕获其点击状态
    share_popover = share_btn.popover("分享")

    temp_image_path = generator.generate_image(st.session_state.response) # 使用session state中的response
    share_popover.image(temp_image_path, caption="右键保存图片")
    os.unlink(temp_image_path)
