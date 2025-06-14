  import streamlit as st
  import requests
  import json
  from datetime import datetime
  import time

  # ตั้งค่าหน้าเว็บ
  st.set_page_config(
      page_title="DeepSeek Chat",
      page_icon="🧠",
      layout="wide",
      initial_sidebar_state="collapsed"
  )

  # Modern CSS สำหรับหน้าตาแบบ ChatGPT/DeepSeek
  st.markdown("""
  <style>
  /* Global Styles */
  .stApp {
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
  }

  /* Hide Streamlit branding */
  #MainMenu {visibility: hidden;}
  footer {visibility: hidden;}
  header {visibility: hidden;}

  /* Main container */
  .main-container {
      background: rgba(255, 255, 255, 0.95);
      backdrop-filter: blur(20px);
      border-radius: 20px;
      margin: 1rem;
      padding: 0;
      box-shadow: 0 20px 40px rgba(0,0,0,0.1);
      min-height: 90vh;
      display: flex;
      flex-direction: column;
  }

  /* Header */
  .chat-header {
      background: linear-gradient(135deg, #2d3748 0%, #4a5568 100%);
      color: white;
      padding: 1.5rem 2rem;
      border-radius: 20px 20px 0 0;
      display: flex;
      justify-content: space-between;
      align-items: center;
      box-shadow: 0 4px 20px rgba(0,0,0,0.1);
  }

  .chat-title {
      font-size: 1.5rem;
      font-weight: 600;
      margin: 0;
      display: flex;
      align-items: center;
      gap: 0.5rem;
  }

  .model-badge {
      background: rgba(255,255,255,0.2);
      padding: 0.25rem 0.75rem;
      border-radius: 20px;
      font-size: 0.8rem;
      font-weight: 500;
  }

  /* Chat Area */
  .chat-area {
      flex: 1;
      padding: 2rem;
      overflow-y: auto;
      background: #f8fafc;
      display: flex;
      flex-direction: column;
      gap: 1rem;
  }

  /* Message Bubbles */
  .message-container {
      display: flex;
      margin: 1rem 0;
      animation: fadeIn 0.3s ease-in;
  }

  .user-message {
      margin-left: auto;
      max-width: 70%;
  }

  .assistant-message {
      margin-right: auto;
      max-width: 70%;
  }

  .message-bubble {
      padding: 1rem 1.5rem;
      border-radius: 18px;
      font-size: 0.95rem;
      line-height: 1.5;
      box-shadow: 0 2px 10px rgba(0,0,0,0.1);
      position: relative;
  }

  .user-bubble {
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      color: white;
      border-bottom-right-radius: 4px;
  }

  .assistant-bubble {
      background: white;
      color: #2d3748;
      border: 1px solid #e2e8f0;
      border-bottom-left-radius: 4px;
  }

  .message-avatar {
      width: 32px;
      height: 32px;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 1.2rem;
      margin: 0 0.75rem;
      flex-shrink: 0;
  }

  .user-avatar {
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      color: white;
  }

  .assistant-avatar {
      background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);
      color: white;
  }

  /* Reasoning Box */
  .reasoning-box {
      background: #f7fafc;
      border: 1px solid #e2e8f0;
      border-radius: 12px;
      padding: 1rem;
      margin: 0.5rem 0;
      font-family: 'Monaco', 'Menlo', monospace;
      font-size: 0.85rem;
      color: #4a5568;
  }

  .reasoning-header {
      display: flex;
      align-items: center;
      gap: 0.5rem;
      font-weight: 600;
      color: #2d3748;
      margin-bottom: 0.5rem;
  }

  /* Input Area */
  .input-container {
      padding: 1.5rem 2rem;
      background: white;
      border-radius: 0 0 20px 20px;
      border-top: 1px solid #e2e8f0;
  }

  .input-wrapper {
      display: flex;
      align-items: center;
      gap: 1rem;
      background: #f8fafc;
      border-radius: 25px;
      padding: 0.75rem 1.5rem;
      border: 2px solid #e2e8f0;
      transition: all 0.2s ease;
  }

  .input-wrapper:focus-within {
      border-color: #667eea;
      box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
  }

  /* Settings Panel */
  .settings-panel {
      background: white;
      border-radius: 15px;
      padding: 1.5rem;
      margin: 1rem 0;
      box-shadow: 0 4px 20px rgba(0,0,0,0.1);
  }

  .settings-header {
      font-size: 1.1rem;
      font-weight: 600;
      color: #2d3748;
      margin-bottom: 1rem;
      display: flex;
      align-items: center;
      gap: 0.5rem;
  }

  /* Animations */
  @keyframes fadeIn {
      from { opacity: 0; transform: translateY(10px); }
      to { opacity: 1; transform: translateY(0); }
  }

  @keyframes pulse {
      0%, 100% { opacity: 1; }
      50% { opacity: 0.5; }
  }

  .typing-indicator {
      animation: pulse 1.5s infinite;
  }

  /* Responsive */
  @media (max-width: 768px) {
      .main-container {
          margin: 0.5rem;
          border-radius: 15px;
      }
      
      .chat-header {
          padding: 1rem;
          border-radius: 15px 15px 0 0;
      }
      
      .message-bubble {
          max-width: 85%;
      }
      
      .chat-area {
          padding: 1rem;
      }
  }

  /* Custom Streamlit Components */
  .stSelectbox > div > div {
      background: #f8fafc;
      border-radius: 10px;
      border: 1px solid #e2e8f0;
  }

  .stSlider > div > div {
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  }

  .stButton > button {
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      color: white;
      border: none;
      border-radius: 10px;
      padding: 0.5rem 1rem;
      font-weight: 500;
      transition: all 0.2s ease;
  }

  .stButton > button:hover {
      transform: translateY(-2px);
      box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
  }
  </style>
  """, unsafe_allow_html=True)

  # สร้าง session state
  if "messages" not in st.session_state:
      st.session_state.messages = []
  if "api_calls_count" not in st.session_state:
      st.session_state.api_calls_count = 0
  if "current_model" not in st.session_state:
      st.session_state.current_model = "deepseek-chat"
  if "show_reasoning" not in st.session_state:
      st.session_state.show_reasoning = False

  # Main Container
  st.markdown('<div class="main-container">', unsafe_allow_html=True)

  # Header
  col1, col2 = st.columns([3, 1])
  with col1:
      st.markdown("""
      <div class="chat-header">
          <div class="chat-title">
              🧠 DeepSeek Chat
              <span class="model-badge">AI Assistant</span>
          </div>
      </div>
      """, unsafe_allow_html=True)

  with col2:
      # Settings Toggle
      if st.button("⚙️", help="Settings", key="settings_toggle"):
          st.session_state.show_settings = not st.session_state.get('show_settings', False)

  # Settings Panel (Collapsible)
  if st.session_state.get('show_settings', False):
      with st.container():
          st.markdown('<div class="settings-panel">', unsafe_allow_html=True)
          st.markdown('<div class="settings-header">⚙️ Settings</div>', unsafe_allow_html=True)
          
          # Model Selection
          model_options = {
              "deepseek-chat": "💬 DeepSeek Chat",
              "deepseek-coder": "💻 DeepSeek Coder", 
              "deepseek-reasoner": "🧠 DeepSeek R1"
          }
          
          col1, col2 = st.columns(2)
          with col1:
              selected_model = st.selectbox(
                  "Model:",
                  options=list(model_options.keys()),
                  format_func=lambda x: model_options[x],
                  key="model_select"
              )
              st.session_state.current_model = selected_model
              
              # R1 specific settings
              if selected_model == "deepseek-reasoner":
                  st.session_state.show_reasoning = st.checkbox(
                      "🔍 Show Reasoning",
                      value=st.session_state.show_reasoning
                  )
          
          with col2:
              # Parameters
              if selected_model == "deepseek-reasoner":
                  temperature = st.slider("Temperature", 0.0, 1.0, 0.3, 0.1)
                  max_tokens = st.slider("Max Tokens", 1000, 8000, 4000, 500)
              else:
                  temperature = st.slider("Temperature", 0.0, 2.0, 0.7, 0.1)
                  max_tokens = st.slider("Max Tokens", 100, 2000, 1000, 100)
          
          # Language & Controls
          col3, col4, col5 = st.columns(3)
          with col3:
              language_options = {
                  "auto": "🌐 Auto",
                  "th": "🇹🇭 Thai",
                  "en": "🇺🇸 English",
                  "zh": "🇨🇳 Chinese"
              }
              selected_language = st.selectbox(
                  "Language:",
                  options=list(language_options.keys()),
                  format_func=lambda x: language_options[x]
              )
          
          with col4:
              if st.button("🗑️ Clear Chat", use_container_width=True):
                  st.session_state.messages = []
                  st.rerun()
          
          with col5:
              st.metric("API Calls", st.session_state.api_calls_count)
          
          st.markdown('</div>', unsafe_allow_html=True)
  else:
      # Default values when settings are hidden
      temperature = 0.3 if st.session_state.current_model == "deepseek-reasoner" else 0.7
      max_tokens = 4000 if st.session_state.current_model == "deepseek-reasoner" else 1000
      selected_language = "auto"

  # Chat Area
  st.markdown('<div class="chat-area">', unsafe_allow_html=True)

  # Welcome Message
  if not st.session_state.messages:
      st.markdown("""
      <div class="message-container">
          <div class="message-avatar assistant-avatar">🧠</div>
          <div class="assistant-message">
              <div class="message-bubble assistant-bubble">
                  👋 สวัสดี! ฉันคือ DeepSeek AI Assistant<br>
                  ฉันพร้อมช่วยเหลือคุณในการ:<br>
                  • 💬 สนทนาทั่วไป<br>
                  • 💻 เขียนโค้ดและ Debug<br>
                  • 🧠 การใช้เหตุผลที่ซับซ้อน<br>
                  • 📊 วิเคราะห์ข้อมูล<br><br>
                  มีอะไรให้ช่วยไหม?
              </div>
          </div>
      </div>
      """, unsafe_allow_html=True)

  # Display Messages
  for message in st.session_state.messages:
      if message["role"] == "user":
          st.markdown(f"""
          <div class="message-container">
              <div class="user-message">
                  <div class="message-bubble user-bubble">
                      {message['content']}
                  </div>
              </div>
              <div class="message-avatar user-avatar">👤</div>
          </div>
          """, unsafe_allow_html=True)
      else:
          # Handle reasoning for R1
          content = message['content']
          reasoning_part = ""
          final_answer = content
          
          if (st.session_state.current_model == "deepseek-reasoner" and 
              st.session_state.show_reasoning and 
              "<think>" in content and "</think>" in content):
              
              start_idx = content.find("<think>") + 7
              end_idx = content.find("</think>")
              reasoning_part = content[start_idx:end_idx].strip()
              final_answer = content[end_idx+8:].strip()
          
          st.markdown(f"""
          <div class="message-container">
              <div class="message-avatar assistant-avatar">🧠</div>
              <div class="assistant-message">
                  <div class="message-bubble assistant-bubble">
                      {final_answer}
                  </div>
              </div>
          </div>
          """, unsafe_allow_html=True)
          
          # Show reasoning if available
          if reasoning_part:
              st.markdown(f"""
              <div class="reasoning-box">
                  <div class="reasoning-header">🧠 Chain of Thought</div>
                  <pre style="white-space: pre-wrap; margin: 0;">{reasoning_part}</pre>
              </div>
              """, unsafe_allow_html=True)

  st.markdown('</div>', unsafe_allow_html=True)

  # API Function
  def call_deepseek_api(messages, model, temperature, max_tokens, language):
      try:
          system_messages = []
          if language != "auto":
              language_prompts = {
                  "th": "กรุณาตอบเป็นภาษาไทย",
                  "en": "Please respond in English",
                  "zh": "请用中文回答"
              }
              if language in language_prompts:
                  system_messages.append({
                      "role": "system", 
                      "content": language_prompts[language]
                  })
          
          if model == "deepseek-reasoner":
              system_messages.append({
                  "role": "system",
                  "content": "คุณเป็น AI ที่มีความสามารถในการใช้เหตุผลแบบลึก กรุณาคิดอย่างเป็นระบบและแสดงขั้นตอนการคิดอย่างชัดเจน"
              })
          
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
              
              if (model == "deepseek-reasoner" and 
                  "reasoning_content" in result["choices"][0]["message"]):
                  reasoning = result["choices"][0]["message"]["reasoning_content"]
                  if reasoning:
                      content = f"<think>\n{reasoning}\n</think>\n\n{content}"
              
              return content
          else:
              return f"❌ Error: HTTP {response.status_code}"
              
      except requests.exceptions.Timeout:
          return "⏰ Request timeout. Please try again."
      except requests.exceptions.ConnectionError:
          return "🌐 Connection error. Please check your internet."
      except Exception as e:
          return f"❌ Error: {str(e)}"

  # Input Area
  st.markdown('<div class="input-container">', unsafe_allow_html=True)

  # Chat Input
  if prompt := st.chat_input("💭 Type your message here...", key="chat_input"):
      # Add user message
      st.session_state.messages.append({"role": "user", "content": prompt})
      
      # Show typing indicator
      with st.spinner("🤔 AI is thinking..."):
          # Call API
          ai_response = call_deepseek_api(
              prompt,
              st.session_state.current_model,
              temperature,
              max_tokens,
              selected_language
          )
          
          st.session_state.api_calls_count += 1
          st.session_state.messages.append({"role": "assistant", "content": ai_response})
      
      st.rerun()

  st.markdown('</div>', unsafe_allow_html=True)
  st.markdown('</div>', unsafe_allow_html=True)

  # Quick Actions (if no messages)
  if not st.session_state.messages:
      st.markdown("### 🚀 Quick Start")
      col1, col2, col3, col4 = st.columns(4)
      
      quick_prompts = [
          "สวัสดี! คุณช่วยอะไรได้บ้าง?",
          "เขียนโค้ด Python สำหรับ Hello World",
          "อธิบายการทำงานของ AI",
          "แก้สมการ: x² + 5x - 6 = 0"
      ]
      
      for i, (col, prompt) in enumerate(zip([col1, col2, col3, col4], quick_prompts)):
          with col:
              if st.button(f"💡 {prompt[:20]}...", key=f"quick_{i}", use_container_width=True):
                  st.session_state.messages.append({"role": "user", "content": prompt})
                  
                  with st.spinner("🤔 AI is thinking..."):
                      ai_response = call_deepseek_api(
                          prompt,
                          st.session_state.current_model,
                          temperature,
                          max_tokens,
                          selected_language
                      )
                      
                      st.session_state.api_calls_count += 1
                      st.session_state.messages.append({"role": "assistant", "content": ai_response})
                  
                  st.rerun()
