#!/usr/bin/env python3
"""
KodeKey ChatGPT-Style Chatbot - Improved Version
A beautiful, modern chatbot with persistent conversation memory and multiple AI models
"""

import streamlit as st
import openai
from openai import OpenAI
import uuid
import json
import os
from datetime import datetime
from typing import Dict, List, Optional
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="KodeKey AI Chat",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern ChatGPT-style interface
st.markdown("""
<style>
    /* Main container styling */
    .stApp {
        background-color: #f5f5f5;
    }
    
    /* Chat message styling */
    .chat-message {
        padding: 1.2rem;
        border-radius: 0.8rem;
        margin: 0.8rem 0;
        display: flex;
        align-items: flex-start;
        animation: fadeIn 0.3s ease-in;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .user-message {
        background: linear-gradient(135deg, #7c3aed 0%, #a855f7 100%);
        margin-left: 20%;
        box-shadow: 0 4px 15px rgba(124, 58, 237, 0.3);
        border: 1px solid rgba(168, 85, 247, 0.3);
        color: white;
    }
    
    .assistant-message {
        background: white;
        margin-right: 20%;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        border: 1px solid #e5e5e5;
        color: #1f2937;
    }
    
    /* Avatar styling */
    .avatar {
        width: 2.5rem;
        height: 2.5rem;
        border-radius: 50%;
        margin-right: 1rem;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.2rem;
        flex-shrink: 0;
    }
    
    .user-avatar {
        background: rgba(124, 58, 237, 0.2);
        border: 2px solid rgba(168, 85, 247, 0.4);
        color: #7c3aed;
    }
    
    .assistant-avatar {
        background: #f3f4f6;
        border: 2px solid #e5e7eb;
        color: #6b7280;
    }
    
    /* Sidebar styling */
    .css-1d391kg, .css-1544g2n {
        background-color: white;
        border-right: 1px solid #e5e5e5;
    }
    
    /* Sidebar text and labels */
    .css-1d391kg p, .css-1d391kg label, .css-1544g2n p, .css-1544g2n label {
        color: #1f2937 !important;
    }
    
    /* Sidebar headers */
    .css-1d391kg h1, .css-1d391kg h2, .css-1d391kg h3,
    .css-1544g2n h1, .css-1544g2n h2, .css-1544g2n h3 {
        color: #1f2937 !important;
    }
    
    /* Sidebar input fields */
    .css-1d391kg input, .css-1544g2n input {
        background-color: #f9fafb !important;
        color: #1f2937 !important;
        border: 1px solid #e5e5e5 !important;
    }
    
    /* Sidebar text input */
    .css-1d391kg .stTextInput input, .css-1544g2n .stTextInput input {
        background-color: #f9fafb !important;
        color: #1f2937 !important;
        border: 1px solid #e5e5e5 !important;
    }
    
    /* Sidebar buttons */
    .css-1d391kg .stButton button, .css-1544g2n .stButton button {
        color: white !important;
    }
    
    /* Ensure purple buttons in sidebar have white text */
    [data-testid="stSidebar"] .stButton button[kind="primary"],
    [data-testid="stSidebar"] .stButton button {
        color: white !important;
    }
    
    /* Conversation buttons with gradient */
    button[kind="primary"] {
        color: white !important;
    }
    
    /* Conversation item styling */
    .conversation-item {
        background: #f9fafb;
        border: 1px solid #e5e5e5;
        border-radius: 0.8rem;
        padding: 0.8rem;
        margin: 0.5rem 0;
        cursor: pointer;
        transition: all 0.3s ease;
        color: #1f2937;
    }
    
    .conversation-item:hover {
        transform: translateX(5px);
        box-shadow: 0 4px 15px rgba(124, 58, 237, 0.3);
        border-color: #7c3aed;
    }
    
    .conversation-item.active {
        background: linear-gradient(135deg, #7c3aed 0%, #a855f7 100%);
        box-shadow: 0 4px 15px rgba(124, 58, 237, 0.4);
        color: white !important;
    }
    
    .conversation-item.active * {
        color: white !important;
    }
    
    /* Input styling */
    .stTextArea textarea {
        background-color: white;
        color: #1f2937;
        border: 2px solid #e5e5e5;
        border-radius: 0.8rem;
        padding: 1rem;
        font-size: 1rem;
        transition: all 0.3s ease;
    }
    
    .stTextArea textarea:focus {
        border-color: #7c3aed;
        box-shadow: 0 0 0 2px rgba(124, 58, 237, 0.3);
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #7c3aed 0%, #a855f7 100%);
        color: white;
        border: none;
        padding: 0.6rem 1.2rem;
        border-radius: 0.6rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(124, 58, 237, 0.5);
    }
    
    /* Quick action buttons */
    .quick-action {
        background: #f9fafb;
        border: 2px solid #e5e5e5;
        color: #1f2937;
        padding: 0.8rem;
        border-radius: 0.6rem;
        text-align: center;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .quick-action:hover {
        border-color: #7c3aed;
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(124, 58, 237, 0.3);
    }
    
    /* Title styling */
    h1, h2, h3 {
        color: #1f2937 !important;
    }
    
    /* Improve text readability */
    .stMarkdown, .stText {
        color: #1f2937 !important;
    }
    
    /* Select box styling */
    .stSelectbox label, .stSlider label {
        color: #1f2937 !important;
    }
    
    /* Sidebar specific overrides */
    section[data-testid="stSidebar"] {
        background-color: white;
    }
    
    section[data-testid="stSidebar"] * {
        color: #1f2937;
    }
    
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] h4,
    section[data-testid="stSidebar"] h5,
    section[data-testid="stSidebar"] h6 {
        color: #1f2937 !important;
    }
    
    section[data-testid="stSidebar"] .stTextInput input {
        background-color: #f9fafb !important;
        color: #1f2937 !important;
        border: 1px solid #e5e5e5 !important;
    }
    
    section[data-testid="stSidebar"] .stSelectbox select {
        background-color: #f9fafb !important;
        color: #1f2937 !important;
        border: 1px solid #e5e5e5 !important;
    }
    
    section[data-testid="stSidebar"] .stMarkdown {
        color: #1f2937 !important;
    }
    
    /* Improve message text contrast */
    .chat-message .stMarkdown {
        font-size: 1rem;
        line-height: 1.6;
    }
    
    .user-message .stMarkdown {
        color: white !important;
    }
    
    .assistant-message .stMarkdown {
        color: #1f2937 !important;
    }
    
    /* Welcome message */
    .welcome-message {
        text-align: center;
        padding: 3rem;
        color: #6b7280;
    }
    
    .welcome-title {
        font-size: 2rem;
        background: linear-gradient(135deg, #7c3aed 0%, #a855f7 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Constants
AVAILABLE_MODELS = {
    "Claude Sonnet 4": "anthropic/claude-sonnet-4",
    "GPT-4o (Nov 2024)": "openai/gpt-4o-2024-11-20",
    "GPT-4.1": "openai/gpt-4.1",
    "Gemini 2.5 Pro": "google/gemini-2.5-pro",
    "Grok 3": "x-ai/grok-3"
}

PERSONALITIES = {
    "🤖 Assistant": "You are a helpful, harmless, and honest AI assistant. Provide clear, accurate, and helpful responses.",
    "💻 Developer": "You are an expert software developer. Help with coding questions, debugging, best practices, and technical architecture.",
    "📚 Teacher": "You are a patient and knowledgeable teacher. Explain concepts clearly with examples and encourage learning.",
    "🎨 Creative": "You are a creative AI assistant. Help with writing, brainstorming, and creative projects with imagination and flair.",
    "📊 Analyst": "You are a data analyst and researcher. Provide detailed analysis, insights, and evidence-based responses."
}

QUICK_ACTIONS = {
    "🔍 Explain": "Can you explain this concept in simple terms?",
    "🐛 Debug": "Help me debug this code issue",
    "✨ Create": "Help me create something new",
    "📈 Analyze": "Analyze this data or situation"
}

# Ensure conversations directory exists
CONVERSATIONS_DIR = Path("conversations")
CONVERSATIONS_DIR.mkdir(exist_ok=True)

class ChatBot:
    def __init__(self, api_key: str = None, base_url: str = None):
        """Initialize the chatbot with KodeKey configuration."""
        self.api_key = api_key or os.getenv("KEYSPACES_API_KEY") or os.getenv("KODEKEY_API_KEY")
        self.base_url = base_url or os.getenv("KEYSPACES_BASE_URL") or os.getenv("KODEKEY_BASE_URL") or "https://main.kk-ai-keys.kodekloud.com/v1"
        
        if not self.api_key:
            raise ValueError("KeySpaces API key is required")
        
        # Initialize OpenAI client with KodeKey
        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url
        )
    
    def stream_response(self, messages: List[Dict], model: str, temperature: float = 0.7):
        """Stream response from the AI model."""
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=2000,
                stream=True
            )
            
            for chunk in response:
                if chunk.choices[0].delta.content is not None:
                    yield chunk.choices[0].delta.content
                    
        except Exception as e:
            yield f"❌ Error: {str(e)}"

def load_conversations():
    """Load all conversations from JSON files."""
    conversations = {}
    for file_path in CONVERSATIONS_DIR.glob("*.json"):
        try:
            with open(file_path, 'r') as f:
                conversation = json.load(f)
                conversations[file_path.stem] = conversation
        except Exception as e:
            st.error(f"Error loading conversation {file_path.name}: {str(e)}")
    return conversations

def save_conversation(conversation_id: str, conversation: Dict):
    """Save a conversation to a JSON file."""
    file_path = CONVERSATIONS_DIR / f"{conversation_id}.json"
    with open(file_path, 'w') as f:
        json.dump(conversation, f, indent=2)

def delete_conversation_file(conversation_id: str):
    """Delete a conversation JSON file."""
    file_path = CONVERSATIONS_DIR / f"{conversation_id}.json"
    if file_path.exists():
        file_path.unlink()

def initialize_session_state():
    """Initialize session state variables."""
    if "conversations" not in st.session_state:
        st.session_state.conversations = load_conversations()
    
    if "active_conversation" not in st.session_state:
        if st.session_state.conversations:
            # Use the most recent conversation
            st.session_state.active_conversation = sorted(
                st.session_state.conversations.items(),
                key=lambda x: x[1].get("updated_at", x[1].get("created_at", "")),
                reverse=True
            )[0][0]
        else:
            # Create first conversation
            create_new_conversation()
    
    if "chatbot" not in st.session_state:
        st.session_state.chatbot = None
    
    # Auto-load API key from .env if available
    if "api_key" not in st.session_state:
        env_key = os.getenv("KEYSPACES_API_KEY") or os.getenv("KODEKEY_API_KEY")
        if env_key:
            st.session_state.api_key = env_key
            try:
                st.session_state.chatbot = ChatBot(env_key)
            except Exception:
                pass

def create_new_conversation():
    """Create a new conversation."""
    conversation_id = str(uuid.uuid4())
    conversation = {
        "title": "New Chat",
        "messages": [],
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
        "model": "anthropic/claude-sonnet-4",
        "personality": "🤖 Assistant",
        "temperature": 0.7
    }
    st.session_state.conversations[conversation_id] = conversation
    save_conversation(conversation_id, conversation)
    st.session_state.active_conversation = conversation_id
    return conversation_id

def delete_conversation(conversation_id: str):
    """Delete a conversation."""
    if len(st.session_state.conversations) > 1:
        del st.session_state.conversations[conversation_id]
        delete_conversation_file(conversation_id)
        if st.session_state.active_conversation == conversation_id:
            # Switch to first available conversation
            st.session_state.active_conversation = list(st.session_state.conversations.keys())[0]

def get_conversation_title(messages: List[Dict]) -> str:
    """Generate a title for the conversation based on first message."""
    if not messages:
        return "New Chat"
    
    first_message = next((msg for msg in messages if msg["role"] == "user"), None)
    if first_message:
        content = first_message["content"]
        # Take first 40 characters and clean up
        title = content[:40].strip()
        if len(content) > 40:
            title += "..."
        return title
    
    return "New Chat"

def search_conversations(query: str) -> List[str]:
    """Search through all conversations."""
    if not query:
        return list(st.session_state.conversations.keys())
    
    query_lower = query.lower()
    matching_conversations = []
    
    for conv_id, conv_data in st.session_state.conversations.items():
        # Search in title
        if query_lower in conv_data.get("title", "").lower():
            matching_conversations.append(conv_id)
            continue
        
        # Search in messages
        for message in conv_data.get("messages", []):
            if query_lower in message.get("content", "").lower():
                matching_conversations.append(conv_id)
                break
    
    return matching_conversations

def render_message(message: Dict, is_user: bool = True):
    """Render a chat message with styling."""
    avatar = "👤" if is_user else "🤖"
    css_class = "user-message" if is_user else "assistant-message"
    avatar_class = "user-avatar" if is_user else "assistant-avatar"
    
    # Escape HTML in message content for security
    import html
    escaped_content = html.escape(message["content"])
    
    st.markdown(f"""
    <div class="chat-message {css_class}">
        <div class="avatar {avatar_class}">{avatar}</div>
        <div style="flex: 1;">
            <div style="line-height: 1.6; white-space: pre-wrap; font-size: 1rem;">{escaped_content}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def main():
    """Main Streamlit application."""
    
    # Initialize session state
    initialize_session_state()
    
    # Sidebar
    with st.sidebar:
        st.markdown("## ⚙️ Configuration")
        
        # API Key input
        api_key = st.text_input(
            "KeySpaces API Key",
            type="password",
            value=st.session_state.get("api_key", ""),
            placeholder="sk-kkAI-...",
            help="Enter your KeySpaces API key"
        )
        
        if api_key:
            st.session_state.api_key = api_key
            try:
                if st.session_state.chatbot is None or st.session_state.chatbot.api_key != api_key:
                    st.session_state.chatbot = ChatBot(api_key)
                st.success("✅ API key configured")
            except Exception as e:
                st.error(f"❌ Invalid API key: {str(e)}")
                st.session_state.chatbot = None
        elif st.session_state.get("api_key"):
            st.success("✅ API key configured")
        
        st.divider()
        
        # Model and personality settings
        if st.session_state.chatbot and st.session_state.active_conversation:
            active_conv = st.session_state.conversations[st.session_state.active_conversation]
            
            st.markdown("## 🎭 Chat Settings")
            
            # Model selection
            model_names = list(AVAILABLE_MODELS.keys())
            current_model_name = next(
                (name for name, model_id in AVAILABLE_MODELS.items() 
                 if model_id == active_conv.get("model", "anthropic/claude-sonnet-4")), 
                model_names[0]
            )
            
            selected_model = st.selectbox(
                "AI Model",
                model_names,
                index=model_names.index(current_model_name),
                help="Choose the AI model for this conversation"
            )
            
            # Personality selection
            personality = st.selectbox(
                "Personality",
                list(PERSONALITIES.keys()),
                index=list(PERSONALITIES.keys()).index(active_conv.get("personality", "🤖 Assistant")),
                help="Choose the AI personality"
            )
            
            # Temperature setting
            temperature = st.slider(
                "Creativity",
                min_value=0.0,
                max_value=1.0,
                value=active_conv.get("temperature", 0.7),
                step=0.1,
                help="Higher values make responses more creative"
            )
            
            # Update conversation settings
            active_conv.update({
                "model": AVAILABLE_MODELS[selected_model],
                "personality": personality,
                "temperature": temperature,
                "updated_at": datetime.now().isoformat()
            })
            save_conversation(st.session_state.active_conversation, active_conv)
            
            st.divider()
        
        # Conversation management
        st.markdown("## 💬 Conversations")
        
        # New conversation button
        if st.button("➕ New Chat", use_container_width=True):
            new_id = create_new_conversation()
            st.rerun()
        
        # Search conversations
        search_query = st.text_input("🔍 Search conversations", placeholder="Search...")
        
        # Conversation list
        matching_conversations = search_conversations(search_query)
        
        for conv_id in matching_conversations:
            conv_data = st.session_state.conversations[conv_id]
            is_active = conv_id == st.session_state.active_conversation
            
            # Conversation item
            col1, col2 = st.columns([5, 1])
            
            with col1:
                title = get_conversation_title(conv_data["messages"])
                if st.button(
                    title,
                    key=f"conv_{conv_id}",
                    use_container_width=True,
                    type="primary" if is_active else "secondary"
                ):
                    st.session_state.active_conversation = conv_id
                    st.rerun()
                
                # Show preview of last message
                if conv_data["messages"]:
                    last_msg = conv_data["messages"][-1]["content"][:50] + "..."
                    st.caption(last_msg)
            
            with col2:
                if st.button("🗑️", key=f"del_{conv_id}", help="Delete conversation"):
                    delete_conversation(conv_id)
                    st.rerun()
    
    # Main chat interface
    if not st.session_state.chatbot:
        st.markdown("""
        <div class="welcome-message">
            <h1 class="welcome-title">Welcome to KeySpaces AI Chat</h1>
            <p>Please enter your KeySpaces API key in the sidebar to start chatting!</p>
            <p>Don't have a KeySpaces API key? Get one at <a href="https://learn.kodekloud.com/user/playgrounds/keyspace" target="_blank">KodeKloud KeySpaces</a></p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    if not st.session_state.active_conversation:
        st.error("❌ No active conversation. Please create a new chat.")
        return
    
    # Get active conversation
    active_conv = st.session_state.conversations[st.session_state.active_conversation]
    
    # Header
    st.markdown(f"# 💬 {get_conversation_title(active_conv['messages'])}")
    
    # Chat messages container
    chat_container = st.container()
    
    with chat_container:
        # Display chat history
        if active_conv["messages"]:
            for message in active_conv["messages"]:
                if message["role"] == "user":
                    render_message(message, is_user=True)
                elif message["role"] == "assistant":
                    render_message(message, is_user=False)
        else:
            st.markdown("""
            <div class="welcome-message">
                <p>👋 Hello! I'm your AI assistant powered by KeySpaces. How can I help you today?</p>
                <p>Try one of the quick actions below or type your own message!</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Input section
    st.divider()
    
    # Quick action buttons
    col1, col2, col3, col4 = st.columns(4)
    
    quick_action_clicked = None
    with col1:
        if st.button("🔍 Explain", use_container_width=True, key="explain_btn"):
            quick_action_clicked = QUICK_ACTIONS["🔍 Explain"]
    
    with col2:
        if st.button("🐛 Debug", use_container_width=True, key="debug_btn"):
            quick_action_clicked = QUICK_ACTIONS["🐛 Debug"]
    
    with col3:
        if st.button("✨ Create", use_container_width=True, key="create_btn"):
            quick_action_clicked = QUICK_ACTIONS["✨ Create"]
    
    with col4:
        if st.button("📈 Analyze", use_container_width=True, key="analyze_btn"):
            quick_action_clicked = QUICK_ACTIONS["📈 Analyze"]
    
    # Chat input
    with st.form(key="chat_form", clear_on_submit=True):
        col1, col2 = st.columns([5, 1])
        
        with col1:
            user_input = st.text_area(
                "Ask me anything...",
                key="user_input",
                height=100,
                placeholder="Type your message here...",
                label_visibility="collapsed",
                value=quick_action_clicked or ""
            )
        
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            submit_button = st.form_submit_button(
                "✉️ Send",
                use_container_width=True,
                type="primary"
            )
    
    # Process user input
    if (submit_button or quick_action_clicked) and (user_input or quick_action_clicked):
        user_message = user_input or quick_action_clicked
        
        # Add user message to conversation
        active_conv["messages"].append({
            "role": "user",
            "content": user_message.strip()
        })
        
        # Update conversation title if it's the first message
        if len(active_conv["messages"]) == 1:
            active_conv["title"] = get_conversation_title(active_conv["messages"])
        
        # Update timestamp
        active_conv["updated_at"] = datetime.now().isoformat()
        
        # Save conversation
        save_conversation(st.session_state.active_conversation, active_conv)
        
        # Prepare messages for API
        messages = [
            {
                "role": "system",
                "content": PERSONALITIES[active_conv["personality"]]
            }
        ]
        
        # Add conversation history (keep last 10 exchanges)
        recent_messages = active_conv["messages"][-20:]
        messages.extend(recent_messages)
        
        # Generate response with streaming
        with st.chat_message("assistant"):
            response_container = st.empty()
            response_text = ""
            
            try:
                for chunk in st.session_state.chatbot.stream_response(
                    messages,
                    active_conv["model"],
                    active_conv["temperature"]
                ):
                    response_text += chunk
                    response_container.markdown(response_text + "▌")
                
                # Final response without cursor
                response_container.markdown(response_text)
                
                # Add assistant response to conversation
                active_conv["messages"].append({
                    "role": "assistant",
                    "content": response_text
                })
                
                # Save updated conversation
                save_conversation(st.session_state.active_conversation, active_conv)
                
            except Exception as e:
                error_msg = f"❌ Error generating response: {str(e)}"
                response_container.error(error_msg)
                active_conv["messages"].append({
                    "role": "assistant",
                    "content": error_msg
                })
                save_conversation(st.session_state.active_conversation, active_conv)
        
        # Rerun to show the updated conversation
        st.rerun()

if __name__ == "__main__":
    main()% 
