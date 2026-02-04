from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import os
import json
from dotenv import load_dotenv

app = Flask(__name__)
CORS(app)

# Configure Gemini API (load from .env)
load_dotenv()
# Read API key from environment (.env file or OS environment)
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
if not GEMINI_API_KEY:
    print("Warning: GEMINI_API_KEY not set. Copy env.example to .env and set your key.")
else:
    genai.configure(api_key=GEMINI_API_KEY)

# Initialize the model
model = genai.GenerativeModel('gemini-2.0-flash')

# HTML content embedded in the Python file
HTML_CONTENT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Language Detection Chatbot</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }

        .container {
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            padding: 40px;
            max-width: 600px;
            width: 100%;
        }

        h1 {
            color: #333;
            margin-bottom: 10px;
            text-align: center;
        }

        .subtitle {
            text-align: center;
            color: #666;
            margin-bottom: 30px;
            font-size: 14px;
        }

        .badge {
            display: inline-block;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 3px 10px;
            border-radius: 12px;
            font-size: 11px;
            font-weight: 600;
            margin-left: 5px;
        }

        .input-section {
            margin-bottom: 30px;
        }

        label {
            display: block;
            margin-bottom: 10px;
            color: #555;
            font-weight: 600;
        }

        textarea {
            width: 100%;
            padding: 15px;
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            font-size: 16px;
            font-family: inherit;
            resize: vertical;
            min-height: 100px;
            transition: border-color 0.3s;
        }

        textarea:focus {
            outline: none;
            border-color: #667eea;
        }

        button {
            width: 100%;
            padding: 15px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 10px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
        }

        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4);
        }

        button:active {
            transform: translateY(0);
        }

        button:disabled {
            background: #ccc;
            cursor: not-allowed;
            transform: none;
        }

        .result-section {
            margin-top: 30px;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 10px;
            display: none;
        }

        .result-section.show {
            display: block;
            animation: fadeIn 0.5s;
        }

        @keyframes fadeIn {
            from {
                opacity: 0;
                transform: translateY(10px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        .result-item {
            margin-bottom: 15px;
        }

        .result-label {
            font-weight: 600;
            color: #555;
            margin-bottom: 5px;
        }

        .result-value {
            padding: 10px;
            background: white;
            border-radius: 5px;
            border-left: 4px solid #667eea;
        }

        .language-badge {
            display: inline-block;
            padding: 5px 15px;
            border-radius: 20px;
            font-weight: 600;
            text-transform: uppercase;
            font-size: 14px;
        }

        .language-sinhala {
            background: #4CAF50;
            color: white;
        }

        .language-english {
            background: #2196F3;
            color: white;
        }

        .language-singlish {
            background: #FF9800;
            color: white;
        }

        .language-mixed {
            background: #9C27B0;
            color: white;
        }

        .language-tamil {
            background: #E91E63;
            color: white;
        }

        .language-unknown {
            background: #757575;
            color: white;
        }

        .confidence-bar {
            width: 100%;
            height: 20px;
            background: #e0e0e0;
            border-radius: 10px;
            overflow: hidden;
            margin-top: 5px;
        }

        .confidence-fill {
            height: 100%;
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            transition: width 0.5s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 12px;
            font-weight: 600;
        }

        .error {
            color: #f44336;
            padding: 10px;
            background: #ffebee;
            border-radius: 5px;
            margin-top: 10px;
        }

        .loader {
            display: none;
            text-align: center;
            margin-top: 20px;
        }

        .loader.show {
            display: block;
        }

        .spinner {
            border: 3px solid #f3f3f3;
            border-top: 3px solid #667eea;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto;
        }

        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        .ai-note {
            background: #e8f4f8;
            border-left: 4px solid #2196F3;
            padding: 10px;
            border-radius: 5px;
            margin-top: 10px;
            font-size: 13px;
            color: #555;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🤖 AI Language Detection Chatbot</h1>
        <p class="subtitle">
            Powered by Google Gemini <span class="badge">AI</span>
        </p>

        <div class="input-section">
            <label for="userMessage">Enter your message:</label>
            <textarea 
                id="userMessage" 
                placeholder="Type in any language: English, සිංහල, Singlish, தமிழ், or mixed..."
            ></textarea>
        </div>

        <button id="detectBtn" onclick="detectLanguage()">🔍 Detect Language with AI</button>

        <div class="loader" id="loader">
            <div class="spinner"></div>
            <p style="margin-top: 10px; color: #666;">AI is analyzing your message...</p>
        </div>

        <div class="result-section" id="resultSection">
            <div class="result-item">
                <div class="result-label">Your Message:</div>
                <div class="result-value" id="userMessageDisplay"></div>
            </div>

            <div class="result-item">
                <div class="result-label">Detected Language:</div>
                <div class="result-value">
                    <span class="language-badge" id="languageBadge"></span>
                </div>
            </div>

            <div class="result-item">
                <div class="result-label">Confidence Level:</div>
                <div class="confidence-bar">
                    <div class="confidence-fill" id="confidenceFill"></div>
                </div>
            </div>

            <div class="result-item">
                <div class="result-label">AI Analysis:</div>
                <div class="result-value" id="analysisDisplay"></div>
            </div>

            <div class="ai-note">
                💡 This detection is powered by Google's Gemini AI for maximum accuracy across all languages and mixed-language text.
            </div>
        </div>

        <div class="error" id="errorMessage" style="display: none;"></div>
    </div>

    <script>
        async function detectLanguage() {
            const messageInput = document.getElementById('userMessage');
            const message = messageInput.value.trim();
            
            document.getElementById('errorMessage').style.display = 'none';
            document.getElementById('resultSection').classList.remove('show');
            
            if (!message) {
                showError('Please enter a message!');
                return;
            }

            document.getElementById('loader').classList.add('show');
            document.getElementById('detectBtn').disabled = true;

            try {
                const response = await fetch('/api/detect', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ message: message })
                });

                const data = await response.json();

                if (response.ok) {
                    displayResults(data);
                } else {
                    showError(data.error || 'An error occurred');
                }
            } catch (error) {
                showError('Failed to connect to the server. Please try again.');
                console.error('Error:', error);
            } finally {
                document.getElementById('loader').classList.remove('show');
                document.getElementById('detectBtn').disabled = false;
            }
        }

        function displayResults(data) {
            document.getElementById('userMessageDisplay').textContent = data.user_message;

            const badge = document.getElementById('languageBadge');
            badge.textContent = data.detected_language;
            badge.className = 'language-badge language-' + data.detected_language.toLowerCase();

            const confidenceFill = document.getElementById('confidenceFill');
            confidenceFill.style.width = data.confidence + '%';
            confidenceFill.textContent = data.confidence.toFixed(0) + '%';

            document.getElementById('analysisDisplay').textContent = data.analysis;

            document.getElementById('resultSection').classList.add('show');
        }

        function showError(message) {
            const errorDiv = document.getElementById('errorMessage');
            errorDiv.textContent = message;
            errorDiv.style.display = 'block';
        }

        document.getElementById('userMessage').addEventListener('keydown', function(e) {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                detectLanguage();
            }
        });
    </script>
</body>
</html>
"""

def detect_language_with_gemini(text):
    """
    Use Gemini API to detect the language of the input text.
    Returns a structured response with language, confidence, and analysis.
    """
    try:
        prompt = f"""Analyze the following text and detect its language(s). 

Text: "{text}"

Please provide your analysis in the following JSON format:
{{
    "language": "primary language (one of: english, sinhala, singlish, tamil, mixed, or other)",
    "confidence": confidence percentage as a number between 0-100,
    "analysis": "brief explanation of your detection including what languages you found and why"
}}

Important notes:
- "sinhala" means text written in Sinhala Unicode script (සිංහල)
- "singlish" means Sinhala words written using English/Latin letters (e.g., "kohomada", "oyata", "mama")
- "english" means standard English text
- "tamil" means text in Tamil script
- "mixed" means combination of multiple languages in the same text
- Be very accurate in distinguishing between Sinhala script and Singlish (romanized Sinhala)

Return ONLY the JSON object, nothing else."""

        response = model.generate_content(prompt)
        result_text = response.text.strip()
        
        # Remove markdown code blocks if present
        if result_text.startswith('```json'):
            result_text = result_text[7:]
        if result_text.startswith('```'):
            result_text = result_text[3:]
        if result_text.endswith('```'):
            result_text = result_text[:-3]
        
        result_text = result_text.strip()
        
        # Parse JSON response
        result = json.loads(result_text)
        
        return {
            'language': result.get('language', 'unknown').lower(),
            'confidence': float(result.get('confidence', 0)),
            'analysis': result.get('analysis', 'No analysis provided')
        }
        
    except json.JSONDecodeError as e:
        print(f"JSON parsing error: {e}")
        print(f"Response text: {result_text}")
        return {
            'language': 'unknown',
            'confidence': 0,
            'analysis': f'Error parsing AI response: {str(e)}'
        }
    except Exception as e:
        print(f"Error in Gemini API call: {e}")
        return {
            'language': 'unknown',
            'confidence': 0,
            'analysis': f'Error: {str(e)}'
        }

@app.route('/')
def index():
    return HTML_CONTENT

@app.route('/api/detect', methods=['POST'])
def detect():
    """
    API endpoint to detect language from user input using Gemini AI
    """
    data = request.get_json()
    
    if not data or 'message' not in data:
        return jsonify({
            'error': 'No message provided'
        }), 400
    
    user_message = data['message']
    
    if not user_message.strip():
        return jsonify({
            'error': 'Message cannot be empty'
        }), 400
    
    # Check if API key is configured
    if not GEMINI_API_KEY:
        return jsonify({
            'error': 'Gemini API key not configured. Please copy env.example to .env and set GEMINI_API_KEY or export it in your environment.'
        }), 500
    
    # Detect language using Gemini
    detection_result = detect_language_with_gemini(user_message)
    
    # Prepare response
    response = {
        'user_message': user_message,
        'detected_language': detection_result['language'],
        'confidence': detection_result['confidence'],
        'analysis': detection_result['analysis']
    }
    
    return jsonify(response)

@app.route('/api/health', methods=['GET'])
def health():
    """
    Health check endpoint
    """
    api_configured = bool(GEMINI_API_KEY)
    return jsonify({
        'status': 'healthy',
        'gemini_api_configured': api_configured
    })

if __name__ == '__main__':
    print("=" * 60)
    print("AI Language Detection Chatbot - Starting Server")
    print("=" * 60)
    print(f"Gemini API Key configured: {bool(GEMINI_API_KEY)}")
    print("Server running at: http://localhost:5000")
    print("Press CTRL+C to stop the server")
    print("=" * 60)
    app.run(debug=True, host='0.0.0.0', port=5000)
