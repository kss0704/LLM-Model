# LLM Code Assistant

A powerful Streamlit-based coding assistant powered by Groq's lightning-fast LLM models. Get instant help with coding, debugging, code review, and programming in 20+ languages.

## ✨ Features

### 🚀 **Multi-Language Code Generation**
- Support for 20+ programming languages
- Clean, efficient, and well-documented code
- Production-ready code with best practices

### 🔧 **Code Execution Environment**
- Run Python and JavaScript code directly in the app
- Safe execution in temporary containers
- Real-time output display

### 🤖 **AI-Powered Assistance**
- Code generation and optimization
- Bug detection and debugging
- Code review and suggestions
- Algorithm explanations

### 📝 **Supported Languages**
- **Web Development**: HTML, CSS, JavaScript, TypeScript
- **Backend**: Python, Java, C++, C, Go, Rust
- **Mobile**: Swift, Kotlin
- **Scripting**: Bash, PowerShell, PHP, Ruby
- **Data Science**: SQL, R, MATLAB
- **And many more!**

### ⚙️ **Advanced Configuration**
- Multiple Groq model options
- Adjustable temperature and token limits
- Real-time API connection testing
- Chat history management

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- Groq API key (free at [console.groq.com](https://console.groq.com/))

### Quick Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd codellm
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run app.py
   ```

4. **Open your browser**
   - Navigate to `http://localhost:8501`
   - Enter your Groq API key in the sidebar
   - Start coding!

## 🔑 Getting Your Groq API Key

1. Visit [console.groq.com](https://console.groq.com/)
2. Sign up for a free account
3. Navigate to API Keys section
4. Generate a new API key
5. Copy and paste it into the app's sidebar

## 🎯 Usage Examples

### Code Generation
```
"Write a Python function to calculate fibonacci numbers"
"Create a REST API endpoint in Node.js"
"Generate a sorting algorithm in C++"
```

### Debugging Help
```
"Why is my Python code throwing a KeyError?"
"Help me fix this JavaScript async/await issue"
"Review my SQL query for performance issues"
```

### Code Explanation
```
"Explain how this recursive function works"
"Break down this regex pattern"
"What's the time complexity of this algorithm?"
```

## 🔧 Configuration Options

### Available Models
- **Llama 3.1 8B Instant** - Fastest responses
- **Llama 3.1 70B Versatile** - Most capable
- **Mixtral 8x7B** - Excellent reasoning
- **Gemma 2 9B** - Efficient performance

### Parameters
- **Temperature**: Controls creativity (0.0 = focused, 1.0 = creative)
- **Max Tokens**: Response length limit (500-32,768)

## 🏃‍♂️ Code Execution

The app supports direct code execution for:
- **Python** - Full standard library support
- **JavaScript** - Node.js runtime required

### Requirements for Code Execution
```bash
# For JavaScript execution
npm install -g node

# Python is included by default
```

## 📁 Project Structure

```
codellm/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── README.md          # This file
└── .gitignore         # Git ignore rules
```

## 🛡️ Security Features

- **Sandboxed Execution**: Code runs in temporary, isolated environments
- **Timeout Protection**: 10-second execution limit
- **Safe File Handling**: Automatic cleanup of temporary files
- **API Key Security**: Keys stored securely in session state

## 🎨 User Interface

- **Modern Design**: Clean, professional interface
- **Responsive Layout**: Works on desktop and mobile
- **Syntax Highlighting**: Code blocks with language detection
- **Real-time Chat**: Instant responses with streaming
- **Dark Theme Support**: Easy on the eyes

## 🔍 Troubleshooting

### Common Issues

**API Connection Failed**
- Verify your Groq API key is correct
- Check your internet connection
- Try the "Test API Connection" button

**Code Execution Errors**
- Ensure required runtime is installed (Node.js for JavaScript)
- Check code syntax and dependencies
- Review timeout limits (10 seconds max)

**Slow Responses**
- Try switching to Llama 3.1 8B Instant model
- Reduce max_tokens setting
- Check Groq service status

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Make your changes**
4. **Commit your changes**
   ```bash
   git commit -m "Add amazing feature"
   ```
5. **Push to the branch**
   ```bash
   git push origin feature/amazing-feature
   ```
6. **Open a Pull Request**

### Development Setup
```bash
# Install development dependencies
pip install -r requirements.txt
pip install black flake8 pytest

# Run tests
pytest

# Format code
black app.py

# Lint code
flake8 app.py
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Groq** - For providing fast, efficient LLM inference
- **Streamlit** - For the amazing web app framework
- **Open Source Community** - For inspiration and support

## 📞 Support

- 🐛 **Bug Reports**: Open an issue on GitHub
- 💡 **Feature Requests**: Create a feature request
- 📖 **Documentation**: Check the wiki
- 💬 **Discussion**: Join our community discussions

## 📊 Roadmap

### Upcoming Features
- [ ] Support for more programming languages
- [ ] Advanced code analysis and metrics
- [ ] Integration with popular IDEs
- [ ] Team collaboration features
- [ ] Code snippet library
- [ ] Enhanced debugging tools

### Version History
- **v1.0.0** - Initial release with basic coding assistance
- **v1.1.0** - Added code execution capabilities
- **v1.2.0** - Enhanced UI and multiple model support

---

**Made with ❤️ using Streamlit and Groq**

*Happy Coding! 🚀*
