# AI Language Detection Service with Google Gemini

A Flask-based backend application powered by Google's Gemini AI for intelligent language detection. Unlike pattern-based detection, this uses actual AI to understand context and accurately identify languages including:

- **Sinhala** (සිංහල) - Native Sinhala script
- **English** - Standard English text
- **Singlish** - Sinhala words written in English letters (e.g., "kohomada", "oyata")
- **Tamil** (தமிழ்) - Tamil script
- **Mixed** - Combination of multiple languages
- **Other** - Any other language

## 🚀 Why Gemini AI?

Instead of using hardcoded patterns that can miss variations, Gemini AI:
- ✅ Understands context and nuance
- ✅ Recognizes Singlish variations automatically
- ✅ Handles mixed-language text intelligently
- ✅ Provides confidence scores and detailed analysis
- ✅ Supports unlimited languages without code changes

## 📋 Prerequisites

1. **Python 3.7+**
2. **Google Gemini API Key** - Get it free at: [https://aistudio.google.com/api-keys](https://aistudio.google.com/api-keys)

## 🔧 Installation

### Step 1: Install Dependencies

```bash
pip install -r requirements_gemini.txt
```

Or manually:
```bash
pip install Flask==3.0.0 flask-cors==4.0.0 google-generativeai==0.3.2
```

### Step 2: Get Your Gemini API Key

1. Go to [https://aistudio.google.com/api-keys](https://aistudio.google.com/api-keys)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy your API key

### Step 3: Set Your API Key

```bash
# On Linux/Mac
export GEMINI_API_KEY="your-api-key-here"

# On Windows (Command Prompt)
set GEMINI_API_KEY=your-api-key-here

# On Windows (PowerShell)
$env:GEMINI_API_KEY="your-api-key-here"
```

## 🚀 Running the Application

```bash
python app_gemini.py
```

Then open your browser to: **http://localhost:5000**

## 📡 API Usage

### Endpoint: `/api/detect`

**Method:** POST

**Request:**
```json
{
  "message": "Your message here"
}
```

**Response:**
```json
{
  "user_message": "kohomada oyata",
  "detected_language": "singlish",
  "confidence": 95,
  "analysis": "This text is written in Singlish (romanized Sinhala). The words 'kohomada' (how are) and 'oyata' (you) are common Sinhala words written in English letters."
}
```

### Example using cURL:

```bash
curl -X POST http://localhost:5000/api/detect \
  -H "Content-Type: application/json" \
  -d '{"message": "mama hondai, oya kohomada?"}'
```

### Example using Python:

```python
import requests

response = requests.post('http://localhost:5000/api/detect', 
    json={'message': 'හෙලෝ වර්ල්ඩ්'})
    
result = response.json()
print(f"Language: {result['detected_language']}")
print(f"Confidence: {result['confidence']}%")
print(f"Analysis: {result['analysis']}")
```

### Health Check Endpoint:

```bash
curl http://localhost:5000/api/health
```

Response:
```json
{
  "status": "healthy",
  "gemini_api_configured": true
}
```

## 🧪 Test Examples

Try these examples in the UI:

1. **Pure Sinhala:** `ආයුබෝවන් ඔබට කොහොමද?`
2. **Pure English:** `Hello, how are you today?`
3. **Singlish:** `mama hondai, oyata kohomada?`
4. **Mixed:** `මම fine, thank you. ඔබ කොහොමද?`
5. **Complex Singlish:** `api yanawa gedara, enna puluwanda?`
6. **Tamil:** `வணக்கம், எப்படி இருக்கிறீர்கள்?`

## 🎯 Key Features

### 1. AI-Powered Detection
Uses Google's Gemini Pro model for intelligent language understanding

### 2. Detailed Analysis
Provides explanation of why a particular language was detected

### 3. High Accuracy
Gemini AI can distinguish between:
- Sinhala script (සිංහල)
- Romanized Sinhala (kohomada)
- Mixed language text
- Similar-looking scripts

### 4. No Pattern Updates Needed
Unlike regex patterns, AI learns and adapts automatically

## 🔒 API Key Security

**Never commit your API key to version control!**

Best practices:
1. Use environment variables
2. Add `.env` file to `.gitignore`
3. Use a `.env` file with python-dotenv:

```bash
pip install python-dotenv
```

Create `.env` file:
```
GEMINI_API_KEY=your-api-key-here
```

Update code:
```python
from dotenv import load_dotenv
load_dotenv()
```

## 🌟 Next Steps / Future Enhancements

Now that you have AI language detection, you can:

1. **Add Response Generation**: Make the chatbot reply in the detected language
2. **Conversation Memory**: Store chat history
3. **Translation**: Auto-translate between languages
4. **Voice Input**: Add speech-to-text
5. **Multi-turn Conversations**: Build a full conversational AI

## 📊 API Rate Limits

Gemini API free tier includes:
- 60 requests per minute
- 1,500 requests per day

For production use, consider upgrading to paid tier.

## 🐛 Troubleshooting

### Error: "API key not configured"
- Make sure you've set your GEMINI_API_KEY environment variable
- Or update the code with your actual API key

### Error: "Module 'google.generativeai' not found"
```bash
pip install google-generativeai
```

### Error: "API key not valid"
- Check your API key at [https://aistudio.google.com/api-keys](https://aistudio.google.com/api-keys)
- Make sure there are no extra spaces or quotes
- Regenerate a new key if needed

## 📝 License

Free to use and modify for your projects!

## 🙏 Credits

- Powered by Google Gemini AI
- Flask web framework
- Built with ❤️ for multilingual communication
