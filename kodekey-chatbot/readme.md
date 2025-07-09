# 🤖 KodeKey AI Chatbot

A beautiful, ChatGPT-style chatbot with conversation memory, multiple AI models, and a modern Streamlit interface powered by KodeKey's unified API.

![KodeKey Chatbot Screenshot](https://res.cloudinary.com/dezmljkdo/image/upload/v1752086507/Screenshot_2025-07-09_at_2.40.54_PM_aairko.png)

## ✨ Features

### 🎯 **Core Functionality**
- **Multiple AI Models**: Switch between Claude Sonnet 4, GPT-4o, and Gemini 2.0 Flash
- **Conversation Memory**: Maintains context within each chat session
- **Multiple Conversations**: Create unlimited chat sessions with easy switching
- **Streaming Responses**: Real-time typing effect for natural conversation flow
- **Personality System**: Choose from 5 AI personalities (Assistant, Developer, Teacher, Creative, Analyst)

### 🎨 **Beautiful Interface**
- **Modern Design**: Glassmorphism effects with gradient backgrounds
- **ChatGPT-Style UI**: Professional message bubbles and layout
- **Responsive Design**: Works perfectly on desktop and mobile
- **Smooth Animations**: Hover effects, transitions, and loading states
- **Dark Theme**: Easy on the eyes with professional aesthetics

### 💾 **Data Management**
- **Export/Import**: Save and restore conversations as JSON files
- **Persistent Sessions**: Conversations saved during browser session
- **Clear History**: Easy conversation management and cleanup
- **Auto-Titles**: Smart conversation titles based on content

### ⚡ **Quick Actions**
- **Explain**: Get detailed explanations of concepts
- **Debug**: Help with code debugging and troubleshooting
- **Create**: Assistance with creative projects
- **Analyze**: Data analysis and insights

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- KodeKey API key ([Get yours here](https://learn.kodekloud.com/user/playgrounds/keyspace))

### Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd kodekey-examples/chatbot
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment** (optional):
   ```bash
   # Create .env file
   echo "KODEKEY_API_KEY=your-api-key-here" > .env
   echo "KODEKEY_BASE_URL=https://main.kk-ai-keys.kodekloud.com/v1" >> .env
   ```

4. **Run the application**:
   ```bash
   streamlit run chatbot.py
   ```

5. **Open in browser**:
   Navigate to `http://localhost:8501`

## 🔧 Configuration

### API Key Setup
You can provide your KodeKey API key in two ways:

1. **Environment Variable** (recommended):
   ```bash
   export KODEKEY_API_KEY="your-api-key-here"
   ```

2. **Direct Input**: Enter your API key in the sidebar when running the app

### Available Models
- **Claude Sonnet 4**: Best for detailed analysis and creative tasks
- **GPT-4o**: Great for general conversation and problem-solving
- **Gemini 2.0 Flash**: Fast responses for quick questions

### Personality Options
- **Assistant**: Helpful and professional responses
- **Developer**: Technical and code-focused assistance
- **Teacher**: Patient and educational explanations
- **Creative**: Imaginative and artistic collaboration
- **Analyst**: Data-driven and analytical insights

## 📁 Project Structure

```
chatbot/
├── chatbot.py              # Main application file
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
├── README.md              # This file
└── assets/               # Optional: screenshots and assets
    └── screenshot.png
```

## 🛠️ Usage

### Basic Chat
1. Enter your KodeKey API key in the sidebar
2. Select your preferred AI model
3. Choose a personality that fits your needs
4. Start chatting!

### Managing Conversations
- **New Chat**: Click "➕ New Chat" to start a fresh conversation
- **Switch Chats**: Click on any conversation in the sidebar to switch
- **Delete Chat**: Click the 🗑️ icon next to any conversation
- **Export Chat**: Use "📤 Export Chat" to save conversations
- **Import Chat**: Use "📥 Import Chat" to restore saved conversations

### Quick Actions
Use the quick action buttons for common tasks:
- **💡 Explain**: Get explanations of complex topics
- **🔧 Debug**: Help with code issues
- **✨ Create**: Brainstorm and create content
- **📊 Analyze**: Analyze data or situations

### Adjusting Creativity
Use the creativity slider to control response style:
- **Low (0.0-0.3)**: More factual and consistent responses
- **Medium (0.4-0.7)**: Balanced creativity and accuracy
- **High (0.8-1.0)**: More creative and varied responses

## 🔄 Advanced Features

### Custom System Prompts
You can extend the personality system by adding custom prompts:

```python
# Add to the system_prompts dictionary
custom_prompts = {
    "Marketing": "You are a marketing expert...",
    "Legal": "You are a legal advisor...",
    "Health": "You are a health advisor..."
}
```

### Model Configuration
Add support for additional models:

```python
# Add to the models dictionary
custom_models = {
    "Claude Opus 4": "anthropic/claude-opus-4",
    "GPT-4 Turbo": "openai/gpt-4-turbo"
}
```

### Conversation Analytics
Track conversation statistics:

```python
def get_conversation_stats(conversation):
    messages = conversation["messages"]
    return {
        "total_messages": len(messages),
        "user_messages": len([m for m in messages if m["role"] == "user"]),
        "assistant_messages": len([m for m in messages if m["role"] == "assistant"])
    }
```

## 🚀 Deployment

### Local Development
```bash
# Run with hot reload
streamlit run chatbot.py --server.runOnSave true
```

### Docker Deployment
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501
CMD ["streamlit", "run", "chatbot.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Cloud Deployment
```bash
# Build and run with Docker
docker build -t kodekey-chatbot .
docker run -p 8501:8501 -e KODEKEY_API_KEY=your-key kodekey-chatbot
```

## 📦 Dependencies

```
openai>=1.3.0
streamlit>=1.28.0
python-dotenv>=1.0.0
uuid>=1.30
```

## 🔐 Security

- **API Key Protection**: Never commit API keys to version control
- **Environment Variables**: Use `.env` files for sensitive data
- **Session Storage**: Conversations are stored in browser session only
- **No Data Persistence**: No server-side data storage

## 🐛 Troubleshooting

### Common Issues

**API Key Error**
```
❌ Invalid API key
```
- Verify your KodeKey API key is correct
- Check that the key is active and has sufficient credits

**Model Not Available**
```
❌ Model not found
```
- Ensure the selected model is available in your KodeKey plan
- Try switching to a different model

**Streaming Issues**
```
❌ Connection error
```
- Check your internet connection
- Verify the KodeKey API endpoint is accessible

**Memory Issues**
```
Browser running slow
```
- Clear conversation history using "🗑️ Clear All Chats"
- Refresh the browser page
- Close and reopen the application

### Performance Tips

- **Context Management**: Keep conversations focused for better responses
- **Model Selection**: Use faster models for simple queries
- **Temperature Settings**: Lower values for factual responses
- **Conversation Limits**: Consider clearing old conversations regularly


## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.


## 🔗 Links

- **KodeKey Platform**: [https://learn.kodekloud.com/user/playgrounds/keyspace](https://learn.kodekloud.com/user/playgrounds/keyspace)
- **Streamlit Documentation**: [https://docs.streamlit.io](https://docs.streamlit.io)

