# gTTS Backend

Lightweight text-to-speech API using Google's gTTS library.

## Features
- ✅ Free, no API keys needed
- ✅ Russian language support
- ✅ Fast deployment (~30s build time)
- ✅ Works on any hardware (no GPU required)
- ✅ Simple REST API

## API Endpoints

### POST /tts
Generate speech from text.

**Request:**
```json
{
  "text": "Привет, как дела?",
  "language": "ru"
}
```

**Response:** MP3 audio file

### GET /health
Check service status.

## Local Development

```bash
pip install -r requirements.txt
python app.py
```

Server runs on `http://localhost:5000`

## Deploy to Render

1. Push code to GitHub
2. Create new Web Service on Render
3. Connect repository
4. Render will auto-detect `render.yaml`
5. Deploy!

## Usage Example

```bash
curl -X POST http://localhost:5000/tts \
  -H "Content-Type: application/json" \
  -d '{"text": "Привет"}' \
  --output speech.mp3
```
