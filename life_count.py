import streamlit as st
import datetime
import os
import base64

# --- 1. 页面配置 ---
st.set_page_config(
    page_title="生命倒计时",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- 2. 核心配置区 (路径已更新) ---
NOTE_FILE = "my_focus.txt"

# ✅ 关键修改：加上了文件夹路径 "music"
# os.path.join 会自动处理 Windows 的斜杠问题，非常稳
MUSIC_FILE = os.path.join("music", "曹于漫 - 你不必非要做任何.mp3")

DEADLINE = datetime.date(2046, 2, 4)
START_DATE = datetime.date(2026, 2, 4)


# --- 3. 核心逻辑函数 ---
def load_notes():
    if os.path.exists(NOTE_FILE):
        with open(NOTE_FILE, "r", encoding="utf-8") as f:
            return f.read()
    return ""


def save_notes(content):
    with open(NOTE_FILE, "w", encoding="utf-8") as f:
        f.write(content)


# 音乐加载函数
def get_audio_html(file_path):
    # 增加调试信息，如果路径不对，会在网页上直接告诉你
    if not os.path.exists(file_path):
        # 获取当前代码运行的目录，帮你排查问题
        current_dir = os.getcwd()
        st.error(f"""
        ⚠️ 找不到音乐文件！

        代码正在这个位置找：{current_dir}
        它试图找这个文件：{file_path}

        请确认：
        1. 你的 'music' 文件夹确实和 life_count.py 在一起。
        2. 音乐文件名必须一字不差（包括空格）。
        """)
        return ""

    with open(file_path, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode()
    return f"""
    <audio id="bgm" autoplay loop>
        <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
    </audio>
    <script>
        var audio = document.getElementById("bgm");
        audio.volume = 0.4; 
        var playPromise = audio.play();
        if (playPromise !== undefined) {{
            playPromise.catch(error => {{
                document.addEventListener('click', function() {{
                    audio.play();
                }}, {{ once: true }});
            }});
        }}
    </script>
    """


today = datetime.date.today()
remaining_days = (DEADLINE - today).days
total_duration = (DEADLINE - START_DATE).days
progress_val = max(0.0, min(1.0, remaining_days / total_duration)) if total_duration > 0 else 0
progress_percent = f"{progress_val:.1%}"

# --- 4. 禅意护眼版样式 ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@100;400;800&display=swap');

    .stApp {background-color: #0E1117 !important;}
    #MainMenu, footer, header {visibility: hidden;}
    .block-container {padding-top: 1rem !important; padding-bottom: 2rem !important; max-width: 100% !important;}

    @keyframes zen-breath {
        0% { color: #61dafb; text-shadow: 0 0 10px rgba(97, 218, 251, 0.3); opacity: 0.85; }
        50% { color: #a2e9ff; text-shadow: 0 0 20px rgba(97, 218, 251, 0.6); opacity: 1.0; }
        100% { color: #61dafb; text-shadow: 0 0 10px rgba(97, 218, 251, 0.3); opacity: 0.85; }
    }

    .cyber-card {
        display: flex; flex-direction: column; align-items: center; justify-content: center;
        padding: 40px 20px; margin-top: 20px;
        border: 1px solid #1f2937; border-radius: 20px;
        background: linear-gradient(180deg, #111827, #0b0f19);
        box-shadow: 0 4px 20px rgba(0,0,0,0.5);
    }

    .cyber-num {
        font-family: 'JetBrains Mono', monospace; font-size: 85px; font-weight: 800;
        line-height: 1.0; margin-bottom: 10px;
        animation: zen-breath 4s infinite ease-in-out;
    }

    .cyber-label {
        font-family: system-ui, -apple-system, sans-serif;
        font-size: 20px; font-weight: 600; color: #57606a; letter-spacing: 2px; margin-bottom: 25px;
    }

    .cyber-bar-box {
        width: 100%; height: 8px; background-color: #1f2937; border-radius: 4px; overflow: hidden;
    }
    .cyber-bar-fill {
        height: 100%; background-color: #61dafb; box-shadow: 0 0 10px rgba(97, 218, 251, 0.4);
    }

    .cyber-info {
        font-family: system-ui, -apple-system, sans-serif; color: #4b5563; font-size: 15px; margin-top: 12px; text-align: right; width: 100%;
    }

    .stTextArea textarea {background-color: #0d1117 !important; color: #c9d1d9 !important; border: 1px solid #30363d !important; font-size: 16px !important;}
    .stButton button {width: 100%; border: 1px solid #30363d; color: #8b949e; background: transparent; font-size: 16px; padding: 10px 0;}
    .stButton button:hover {border-color: #61dafb; color: #61dafb;}
</style>
""", unsafe_allow_html=True)

# --- 5. 渲染与交互 ---
audio_html = get_audio_html(MUSIC_FILE)
if audio_html:
    st.markdown(audio_html, unsafe_allow_html=True)

st.markdown(
    "<div style='text-align: center; color: #30363d; letter-spacing: 4px; font-size: 14px; margin-bottom: 10px; font-weight: bold;'>MEMENTO MORI</div>",
    unsafe_allow_html=True)

html_structure = f"""
<div class="cyber-card">
<div class="cyber-num">{remaining_days}</div>
<div class="cyber-label">静 待 余 生</div>
<div class="cyber-bar-box"><div class="cyber-bar-fill" style="width: {progress_percent};"></div></div>
<div class="cyber-info">生命电量: {progress_percent}</div>
</div>
"""
st.markdown(html_structure, unsafe_allow_html=True)

st.write("")

with st.expander("✍️ 今天你想要什么？", expanded=False):
    saved_content = load_notes()
    with st.form("notes_form"):
        user_input = st.text_area("写下来吧...", value=saved_content, height=120)
        if st.form_submit_button("保 存"):
            save_notes(user_input)

            st.success("已落笔")
