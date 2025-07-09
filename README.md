# 🚀 KodeKey AI Examples

A collection of practical AI applications built with KodeKey's unified API access to multiple AI models including Claude Sonnet 4, GPT-4o, and Gemini 2.0 Flash.

![KodeKey Examples](https://via.placeholder.com/800x400/667eea/ffffff?text=KodeKey+AI+Examples)

## 🌟 What is KodeKey?

**KodeKey** is a unified API platform that provides access to multiple state-of-the-art AI models through a single API key. Instead of managing multiple API keys and different interfaces, KodeKey lets you access Claude, GPT, Gemini, and other models seamlessly.

### 🔑 Get Your KodeKey
**[Get your KodeKey API key here →](https://learn.kodekloud.com/user/playgrounds/keyspace)**

## 📚 Available Examples

### 1. 🤖 **AI Chatbot** - ChatGPT-Style Interface
A beautiful, modern chatbot with conversation memory and multiple AI models.

**Features:**
- ChatGPT-style UI with glassmorphism design
- Multiple AI models (Claude Sonnet 4, GPT-4o, Gemini 2.0)
- Conversation memory and session management
- Export/import conversations
- Multiple AI personalities
- Streaming responses with typing effect

**[👉 View Chatbot Example](./chatbot/)**

### 2. 📚 **Documentation Generator** - Smart Code Documentation
Automatically generate comprehensive documentation for your code projects using LangChain.

**Features:**
- Upload ZIP files of code projects
- Multi-language support (Python, JavaScript, TypeScript, Java, etc.)
- Generate README, API docs, and file documentation
- LangChain integration for advanced prompting
- Project analysis and statistics
- Export documentation as individual files or ZIP

**[👉 View Documentation Generator](./documentation-generator/)**

## 🎯 Why Use KodeKey?

### ✅ **Unified Access**
- **One API Key** for all major AI models
- **Consistent Interface** across different providers
- **No vendor lock-in** - easily switch between models

### ⚡ **Developer-Friendly**
- **Drop-in replacement** for OpenAI SDK
- **Same familiar interface** you already know
- **Minimal code changes** required

### 💰 **Cost-Effective**
- **No additional cost!** 25 Free use credits and 500 Premium Credits (with the AI Plan) every month.
- **Use the best model** for each specific task
- **No minimum commitments** or setup fees

### 🔧 **Easy Integration**
```python
from openai import OpenAI

client = OpenAI(
    api_key="your-kodekey-api-key",
    base_url="https://main.kk-ai-keys.kodekloud.com/v1"
)

response = client.chat.completions.create(
    model="anthropic/claude-sonnet-4",
    messages=[{"role": "user", "content": "Hello!"}]
)
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- KodeKey API key ([Get yours here](https://learn.kodekloud.com/user/playgrounds/keyspace))

### 1. Clone the Repository
```bash
git clone https://github.com/kodekloud/kodekey-examples.git
cd kodekey-examples
```

### 2. Choose an Example
```bash
# For the chatbot
cd chatbot
pip install -r requirements.txt
streamlit run chatbot.py

# For the documentation generator
cd documentation-generator
pip install -r requirements.txt
streamlit run doc_generator.py
```

### 3. Set Up Your API Key
```bash
# Set environment variable
export KODEKEY_API_KEY="your-api-key-here"

# Or create a .env file
echo "KODEKEY_API_KEY=your-api-key-here" > .env
```

### 4. Run the Application
Open your browser to `http://localhost:8501` and start exploring!

## 🤖 Available AI Models

### **Claude Sonnet 4** (`anthropic/claude-sonnet-4`)
- **Best for**: Detailed analysis, creative writing, complex reasoning
- **Strengths**: Excellent at following instructions, nuanced responses
- **Use cases**: Content creation, code review, research analysis

### **GPT-4o** (`openai/gpt-4o`)
- **Best for**: General conversation, problem-solving, coding
- **Strengths**: Fast responses, broad knowledge, reliable performance
- **Use cases**: Customer support, tutoring, general assistance

### **Gemini 2.0 Flash** (`google/gemini-2.0-flash-thinking-exp`)
- **Best for**: Quick responses, simple tasks, high-throughput scenarios
- **Strengths**: Speed, efficiency, cost-effective
- **Use cases**: Simple queries, batch processing, real-time applications

## 💡 Usage Examples

### Basic Chat Completion
```python
from openai import OpenAI

client = OpenAI(
    api_key="your-kodekey-api-key",
    base_url="https://main.kk-ai-keys.kodekloud.com/v1"
)

response = client.chat.completions.create(
    model="anthropic/claude-sonnet-4",
    messages=[
        {"role": "user", "content": "Explain quantum computing in simple terms"}
    ]
)

print(response.choices[0].message.content)
```

### Streaming Responses
```python
response = client.chat.completions.create(
    model="openai/gpt-4o",
    messages=[{"role": "user", "content": "Write a story about AI"}],
    stream=True
)

for chunk in response:
    if chunk.choices[0].delta.content is not None:
        print(chunk.choices[0].delta.content, end="")
```

### Model Comparison
```python
models = [
    "anthropic/claude-sonnet-4",
    "openai/gpt-4o",
    "google/gemini-2.0-flash-thinking-exp"
]

for model in models:
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": "What is machine learning?"}]
    )
    print(f"{model}: {response.choices[0].message.content}\n")
```

## 🔧 Configuration

### Environment Variables
```bash
# Required
KODEKEY_API_KEY=your-api-key-here

# Optional
KODEKEY_BASE_URL=https://main.kk-ai-keys.kodekloud.com/v1
```

### Model Parameters
```python
response = client.chat.completions.create(
    model="anthropic/claude-sonnet-4",
    messages=[{"role": "user", "content": "Hello!"}],
    temperature=0.7,    # Creativity level (0-1)
    max_tokens=1000,    # Response length limit
    top_p=1,           # Nucleus sampling
    frequency_penalty=0, # Repetition penalty
    presence_penalty=0   # Topic diversity
)
```

## 🛠️ Development Setup

### Install Dependencies
```bash
# Install all dependencies for all examples
pip install -r requirements.txt

# Or install for specific examples
pip install streamlit openai python-dotenv
pip install langchain langchain-openai gitpython  # For doc generator
```

### Run in Development Mode
```bash
# Chatbot with hot reload
streamlit run chatbot/chatbot.py --server.runOnSave true

# Documentation generator
streamlit run documentation-generator/doc_generator.py
```

## 🚀 Deployment

### Docker Deployment
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501
CMD ["streamlit", "run", "chatbot/chatbot.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Cloud Deployment
```bash
# Build and run
docker build -t kodekey-examples .
docker run -p 8501:8501 -e KODEKEY_API_KEY=your-key kodekey-examples
```

## 📈 Performance & Best Practices

### Model Selection Guidelines
- **Claude Sonnet 4**: Use for complex analysis, creative tasks, detailed explanations
- **GPT-4o**: Use for general conversation, coding help, balanced performance
- **Gemini 2.0 Flash**: Use for quick responses, simple queries, high-volume tasks

### Optimization Tips
- **Temperature Settings**: Use 0.1-0.3 for factual responses, 0.7-1.0 for creative tasks
- **Context Management**: Keep conversation history focused and relevant
- **Token Limits**: Monitor usage to stay within limits
- **Caching**: Cache common responses to reduce API calls

## 🔐 Security

- **API Key Protection**: Never commit API keys to version control
- **Environment Variables**: Use `.env` files for sensitive configuration
- **Rate Limiting**: Implement proper rate limiting for production use
- **Input Validation**: Validate user inputs before sending to AI models

## 🐛 Troubleshooting

### Common Issues

**API Key Error**
```
❌ Authentication failed
```
- Verify your KodeKey API key is correct
- Check if the key is active and has sufficient credits

**Model Not Available**
```
❌ Model not found
```
- Ensure the model is available in your KodeKey plan
- Check the model name spelling

**Rate Limits**
```
❌ Rate limit exceeded
```
- Implement exponential backoff
- Consider using a different model
- Check your usage limits

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 style guide
- Add docstrings to all functions
- Include error handling
- Add tests for new features
- Update documentation

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **KodeKey Team** for the unified API platform
- **Streamlit** for the amazing web framework
- **OpenAI** for the SDK and API standards
- **Anthropic, OpenAI, Google** for the AI models
- **Community contributors** for feedback and improvements

## 🔗 Resources

### KodeKey Platform
- **Get API Key**: [https://learn.kodekloud.com/user/playgrounds/keyspace](https://learn.kodekloud.com/user/playgrounds/keyspace)


---

**🚀 Start building amazing AI applications with KodeKey today!**

*One key to rule them all - access multiple AI models through a single, unified API.*
