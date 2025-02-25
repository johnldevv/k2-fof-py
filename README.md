# AI Voice Assistant

A voice-enabled AI assistant that can:
- Record voice input
- Convert speech to text
- Generate AI responses
- Convert text to speech
- Support multiple languages
- Save conversations
- Load and process PDF documents

## Features
- Real-time voice recording
- Language detection and response
- Text-to-speech output
- Conversation history
- Download conversation logs
- PDF document management

## Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Create a `config.py` file with your OpenAI API key
3. Run the app:
   ```bash
   streamlit run app.py
   ```

## PDF Support
- Upload PDF documents through the interface
- Documents are stored locally for future access
- View and load previously uploaded PDFs

## API Setup

### Required API Keys
This project requires the following API key:

1. **OpenAI API Key**
   - Go to [OpenAI API Keys](https://platform.openai.com/api-keys)
   - Sign up or log in to your OpenAI account
   - Click on "Create new secret key"
   - Copy your API key
   - Estimated costs: $0.002 per 1K tokens for GPT-3.5-turbo

### Setting Up Your Keys
1. Copy the `config_template.py` file to create your own `config.py`:
   ```bash
   cp config_template.py config.py
   ```
2. Open `config.py` and replace the placeholder with your actual OpenAI API key
3. Make sure to never commit your `config.py` file with real API keys

### Security Best Practices
- Never share your API keys publicly
- Don't commit your `config.py` file to version control
- Consider using environment variables for production deployments