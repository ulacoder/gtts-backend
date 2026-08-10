from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from gtts import gTTS
import io
import os

app = Flask(__name__)
CORS(app)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok", "model": "gtts", "language": "ru"})

@app.route('/tts', methods=['POST'])
def generate_speech():
    try:
        data = request.get_json(force=True)
        text = data.get('text', '')
        language = data.get('language', 'ru')  # Default to Russian

        if not text:
            return jsonify({"error": "No text provided"}), 400

        # Generate speech using Google TTS
        tts = gTTS(text=text, lang=language, slow=False)

        # Save to buffer
        mp3_buffer = io.BytesIO()
        tts.write_to_fp(mp3_buffer)
        mp3_buffer.seek(0)

        return send_file(
            mp3_buffer,
            mimetype='audio/mpeg',
            as_attachment=False
        )

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
