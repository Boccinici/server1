from flask import Flask, request, jsonify
import yt_dlp
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "ESP32 YouTube Ses Sunucusu Aktif!"

@app.route('/get_audio')
def get_audio():
    video_id = request.args.get('video_id')
    if not video_id:
        return jsonify({"error": "video_id eksik"}), 400

    youtube_url = f"https://www.youtube.com/watch?v={video_id}"

    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'quiet': True,
        'nocheckcertificate': True,
        'ignoreerrors': False,
        'logtostderr': False,
        'no_warnings': True,
        'source_address': '0.0.0.0'
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(youtube_url, download=False)
            audio_url = info['url']
            # ESP32'nin çözebilmesi için veriyi JSON formatında gönderiyoruz
            return jsonify({"audio_url": audio_url})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
