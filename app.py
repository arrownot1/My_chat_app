import streamlit as st
import requests
import json
from datetime import datetime
import time

# ตั้งค่าหน้าเว็บ
st.set_page_config(
    page_title="My Personal Chat AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS สำหรับปรับแต่งหน้าตา
st.markdown("""
<style>
.main-header {
    background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    padding: 1rem;
    border-radius: 10px;
    margin-bottom: 2rem;
    text-align: center;
    color: white;
}

.chat-container {
    background-color: #f8f9fa;
    padding: 1rem;
    border-radius: 10px;
    margin: 1rem 0;
}

.user-message {
    background-color: #007bff;
    color: white;
    padding: 0.5rem 1rem;
    border-radius: 18px;
    margin: 0.5rem 0;
    text-align: right;
}

.ai-message {
    background-color: #28a745;
    color: white;
    padding: 0.5rem 1rem;
    border-radius: 18px;
    margin: 0.5rem 0;
}

.sidebar-section {
    background-color: #f1f3f4;
    padding: 1rem;
    border-radius: 8px;
    margin: 1rem 0;
}
</style>
""", unsafe_allow_html=True)

# หัวข้อหลัก
st.markdown("""
<div class="main-header">
    <h1>🤖 My Personal Chat AI</h1>
    <p>Powered by DeepSeek API</p>
</div>
""", unsafe_allow_html=True)

# สร้าง session state สำหรับเก็บข้อมูล
if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "api_calls_count" not in st.session_state:
    st.session_state.api_calls_count = 0

if "current_model" not in st.session_state:
    st.session_state.current_model = "deepseek-chat"

# Sidebar สำหรับการตั้งค่า
with st.sidebar:
    st.markdown("### ⚙️ การตั้งค่า")
    
    # เลือกโมเดล AI
    model_options = {
        "deepseek-chat": "DeepSeek Chat",
        "deepseek-coder": "DeepSeek Coder"
    }
    
    selected_model = st.selectbox(
        "เลือกโมเดล AI:",
        options=list(model_options.keys()),
        format_func=lambda x: model_options[x],
        index=0
    )
    st.session_state.current_model = selected_model
    
    # ตั้งค่าพารามิเตอร์ AI
    st.markdown("#### 🎛️ ตั้งค่า AI")
    temperature = st.slider("Temperature (ความคิดสร้างสรรค์)", 0.0, 2.0, 0.7, 0.1)
    max_tokens = st.slider("Max Tokens (ความยาวคำตอบ)", 100, 2000, 1000, 100)
    
    # ตั้งค่าภาษา
    st.markdown("#### 🌐 ตั้งค่าภาษา")
    language_options = {
        "auto": "ตรวจจับอัตโนมัติ",
        "th": "ไทย",
        "en": "English",
        "zh": "中文",
        "ja": "日本語"
    }
    
    selected_language = st.selectbox(
        "ภาษาที่ต้องการให้ AI ตอบ:",
        options=list(language_options.keys()),
        format_func=lambda x: language_options[x]
    )
    
    # สถิติการใช้งาน
    st.markdown("#### 📊 สถิติการใช้งาน")
    st.metric("จำนวนการเรียก API", st.session_state.api_calls_count)
    st.metric("จำนวนข้อความ", len(st.session_state.messages))
    
    st.markdown("---")
    
    # ปุ่มควบคุม
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🗑️ ล้างประวัติ", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
    
    with col2:
        if st.button("📥 Export Chat", use_container_width=True):
            if st.session_state.messages:
                # สร้างข้อความสำหรับ export
                export_text = f"Chat Export - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                export_text += "="*50 + "\n\n"
                
                for msg in st.session_state.messages:
                    role = "คุณ" if msg["role"] == "user" else "AI"
                    export_text += f"{role}: {msg['content']}\n\n"
                
                st.download_button(
                    label="💾 ดาวน์โหลด",
                    data=export_text,
                    file_name=f"chat_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain"
                )
    
    # คำแนะนำการใช้งาน
    st.markdown("---")
    st.markdown("### 💡 คำแนะนำ")
    st.markdown("""
    - **พิมพ์คำถาม** ในช่องด้านล่าง
    - **ปรับ Temperature** เพื่อเปลี่ยนความคิดสร้างสรรค์
    - **เลือกโมเดล** ที่เหมาะกับงาน
    - **Export การสนทนา** เพื่อบันทึก
    """)

# แสดงประวัติการสนทนา
st.markdown("### 💬 การสนทนา")

# สร้าง container สำหรับ chat
chat_container = st.container()

with chat_container:
    for i, message in enumerate(st.session_state.messages):
        if message["role"] == "user":
            with st.chat_message("user", avatar="👤"):
                st.markdown(f"**คุณ:** {message['content']}")
        else:
            with st.chat_message("assistant", avatar="🤖"):
                st.markdown(f"**AI:** {message['content']}")

# ฟังก์ชันสำหรับเรียก API
def call_deepseek_api(messages, model, temperature, max_tokens, language):
    try:
        # เตรียม system message ตามภาษาที่เลือก
        system_messages = []
        if language != "auto":
            language_prompts = {
                "th": "กรุณาตอบเป็นภาษาไทย",
                "en": "Please respond in English",
                "zh": "请用中文回答",
                "ja": "日本語で答えてください"
            }
            if language in language_prompts:
                system_messages.append({
                    "role": "system", 
                    "content": language_prompts[language]
                })
        
        # รวม system messages กับ user messages
        all_messages = system_messages + [{"role": "user", "content": messages}]
        
        headers = {
            "Authorization": f"Bearer {st.secrets['DEEPSEEK_API_KEY']}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": model,
            "messages": all_messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": False
        }
        
        response = requests.post(
            "https://api.deepseek.com/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=30
        )
        
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            return f"❌ เกิดข้อผิดพลาด: HTTP {response.status_code}"
            
    except requests.exceptions.Timeout:
        return "⏰ หมดเวลาการเชื่อมต่อ กรุณาลองใหม่อีกครั้ง"
    except requests.exceptions.ConnectionError:
        return "🌐 ไม่สามารถเชื่อมต่ออินเทอร์เน็ตได้"
    except Exception as e:
        return f"❌ เกิดข้อผิดพลาด: {str(e)}"

# รับข้อความจากผู้ใช้
if prompt := st.chat_input("💭 พิมพ์ข้อความของคุณที่นี่...", key="user_input"):
    # เพิ่มข้อความผู้ใช้ลงในประวัติ
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # แสดงข้อความผู้ใช้
    with st.chat_message("user", avatar="👤"):
        st.markdown(f"**คุณ:** {prompt}")
    
    # แสดง loading spinner
    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("🤔 AI กำลังคิด..."):
            # เรียก API
            ai_response = call_deepseek_api(
                prompt,
                st.session_state.current_model,
                temperature,
                max_tokens,
                selected_language
            )
            
            # นับจำนวนการเรียก API
            st.session_state.api_calls_count += 1
            
            # แสดงคำตอบ
            st.markdown(f"**AI:** {ai_response}")
            
            # เพิ่มคำตอบ AI ลงในประวัติ
            st.session_state.messages.append({"role": "assistant", "content": ai_response})

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; font-size: 14px;'>
    🚀 สร้างด้วย Streamlit | 🤖 Powered by DeepSeek API<br>
    Made with ❤️ for personal use
</div>
""", unsafe_allow_html=True)

# แสดงเวอร์ชันและข้อมูลเพิ่มเติม
if st.checkbox("🔧 แสดงข้อมูลเทคนิค"):
    st.json({
        "Streamlit Version": st.__version__,
        "Current Model": st.session_state.current_model,
        "Temperature": temperature,
        "Max Tokens": max_tokens,
        "Language": selected_language,
        "Total Messages": len(st.session_state.messages),
        "API Calls": st.session_state.api_calls_count
    })
