from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from gtts import gTTS
import io
import os
import sys

# Force UTF-8 encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

app = Flask(__name__)
CORS(app)
app.config['JSON_AS_ASCII'] = False

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok", "model": "gtts", "language": "ru"})

@app.route('/tts', methods=['POST'])
def generate_speech():
    try:
        # Log request details for debugging
        print(f"Request content type: {request.content_type}")
        print(f"Request data: {request.data}")

        # Parse JSON manually with UTF-8 encoding
        import json
        data = json.loads(request.data.decode('utf-8'))
        print(f"Parsed JSON: {data}")

        text = data.get('text', '')
        language = data.get('language', 'ru')  # Default to Russian

        if not text:
            return jsonify({"error": "No text provided"}), 400

        print(f"Generating TTS for text: {text}, language: {language}")

        # Generate speech using Google TTS
        tts = gTTS(text=text, lang=language, slow=False)

        # Save to buffer
        mp3_buffer = io.BytesIO()
        tts.write_to_fp(mp3_buffer)
        mp3_buffer.seek(0)

        print(f"TTS generated successfully, buffer size: {mp3_buffer.getbuffer().nbytes}")

        return send_file(
            mp3_buffer,
            mimetype='audio/mpeg',
            as_attachment=False
        )

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
