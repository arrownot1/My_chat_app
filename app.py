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

# CSS สำหรับปรับแต่งหน้าตาให้สวยงามขึ้น
st.markdown("""
<style>
/* Import Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* Global Styles */
.stApp {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    background-attachment: fixed;
}

/* Hide Streamlit elements */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
.stDeployButton {display: none;}

/* Main header */
.main-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 2rem;
    border-radius: 15px;
    margin-bottom: 2rem;
    text-align: center;
    color: white;
    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    backdrop-filter: blur(10px);
}

.main-header h1 {
    font-size: 2.5rem;
    font-weight: 700;
    margin: 0;
    text-shadow: 0 2px 10px rgba(0,0,0,0.3);
}

.main-header p {
    font-size: 1.1rem;
    opacity: 0.9;
    margin: 0.5rem 0 0 0;
}

/* Chat container */
.chat-container {
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(20px);
    padding: 1.5rem;
    border-radius: 15px;
    margin: 1rem 0;
    box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    border: 1px solid rgba(255,255,255,0.2);
}

/* Message styles */
.user-message {
    background: linear-gradient(135deg, #007bff 0%, #0056b3 100%);
    color: white;
    padding: 0.75rem 1.25rem;
    border-radius: 20px;
    margin: 0.75rem 0;
    text-align: right;
    box-shadow: 0 4px 15px rgba(0,123,255,0.3);
    font-weight: 500;
}

.ai-message {
    background: linear-gradient(135deg, #28a745 0%, #1e7e34 100%);
    color: white;
    padding: 0.75rem 1.25rem;
    border-radius: 20px;
    margin: 0.75rem 0;
    box-shadow: 0 4px 15px rgba(40,167,69,0.3);
    font-weight: 500;
}

/* Sidebar styles */
.sidebar-section {
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
    padding: 1.25rem;
    border-radius: 12px;
    margin: 1rem 0;
    border: 1px solid rgba(255,255,255,0.2);
}

/* Custom chat message styling */
.stChatMessage {
    background: rgba(255, 255, 255, 0.95) !important;
    backdrop-filter: blur(20px);
    border-radius: 15px !important;
    border: 1px solid rgba(255,255,255,0.2);
    box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    margin: 1rem 0 !important;
}

.stChatMessage[data-testid="user-message"] {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    color: white;
}

.stChatMessage[data-testid="assistant-message"] {
    background: rgba(255, 255, 255, 0.95) !important;
}

/* Input styling */
.stChatInput > div {
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(20px);
    border-radius: 25px;
    border: 2px solid rgba(255,255,255,0.3);
    box-shadow: 0 8px 32px rgba(0,0,0,0.1);
}

.stChatInput input {
    background: transparent !important;
    border: none !important;
    font-size: 1rem;
    padding: 1rem 1.5rem;
}

/* Button styling */
.stButton > button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    border-radius: 10px;
    padding: 0.6rem 1.2rem;
    font-weight: 500;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
}

/* Selectbox styling */
.stSelectbox > div > div {
    background: rgba(255, 255, 255, 0.9);
    border-radius: 10px;
    border: 1px solid rgba(255,255,255,0.3);
    backdrop-filter: blur(10px);
}

/* Slider styling */
.stSlider > div > div > div {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

/* Metric styling */
.stMetric {
    background: rgba(255, 255, 255, 0.1);
    padding: 1rem;
    border-radius: 10px;
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.2);
}

/* Reasoning box for R1 */
.reasoning-container {
    background: rgba(255, 248, 220, 0.95);
    border: 2px solid #ffd700;
    border-radius: 12px;
    padding: 1rem;
    margin: 1rem 0;
    backdrop-filter: blur(10px);
}

.reasoning-header {
    color: #b8860b;
    font-weight: 600;
    font-size: 0.9rem;
    margin-bottom: 0.5rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.reasoning-content {
    background: rgba(255, 255, 255, 0.8);
    padding: 0.75rem;
    border-radius: 8px;
    font-family: 'Monaco', 'Consolas', monospace;
    font-size: 0.85rem;
    color: #444;
    white-space: pre-wrap;
    max-height: 300px;
    overflow-y: auto;
}

/* Footer styling */
.footer {
    text-align: center;
    color: rgba(255,255,255,0.8);
    font-size: 14px;
    margin-top: 2rem;
    padding: 1rem;
    background: rgba(255,255,255,0.1);
    border-radius: 10px;
    backdrop-filter: blur(10px);
}

/* Responsive design */
@media (max-width: 768px) {
    .main-header h1 {
        font-size: 2rem;
    }
    
    .main-header {
        padding: 1.5rem;
    }
    
    .chat-container {
        padding: 1rem;
    }
}

/* Animation */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

.stChatMessage {
    animation: fadeIn 0.5s ease-out;
}
</style>
""", unsafe_allow_html=True)

# หัวข้อหลัก
st.markdown("""
<div class="main-header">
    <h1>🤖 My Personal Chat AI</h1>
    <p>Powered by DeepSeek API with Advanced Reasoning</p>
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

if "show_reasoning" not in st.session_state:
    st.session_state.show_reasoning = False

# Sidebar สำหรับการตั้งค่า
with st.sidebar:
    st.markdown("### ⚙️ การตั้งค่า")
    
    # เลือกโมเดล AI
    model_options = {
        "deepseek-chat": "💬 DeepSeek Chat",
        "deepseek-coder": "💻 DeepSeek Coder",
        "deepseek-reasoner": "🧠 DeepSeek R1 (Reasoning)"
    }
    
    selected_model = st.selectbox(
        "เลือกโมเดล AI:",
        options=list(model_options.keys()),
        format_func=lambda x: model_options[x],
        index=0
    )
    st.session_state.current_model = selected_model
    
    # แสดงคำอธิบายโมเดล
    model_descriptions = {
        "deepseek-chat": "💬 เหมาะสำหรับการสนทนาทั่วไป",
        "deepseek-coder": "💻 เหมาะสำหรับการเขียนโค้ด", 
        "deepseek-reasoner": "🧠 เหมาะสำหรับการใช้เหตุผลที่ซับซ้อน"
    }
    st.info(model_descriptions[selected_model])
    
    # ตัวเลือกสำหรับ DeepSeek R1
    if selected_model == "deepseek-reasoner":
        st.session_state.show_reasoning = st.checkbox(
            "🔍 แสดงกระบวนการคิด (Chain of Thought)",
            value=st.session_state.show_reasoning,
            help="แสดงขั้นตอนการใช้เหตุผลของ AI"
        )
    
    # ตั้งค่าพารามิเตอร์ AI
    st.markdown("#### 🎛️ ตั้งค่า AI")
    
    # ปรับ parameter range สำหรับ R1
    if selected_model == "deepseek-reasoner":
        temperature = st.slider("Temperature (ความคิดสร้างสรรค์)", 0.0, 1.0, 0.3, 0.1,
                               help="R1 แนะนำให้ใช้ค่าต่ำเพื่อความแม่นยำ")
        max_tokens = st.slider("Max Tokens (ความยาวคำตอบ)", 1000, 8000, 4000, 500,
                              help="R1 ต้องการ tokens มากขึ้นสำหรับการใช้เหตุผล")
    else:
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
    col1, col2 = st.columns(2)
    with col1:
        st.metric("API Calls", st.session_state.api_calls_count)
    with col2:
        st.metric("Messages", len(st.session_state.messages))
    
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
    
    # ตัวอย่างคำถามสำหรับ R1
    if st.session_state.current_model == "deepseek-reasoner":
        st.markdown("---")
        st.markdown("#### 🎯 ตัวอย่างคำถามสำหรับ R1:")
        examples = [
            "แก้สมการ: x² + 5x - 6 = 0",
            "อธิบายทฤษฎีสัมพัทธภาพแบบง่าย",
            "วิเคราะห์ปัญหาเศรษฐกิจของไทย",
            "เปรียบเทียบ Python vs JavaScript"
        ]
        
        for i, example in enumerate(examples):
            if st.button(f"💡 {example[:25]}...", key=f"example_{i}", use_container_width=True):
                st.session_state.example_question = example
    
    # คำแนะนำการใช้งาน
    st.markdown("---")
    st.markdown("### 💡 คำแนะนำ")
    st.markdown("""
    - **💬 DeepSeek Chat**: สนทนาทั่วไป
    - **💻 DeepSeek Coder**: เขียนโค้ด, debug
    - **🧠 DeepSeek R1**: การใช้เหตุผลซับซ้อน
    - **ปรับ Temperature**: เพื่อเปลี่ยนความคิดสร้างสรรค์
    - **Export การสนทนา**: เพื่อบันทึกผลลัพธ์
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
                content = message['content']
                
                # แสดงการใช้เหตุผลสำหรับ R1
                if (st.session_state.current_model == "deepseek-reasoner" and 
                    st.session_state.show_reasoning and 
                    "<think>" in content and "</think>" in content):
                    
                    start_idx = content.find("<think>") + 7
                    end_idx = content.find("</think>")
                    reasoning_part = content[start_idx:end_idx].strip()
                    final_answer = content[end_idx+8:].strip()
                    
                    # แสดงกระบวนการคิด
                    st.markdown("""
                    <div class="reasoning-container">
                        <div class="reasoning-header">🧠 กระบวนการใช้เหตุผล (Chain of Thought)</div>
                        <div class="reasoning-content">{}</div>
                    </div>
                    """.format(reasoning_part), unsafe_allow_html=True)
                    
                    st.markdown(f"**AI:** {final_answer}")
                else:
                    st.markdown(f"**AI:** {content}")

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
        
        # เพิ่ม system message สำหรับ R1
        if model == "deepseek-reasoner":
            system_messages.append({
                "role": "system",
                "content": "คุณเป็น AI ที่มีความสามารถในการใช้เหตุผลแบบลึก กรุณาคิดอย่างเป็นระบบและแสดงขั้นตอนการคิดอย่างชัดเจน"
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
        
        # เพิ่ม reasoning parameters สำหรับ R1
        if model == "deepseek-reasoner":
            data["reasoning_effort"] = "medium"
        
        response = requests.post(
            "https://api.deepseek.com/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=60 if model == "deepseek-reasoner" else 30
        )
        
        if response.status_code == 200:
            result = response.json()
            content = result["choices"][0]["message"]["content"]
            
            # สำหรับ R1 อาจมี reasoning_content แยกต่างหาก
            if (model == "deepseek-reasoner" and 
                "reasoning_content" in result["choices"][0]["message"]):
                reasoning = result["choices"][0]["message"]["reasoning_content"]
                if reasoning:
                    content = f"<think>\n{reasoning}\n</think>\n\n{content}"
            
            return content
        else:
            return f"❌ เกิดข้อผิดพลาด: HTTP {response.status_code}"
            
    except requests.exceptions.Timeout:
        return "⏰ หมดเวลาการเชื่อมต่อ (R1 ใช้เวลาในการคิดนานกว่าปกติ) กรุณาลองใหม่อีกครั้ง"
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
        loading_text = "🧠 R1 กำลังใช้เหตุผล..." if st.session_state.current_model == "deepseek-reasoner" else "🤔 AI กำลังคิด..."
        
        with st.spinner(loading_text):
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
            
            # แสดงผลสำหรับ R1
            if (st.session_state.current_model == "deepseek-reasoner" and 
                st.session_state.show_reasoning and 
                "<think>" in ai_response and "</think>" in ai_response):
                
                start_idx = ai_response.find("<think>") + 7
                end_idx = ai_response.find("</think>")
                reasoning_part = ai_response[start_idx:end_idx].strip()
                final_answer = ai_response[end_idx+8:].strip()
                
                # แสดงกระบวนการคิด
                st.markdown("""
                <div class="reasoning-container">
                    <div class="reasoning-header">🧠 กระบวนการใช้เหตุผล (Chain of Thought)</div>
                    <div class="reasoning-content">{}</div>
                </div>
                """.format(reasoning_part), unsafe_allow_html=True)
                
                st.markdown(f"**AI:** {final_answer}")
            else:
                # แสดงคำตอบปกติ
                st.markdown(f"**AI:** {ai_response}")
            
            # เพิ่มคำตอบ AI ลงในประวัติ
            st.session_state.messages.append({"role": "assistant", "content": ai_response})

# ตรวจสอบคำถามตัวอย่างจาก sidebar
if hasattr(st.session_state, 'example_question'):
    example_prompt = st.session_state.example_question
    del st.session_state.example_question
    
    # เพิ่มคำถามตัวอย่างลงในประวัติ
    st.session_state.messages.append({"role": "user", "content": example_prompt})
    
    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("🧠 R1 กำลังใช้เหตุผล..."):
            ai_response = call_deepseek_api(
                example_prompt,
                st.session_state.current_model,
                temperature,
                max_tokens,
                selected_language
            )
            
            st.session_state.api_calls_count += 1
            st.session_state.messages.append({"role": "assistant", "content": ai_response})
    
    st.rerun()

# Footer
st.markdown("""
<div class="footer">
    🚀 สร้างด้วย Streamlit | 🤖 Powered by DeepSeek API<br>
    Made with ❤️ for personal use
</div>
""", unsafe_allow_html=True)

# แสดงเวอร์ชันและข้อมูลเทคนิค
if st.checkbox("🔧 แสดงข้อมูลเทคนิค"):
    st.json({
        "Streamlit Version": st.__version__,
        "Current Model": st.session_state.current_model,
        "Temperature": temperature,
        "Max Tokens": max_tokens,
        "Language": selected_language,
        "Total Messages": len(st.session_state.messages),
        "API Calls": st.session_state.api_calls_count,
        "Show Reasoning": st.session_state.show_reasoning
    })
