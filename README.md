# 🚀 KodeKloud KeySpaces Examples

**One Key, Unlimited AI Possibilities**

Ready-to-use examples demonstrating KodeKloud KeySpaces - the fastest way for developers to start building AI-powered applications.

![KeySpaces Examples](https://res.cloudinary.com/dezmljkdo/image/upload/v1752086507/Screenshot_2025-07-09_at_2.40.54_PM_aairko.png)

## 🌟 What is KodeKloud KeySpaces?

KeySpaces is an AI playground that provides instant access to multiple cutting-edge language models through a single API key:

✨ **One Key, Multiple Models**: Claude Sonnet 4, GPT-4o, GPT-4.1, Gemini 2.5 Pro, Grok 3, and more  
🚀 **Zero Setup**: Skip API approvals and billing setups for each provider  
📚 **Ready-to-Run Examples**: Copy-paste code that works immediately  

### 🔑 Get Your Free API Key
**[Generate your KeySpaces API key →](https://learn.kodekloud.com/user/playgrounds/keyspace)**

## ⚠️ Important Disclaimer

**KeySpaces is designed for learning, experimentation, and rapid prototyping only.**

- ❌ **NOT for production use** - Rate limits are intentionally low
- ❌ **NOT a replacement** for direct vendor APIs in production
- ✅ **PERFECT for** quick prototypes, learning AI, and testing different models
- ✅ **IDEAL for** developers who want to start building AI apps immediately

## 📚 Available Examples

### 🤖 [AI Chatbot](./kodekey-chatbot/)
A modern ChatGPT-style interface with:
- Multiple AI models in one interface
- Persistent conversation memory
- 5 different AI personalities
- Full-text search across chats

*More examples coming soon!*

## 🚀 Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/kodekloud/kodekey-examples.git
cd kodekey-examples

# 2. Choose an example
cd kodekey-chatbot

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set your API key
echo "KEYSPACES_API_KEY=your-api-key-here" > .env

# 5. Run!
streamlit run chatbot.py
```

## 🤖 Available Models

- **Claude Sonnet 4** - Advanced reasoning and analysis
- **GPT-4o** - Versatile general-purpose AI
- **GPT-4.1** - Enhanced GPT-4 capabilities
- **Gemini 2.5 Pro** - Multimodal excellence
- **Grok 3** - Real-time knowledge
- **Gemini 2.0 Flash** - Lightning-fast responses

## 💳 Subscription Tiers

### Free Tier
- ✅ 25 requests/month
- ✅ Access to all models
- ✅ Perfect for trying out AI

### AI Plan
- 🚀 500 requests/month (20X more!)
- 🚀 Up to 1,000 tokens per request
- 🚀 Priority support

## 🔧 Integration Example

```python
from openai import OpenAI

# Works with standard OpenAI client!
client = OpenAI(
    api_key="your-keyspaces-api-key",
    base_url="https://main.kk-ai-keys.kodekloud.com/v1"
)

response = client.chat.completions.create(
    model="anthropic/claude-sonnet-4",
    messages=[{"role": "user", "content": "Hello AI!"}]
)
```

## 🔐 Security & Privacy

- 🔒 Keys are encrypted at rest
- 🔄 Rotate keys anytime for security
- 🚫 We never train on or store your prompts
- 📊 Real-time usage tracking

## 🤝 Contributing

We welcome new examples! Each example should:
- Include its own README with setup instructions
- Demonstrate unique AI capabilities
- Be simple enough for beginners to understand

## 🔗 Resources

- **Generate API Key**: [keyspace.kodekloud.com](https://learn.kodekloud.com/user/playgrounds/keyspace)
- **Explore Playgrounds**: [kodekloud.com/playgrounds](https://kodekloud.com/playgrounds/)

---

**Start building AI applications in minutes, not days!**

*KodeKloud KeySpaces: Where AI Development Becomes Effortless*%   
