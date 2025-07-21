import streamlit as st
import requests
import json
import time
from typing import Dict, List, Optional
import re
from datetime import datetime
import subprocess
import tempfile
import os
import sys

# Page configuration
st.set_page_config(
    page_title="LLM Coding Assistant",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
.main-header {
    text-align: center;
    padding: 1rem 0;
    background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    color: white;
    border-radius: 10px;
    margin-bottom: 2rem;
}
.chat-message {
    padding: 1rem;
    margin: 0.5rem 0;
    border-radius: 10px;
    border-left: 4px solid #667eea;
    background-color: #f8f9fa;
}
.user-message {
    border-left-color: #28a745;
    background-color: #e8f5e9;
}
.assistant-message {
    border-left-color: #667eea;
    background-color: #f0f2ff;
}
.code-block {
    background-color: #1e1e1e;
    color: #d4d4d4;
    padding: 1rem;
    border-radius: 8px;
    margin: 0.5rem 0;
    overflow-x: auto;
}
.language-badge {
    display: inline-block;
    background-color: #667eea;
    color: white;
    padding: 0.2rem 0.5rem;
    border-radius: 15px;
    font-size: 0.8rem;
    margin-bottom: 0.5rem;
}
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'api_key' not in st.session_state:
    st.session_state.api_key = ""
if 'model' not in st.session_state:
    st.session_state.model = "llama-3.1-8b-instant"
if 'temperature' not in st.session_state:
    st.session_state.temperature = 0.1
if 'max_tokens' not in st.session_state:
    st.session_state.max_tokens = 4000

# Supported programming languages
SUPPORTED_LANGUAGES = {
    'python': {'extension': '.py', 'runner': 'python'},
    'javascript': {'extension': '.js', 'runner': 'node'},
    'java': {'extension': '.java', 'runner': 'java'},
    'cpp': {'extension': '.cpp', 'runner': 'g++'},
    'c': {'extension': '.c', 'runner': 'gcc'},
    'go': {'extension': '.go', 'runner': 'go run'},
    'rust': {'extension': '.rs', 'runner': 'rustc'},
    'php': {'extension': '.php', 'runner': 'php'},
    'ruby': {'extension': '.rb', 'runner': 'ruby'},
    'swift': {'extension': '.swift', 'runner': 'swift'},
    'kotlin': {'extension': '.kt', 'runner': 'kotlinc'},
    'typescript': {'extension': '.ts', 'runner': 'ts-node'},
    'bash': {'extension': '.sh', 'runner': 'bash'},
    'powershell': {'extension': '.ps1', 'runner': 'powershell'},
    'sql': {'extension': '.sql', 'runner': 'sqlite3'},
    'html': {'extension': '.html', 'runner': 'browser'},
    'css': {'extension': '.css', 'runner': 'browser'},
    'r': {'extension': '.r', 'runner': 'Rscript'},
    'matlab': {'extension': '.m', 'runner': 'octave'}
}

# Updated list of working Groq models (as of 2024)
GROQ_MODELS = {
    "llama-3.1-8b-instant": "Llama 3.1 8B (Fastest)",
    "llama-3.1-70b-versatile": "Llama 3.1 70B (Most Capable)",
    "llama-3.2-1b-preview": "Llama 3.2 1B (Preview)",
    "llama-3.2-3b-preview": "Llama 3.2 3B (Preview)",
    "mixtral-8x7b-32768": "Mixtral 8x7B",
    "gemma2-9b-it": "Gemma 2 9B",
    "gemma-7b-it": "Gemma 7B",
    "llama3-8b-8192": "Llama 3 8B (Legacy)",
    "llama3-70b-8192": "Llama 3 70B (Legacy)"
}

def get_system_prompt() -> str:
    """Enhanced system prompt for coding tasks."""
    return """You are CodeMaster AI, an expert programming assistant specializing in:

1. **Code Generation**: Write clean, efficient, and well-documented code
2. **Multi-language Support**: Proficient in Python, JavaScript, Java, C++, C, Go, Rust, PHP, Ruby, Swift, Kotlin, TypeScript, and more
3. **Problem Solving**: Break down complex programming problems into manageable steps
4. **Code Review**: Analyze and improve existing code for performance and readability
5. **Debugging**: Identify and fix bugs with detailed explanations
6. **Best Practices**: Follow industry standards and coding conventions
7. **Documentation**: Provide clear explanations and inline comments

**Response Format Guidelines:**
- Always specify the programming language when providing code
- Use proper code formatting and syntax highlighting
- Include comments explaining complex logic
- Provide working examples when possible
- Suggest optimizations and alternatives when relevant
- Be concise but thorough in explanations

**Code Quality Standards:**
- Write production-ready code
- Follow language-specific conventions
- Include error handling where appropriate
- Optimize for readability and maintainability
- Test edge cases when relevant

Focus on delivering fast, accurate, and practical solutions."""

def call_llm_api(messages: List[Dict], api_key: str, model: str, temperature: float, max_tokens: int) -> Optional[str]:
    """Call Groq API with enhanced error handling and retry logic."""
    try:
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        
        data = {
            'model': model,
            'messages': messages,
            'temperature': temperature,
            'max_tokens': max_tokens,
            'stream': False
        }
        
        # Add retry logic for failed requests
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = requests.post(
                    'https://api.groq.com/openai/v1/chat/completions',
                    headers=headers,
                    json=data,
                    timeout=60  # Increased timeout
                )
                
                if response.status_code == 200:
                    result = response.json()
                    if 'choices' in result and len(result['choices']) > 0:
                        return result['choices'][0]['message']['content']
                    else:
                        st.error("Unexpected API response format")
                        return None
                elif response.status_code == 401:
                    st.error("❌ Invalid API key. Please check your Groq API key.")
                    return None
                elif response.status_code == 429:
                    st.warning(f"⏳ Rate limit exceeded. Retrying in {2**attempt} seconds...")
                    time.sleep(2**attempt)
                    continue
                else:
                    error_detail = ""
                    try:
                        error_response = response.json()
                        if 'error' in error_response:
                            error_detail = error_response['error'].get('message', '')
                    except:
                        error_detail = response.text
                    
                    st.error(f"❌ API Error ({response.status_code}): {error_detail}")
                    return None
                    
            except requests.exceptions.Timeout:
                if attempt < max_retries - 1:
                    st.warning(f"⏳ Request timed out. Retrying... (Attempt {attempt + 2})")
                    continue
                else:
                    st.error("❌ Request timed out after multiple attempts")
                    return None
            except requests.exceptions.RequestException as e:
                if attempt < max_retries - 1:
                    st.warning(f"⏳ Connection error. Retrying... (Attempt {attempt + 2})")
                    time.sleep(1)
                    continue
                else:
                    st.error(f"❌ Connection failed: {str(e)}")
                    return None
        
        return None
            
    except Exception as e:
        st.error(f"❌ Unexpected error: {str(e)}")
        return None

def extract_code_blocks(text: str) -> List[Dict]:
    """Extract code blocks from markdown text."""
    pattern = r'```(\w+)?\n(.*?)```'
    matches = re.findall(pattern, text, re.DOTALL)
    
    code_blocks = []
    for match in matches:
        language = match[0] if match[0] else 'text'
        code = match[1].strip()
        code_blocks.append({
            'language': language,
            'code': code
        })
    
    return code_blocks

def run_code(code: str, language: str) -> tuple:
    """Execute code safely in a temporary environment."""
    if language not in SUPPORTED_LANGUAGES:
        return False, f"Language {language} not supported for execution"
    
    try:
        with tempfile.NamedTemporaryFile(
            mode='w', 
            suffix=SUPPORTED_LANGUAGES[language]['extension'],
            delete=False
        ) as tmp_file:
            tmp_file.write(code)
            tmp_file_path = tmp_file.name
        
        if language == 'python':
            result = subprocess.run(
                [sys.executable, tmp_file_path],
                capture_output=True,
                text=True,
                timeout=10
            )
        elif language == 'javascript':
            result = subprocess.run(
                ['node', tmp_file_path],
                capture_output=True,
                text=True,
                timeout=10
            )
        else:
            return False, f"Execution for {language} not implemented in this demo"
        
        # Clean up
        os.unlink(tmp_file_path)
        
        if result.returncode == 0:
            return True, result.stdout
        else:
            return False, result.stderr
            
    except subprocess.TimeoutExpired:
        return False, "Code execution timed out"
    except Exception as e:
        return False, f"Execution error: {str(e)}"

def display_message(message: Dict, is_user: bool = False):
    """Display chat message with proper formatting."""
    css_class = "user-message" if is_user else "assistant-message"
    
    with st.container():
        st.markdown(f"""
        <div class="chat-message {css_class}">
            <strong>{'You' if is_user else 'CodeMaster AI'}</strong>
            <small style="color: #666; margin-left: 10px;">
                {message.get('timestamp', datetime.now().strftime('%H:%M:%S'))}
            </small>
        </div>
        """, unsafe_allow_html=True)
        
        # Display message content
        if is_user:
            st.markdown(message['content'])
        else:
            # Parse and display assistant message with code blocks
            content = message['content']
            code_blocks = extract_code_blocks(content)
            
            if code_blocks:
                # Display text and code blocks separately
                lines = content.split('\n')
                current_text = []
                in_code_block = False
                
                for line in lines:
                    if line.strip().startswith('```'):
                        if current_text and not in_code_block:
                            st.markdown('\n'.join(current_text))
                            current_text = []
                        in_code_block = not in_code_block
                    elif not in_code_block:
                        current_text.append(line)
                
                if current_text:
                    st.markdown('\n'.join(current_text))
                
                # Display code blocks with execution option
                for i, block in enumerate(code_blocks):
                    st.markdown(f'<div class="language-badge">{block["language"].upper()}</div>', 
                              unsafe_allow_html=True)
                    st.code(block['code'], language=block['language'])
                    
                    # Add execution button for supported languages
                    if block['language'] in ['python', 'javascript']:
                        col1, col2 = st.columns([1, 4])
                        with col1:
                            if st.button(f"▶️ Run", key=f"run_{i}_{len(st.session_state.messages)}"):
                                with st.spinner("Executing code..."):
                                    success, output = run_code(block['code'], block['language'])
                                    if success:
                                        st.success("Code executed successfully!")
                                        if output.strip():
                                            st.code(output, language='text')
                                    else:
                                        st.error("Execution failed!")
                                        st.code(output, language='text')
            else:
                st.markdown(content)

# Sidebar configuration
with st.sidebar:
    st.markdown("### ⚙️ Configuration")
    
    # API Configuration
    st.markdown("#### API Settings")
    api_key = st.text_input(
        "Groq API Key", 
        type="password", 
        value=st.session_state.api_key,
        placeholder="Enter your Groq API key",
        help="Get your free API key from https://console.groq.com/"
    )
    
    # Model selection with updated working models
    model_keys = list(GROQ_MODELS.keys())
    model_labels = [GROQ_MODELS[key] for key in model_keys]
    
    selected_index = 0
    if st.session_state.model in model_keys:
        selected_index = model_keys.index(st.session_state.model)
    
    selected_model_index = st.selectbox(
        "Model",
        range(len(model_keys)),
        format_func=lambda x: model_labels[x],
        index=selected_index,
        help="Choose from available Groq models"
    )
    
    model = model_keys[selected_model_index]
    
    temperature = st.slider(
        "Temperature (Creativity)",
        min_value=0.0,
        max_value=1.0,
        value=st.session_state.temperature,
        step=0.1,
        help="Lower values = more focused, Higher values = more creative"
    )
    
    max_tokens = st.slider(
        "Max Tokens",
        min_value=500,
        max_value=32768,
        value=st.session_state.max_tokens,
        step=500,
        help="Maximum response length"
    )
    
    # Update session state
    st.session_state.api_key = api_key
    st.session_state.model = model
    st.session_state.temperature = temperature
    st.session_state.max_tokens = max_tokens
    
    st.markdown("---")
    
    # Model status indicator
    st.markdown("#### 🔋 Model Status")
    if model in ["llama-3.1-8b-instant", "llama-3.1-70b-versatile"]:
        st.success("✅ Recommended (Latest)")
    elif model in ["mixtral-8x7b-32768", "gemma2-9b-it"]:
        st.info("ℹ️ Alternative Option")
    else:
        st.warning("⚠️ Legacy Model")
    
    # Quick Actions
    st.markdown("#### 🚀 Quick Actions")
    
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()
    
    if st.button("📊 Show Stats"):
        st.info(f"Messages: {len(st.session_state.messages)}")
        if st.session_state.messages:
            total_chars = sum(len(msg['content']) for msg in st.session_state.messages)
            st.info(f"Total Characters: {total_chars:,}")
    
    # Test API Connection
    if st.button("🔌 Test API Connection"):
        if not api_key:
            st.error("Please enter your API key first")
        else:
            with st.spinner("Testing connection..."):
                test_response = call_llm_api(
                    [{"role": "user", "content": "Hello, just testing the connection. Please respond with 'Connection successful!'"}],
                    api_key, model, 0.1, 100
                )
                if test_response:
                    st.success("✅ Connection successful!")
                else:
                    st.error("❌ Connection failed")
    
    st.markdown("---")
    
    # Supported Languages
    st.markdown("#### 📝 Supported Languages")
    st.markdown("""
    - **Web**: HTML, CSS, JavaScript, TypeScript
    - **Backend**: Python, Java, C++, C, Go, Rust
    - **Mobile**: Swift, Kotlin, Java
    - **Scripting**: Bash, PowerShell, PHP, Ruby
    - **Data**: SQL, R, MATLAB
    - **And many more...**
    """)

# Main interface
st.markdown("""
<div class="main-header">
    <h1>CodeLLM</h1>
    <p>LLM Coding Assistant by Groq</p>
</div>
""", unsafe_allow_html=True)

# API Key check
if not st.session_state.api_key:
    st.warning("⚠️ Please enter your Groq API key in the sidebar to start coding!")
    st.info("📝 Get your free API key at: https://console.groq.com/")

# Display chat messages
for message in st.session_state.messages:
    display_message(message, message['role'] == 'user')

# Chat input
if prompt := st.chat_input("Ask me anything about coding, debugging, or programming..."):
    if not st.session_state.api_key:
        st.error("Please enter your Groq API key in the sidebar to continue.")
        st.stop()
    
    # Add user message
    user_message = {
        'role': 'user',
        'content': prompt,
        'timestamp': datetime.now().strftime('%H:%M:%S')
    }
    st.session_state.messages.append(user_message)
    
    # Display user message
    display_message(user_message, True)
    
    # Generate assistant response
    with st.spinner("🤖 CodeMaster AI is thinking..."):
        # Prepare messages for API
        api_messages = [{'role': 'system', 'content': get_system_prompt()}]
        api_messages.extend([
            {'role': msg['role'], 'content': msg['content']} 
            for msg in st.session_state.messages[-10:]  # Last 10 messages for context
        ])
        
        # Call LLM API
        response = call_llm_api(
            api_messages,
            st.session_state.api_key,
            st.session_state.model,
            st.session_state.temperature,
            st.session_state.max_tokens
        )
        
        if response:
            # Add assistant message
            assistant_message = {
                'role': 'assistant',
                'content': response,
                'timestamp': datetime.now().strftime('%H:%M:%S')
            }
            st.session_state.messages.append(assistant_message)
            
            # Display assistant message
            display_message(assistant_message, False)
        else:
            st.error("❌ Failed to generate response. Please check your API key and connection.")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <p>💡 <strong>Tip:</strong> Be specific with your coding requests for better results!</p>
</div>
""", unsafe_allow_html=True)
