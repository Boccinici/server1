from flask import Flask, request, jsonify
import yt_dlp

app = Flask(__name__)

@app.route('/')
def home():
    return "ESP32 YouTube Ses Sunucusu Aktif!"

@app.route('/get_audio')
def get_audio():
    # ESP32'den gelen video ID'sini veya URL'sini alıyoruz
    video_id = request.args.get('video_id')
    if not video_id:
        return jsonify({"error": "video_id parametresi eksik"}), 400

    # YouTube URL'sini oluşturuyoruz
    youtube_url = f"https://www.youtube.com/watch?v={video_id}"

    # Sadece ham ses linkini çözmek için yt_dlp ayarları
    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'quiet': True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(youtube_url, download=False)
            # ESP32'nin doğrudan çalabileceği ham ses URL'si
            audio_url = info['url']
            return jsonify({"audio_url": audio_url})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
