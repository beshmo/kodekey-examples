#!/usr/bin/env python3
"""
KodeKey ChatGPT-Style Chatbot
A modern chatbot with conversation memory, tabs, and multiple AI models
using KodeKey's unified API access through OpenAI SDK.
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

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="KodeKey AI Chat",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .stApp {
        background-color: #0e1117;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.8rem;
        margin: 0.5rem 0;
        display: flex;
        align-items: flex-start;
    }
    .user-message {
        background-color: #2d3748;
        margin-left: 2rem;
    }
    .assistant-message {
        background-color: #1a202c;
        margin-right: 2rem;
    }
    .avatar {
        width: 2rem;
        height: 2rem;
        border-radius: 50%;
        margin-right: 0.5rem;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1rem;
    }
    .user-avatar {
        background-color: #4a5568;
    }
    .assistant-avatar {
        background-color: #2d3748;
    }
    .conversation-tab {
        background-color: #2d3748;
        border: 1px solid #4a5568;
        border-radius: 0.5rem;
        padding: 0.5rem;
        margin: 0.2rem;
        cursor: pointer;
        transition: all 0.2s;
    }
    .conversation-tab:hover {
        background-color: #4a5568;
    }
    .active-tab {
        background-color: #4a5568;
        border-color: #63b3ed;
    }
    .stTextInput > div > div > input {
        background-color: #2d3748;
        color: white;
        border: 1px solid #4a5568;
    }
    .stSelectbox > div > div > select {
        background-color: #2d3748;
        color: white;
        border: 1px solid #4a5568;
    }
    .conversation-preview {
        font-size: 0.8rem;
        color: #a0aec0;
        margin-top: 0.2rem;
    }
</style>
""", unsafe_allow_html=True)

class ChatBot:
    def __init__(self, api_key: str = None, base_url: str = None):
        """Initialize the chatbot with KodeKey configuration."""
        self.api_key = api_key or os.getenv("KODEKEY_API_KEY")
        self.base_url = base_url or os.getenv("KODEKEY_BASE_URL")
        
        if not self.api_key:
            raise ValueError("KodeKey API key is required")
        
        # Initialize OpenAI client with KodeKey
        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url
        )
        
        # Available models
        self.models = {
            "Claude Sonnet 4": "anthropic/claude-sonnet-4",
            "GPT-4o": "openai/gpt-4o", 
            "Gemini 2.0 Flash": "google/gemini-2.0-flash-thinking-exp"
        }
        
        # System prompts for different personalities
        self.system_prompts = {
            "Assistant": "You are a helpful AI assistant. Provide clear, accurate, and helpful responses to user queries.",
            "Developer": "You are an expert software developer. Help with coding questions, debugging, and best practices.",
            "Teacher": "You are a patient and knowledgeable teacher. Explain concepts clearly with examples and encourage learning.",
            "Creative": "You are a creative AI assistant. Help with writing, brainstorming, and creative projects with imagination and flair.",
            "Analyst": "You are a data analyst and researcher. Provide detailed analysis, insights, and evidence-based responses."
        }
    
    def get_response(self, messages: List[Dict], model: str, temperature: float = 0.7) -> str:
        """Get response from the AI model."""
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=2000,
                stream=False
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
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

def initialize_session_state():
    """Initialize session state variables."""
    if "conversations" not in st.session_state:
        st.session_state.conversations = {}
    
    if "active_conversation" not in st.session_state:
        # Create first conversation
        conversation_id = str(uuid.uuid4())
        st.session_state.conversations[conversation_id] = {
            "title": "New Chat",
            "messages": [],
            "created_at": datetime.now().isoformat(),
            "model": "anthropic/claude-sonnet-4",
            "personality": "Assistant",
            "temperature": 0.7
        }
        st.session_state.active_conversation = conversation_id
    
    if "chatbot" not in st.session_state:
        st.session_state.chatbot = None

def create_new_conversation():
    """Create a new conversation."""
    conversation_id = str(uuid.uuid4())
    st.session_state.conversations[conversation_id] = {
        "title": "New Chat",
        "messages": [],
        "created_at": datetime.now().isoformat(),
        "model": "anthropic/claude-sonnet-4", 
        "personality": "Assistant",
        "temperature": 0.7
    }
    st.session_state.active_conversation = conversation_id
    st.rerun()

def delete_conversation(conversation_id: str):
    """Delete a conversation."""
    if len(st.session_state.conversations) > 1:
        del st.session_state.conversations[conversation_id]
        if st.session_state.active_conversation == conversation_id:
            # Switch to first available conversation
            st.session_state.active_conversation = list(st.session_state.conversations.keys())[0]
        st.rerun()

def get_conversation_title(messages: List[Dict]) -> str:
    """Generate a title for the conversation based on first message."""
    if not messages:
        return "New Chat"
    
    first_message = next((msg for msg in messages if msg["role"] == "user"), None)
    if first_message:
        content = first_message["content"]
        # Take first 30 characters and clean up
        title = content[:30].strip()
        if len(content) > 30:
            title += "..."
        return title
    
    return "New Chat"

def export_conversation(conversation_id: str):
    """Export conversation as JSON."""
    if conversation_id in st.session_state.conversations:
        conversation = st.session_state.conversations[conversation_id]
        return json.dumps(conversation, indent=2)
    return None

def import_conversation(uploaded_file):
    """Import conversation from JSON file."""
    try:
        conversation_data = json.load(uploaded_file)
        conversation_id = str(uuid.uuid4())
        st.session_state.conversations[conversation_id] = conversation_data
        st.session_state.active_conversation = conversation_id
        st.success("✅ Conversation imported successfully!")
        st.rerun()
    except Exception as e:
        st.error(f"❌ Error importing conversation: {str(e)}")

def render_message(message: Dict, is_user: bool = True):
    """Render a chat message with styling."""
    avatar = "👤" if is_user else "🤖"
    css_class = "user-message" if is_user else "assistant-message"
    avatar_class = "user-avatar" if is_user else "assistant-avatar"
    
    st.markdown(f"""
    <div class="chat-message {css_class}">
        <div class="avatar {avatar_class}">{avatar}</div>
        <div style="flex: 1;">
            <div style="color: white; line-height: 1.6;">{message["content"]}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def main():
    """Main Streamlit application."""
    
    # Initialize session state
    initialize_session_state()
    
    # Header
    st.title("🤖 KodeKey AI Chat")
    st.markdown("*ChatGPT-style interface with multiple AI models*")
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # API Key input
        api_key = st.text_input(
            "KodeKey API Key",
            type="password",
            value=st.session_state.get("api_key", ""),
            placeholder="Sk-kkAI-...",
            help="Enter your KodeKey API key"
        )
        
        if api_key:
            st.session_state.api_key = api_key
            try:
                if st.session_state.chatbot is None:
                    st.session_state.chatbot = ChatBot(api_key)
                st.success("✅ API key configured")
            except Exception as e:
                st.error(f"❌ Invalid API key: {str(e)}")
                st.session_state.chatbot = None
        
        st.divider()
        
        # Model and personality settings for active conversation
        if st.session_state.chatbot and st.session_state.active_conversation:
            active_conv = st.session_state.conversations[st.session_state.active_conversation]
            
            st.header("🎭 Chat Settings")
            
            # Model selection
            model_names = list(st.session_state.chatbot.models.keys())
            current_model_name = next(
                (name for name, model_id in st.session_state.chatbot.models.items() 
                 if model_id == active_conv["model"]), 
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
                list(st.session_state.chatbot.system_prompts.keys()),
                index=list(st.session_state.chatbot.system_prompts.keys()).index(active_conv["personality"]),
                help="Choose the AI personality"
            )
            
            # Temperature setting
            temperature = st.slider(
                "Creativity",
                min_value=0.0,
                max_value=1.0,
                value=active_conv["temperature"],
                step=0.1,
                help="Higher values make responses more creative"
            )
            
            # Update conversation settings
            st.session_state.conversations[st.session_state.active_conversation].update({
                "model": st.session_state.chatbot.models[selected_model],
                "personality": personality,
                "temperature": temperature
            })
            
            st.divider()
        
        # Conversation management
        st.header("💬 Conversations")
        
        # New conversation button
        if st.button("➕ New Chat", use_container_width=True):
            create_new_conversation()
        
        # Conversation list
        conversations = st.session_state.conversations
        for conv_id, conv_data in conversations.items():
            is_active = conv_id == st.session_state.active_conversation
            
            # Conversation item
            col1, col2 = st.columns([3, 1])
            
            with col1:
                if st.button(
                    get_conversation_title(conv_data["messages"]),
                    key=f"conv_{conv_id}",
                    use_container_width=True,
                    type="primary" if is_active else "secondary"
                ):
                    st.session_state.active_conversation = conv_id
                    st.rerun()
            
            with col2:
                if st.button("🗑️", key=f"del_{conv_id}", help="Delete conversation"):
                    delete_conversation(conv_id)
        
        st.divider()
        
        # Export/Import
        st.header("📁 Data Management")
        
        # Export current conversation
        if st.session_state.active_conversation:
            export_data = export_conversation(st.session_state.active_conversation)
            if export_data:
                st.download_button(
                    "📤 Export Chat",
                    export_data,
                    f"conversation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    "application/json",
                    use_container_width=True
                )
        
        # Import conversation
        uploaded_file = st.file_uploader(
            "📥 Import Chat",
            type=['json'],
            help="Upload a previously exported conversation"
        )
        
        if uploaded_file:
            import_conversation(uploaded_file)
        
        # Clear all conversations
        if st.button("🗑️ Clear All Chats", use_container_width=True):
            if st.session_state.conversations:
                # Keep only one empty conversation
                conversation_id = str(uuid.uuid4())
                st.session_state.conversations = {
                    conversation_id: {
                        "title": "New Chat",
                        "messages": [],
                        "created_at": datetime.now().isoformat(),
                        "model": "anthropic/claude-sonnet-4",
                        "personality": "Assistant",
                        "temperature": 0.7
                    }
                }
                st.session_state.active_conversation = conversation_id
                st.rerun()
    
    # Main chat interface
    if not st.session_state.chatbot:
        st.warning("🔑 Please enter your KodeKey API key in the sidebar to start chatting!")
        st.info("Don't have a KodeKey API key? Get one at [KodeKloud](https://kodekloud.com)")
        return
    
    if not st.session_state.active_conversation:
        st.error("❌ No active conversation. Please create a new chat.")
        return
    
    # Get active conversation
    active_conv = st.session_state.conversations[st.session_state.active_conversation]
    
    # Display conversation title
    st.subheader(f"💬 {get_conversation_title(active_conv['messages'])}")
    
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
            <div style="text-align: center; color: #a0aec0; padding: 2rem;">
                👋 Hello! I'm your AI assistant. How can I help you today?
            </div>
            """, unsafe_allow_html=True)
    
    # Chat input
    with st.container():
        st.divider()
        
        # Input form
        with st.form(key="chat_form", clear_on_submit=True):
            col1, col2 = st.columns([4, 1])
            
            with col1:
                user_input = st.text_area(
                    "Type your message...",
                    key="user_input",
                    height=100,
                    placeholder="Ask me anything...",
                    label_visibility="collapsed"
                )
            
            with col2:
                st.markdown("<br>", unsafe_allow_html=True)  # Add spacing
                submit_button = st.form_submit_button(
                    "🚀 Send",
                    use_container_width=True,
                    type="primary"
                )
        
        # Quick action buttons
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("💡 Explain", use_container_width=True):
                user_input = "Can you explain this concept in simple terms?"
        
        with col2:
            if st.button("🔧 Debug", use_container_width=True):
                user_input = "Help me debug this code issue"
        
        with col3:
            if st.button("✨ Create", use_container_width=True):
                user_input = "Help me create something new"
        
        with col4:
            if st.button("📊 Analyze", use_container_width=True):
                user_input = "Analyze this data or situation"
    
    # Process user input
    if submit_button and user_input.strip():
        # Add user message to conversation
        active_conv["messages"].append({
            "role": "user",
            "content": user_input.strip()
        })
        
        # Update conversation title if it's the first message
        if len(active_conv["messages"]) == 1:
            active_conv["title"] = get_conversation_title(active_conv["messages"])
        
        # Prepare messages for API
        messages = [
            {
                "role": "system",
                "content": st.session_state.chatbot.system_prompts[active_conv["personality"]]
            }
        ]
        
        # Add conversation history (keep last 10 exchanges to manage context)
        recent_messages = active_conv["messages"][-20:]  # Last 20 messages
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
                
            except Exception as e:
                error_msg = f"❌ Error generating response: {str(e)}"
                response_container.error(error_msg)
                active_conv["messages"].append({
                    "role": "assistant",
                    "content": error_msg
                })
        
        # Rerun to show the updated conversation
        st.rerun()

if __name__ == "__main__":
    main()