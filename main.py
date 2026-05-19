from flask import Flask, request
import yt_dlp

app = Flask(__name__)

@app.route('/')
def home():
    return "ESP32 YouTube Ses Sunucusu Aktif!"

@app.route('/get_audio')
def get_audio():
    video_id = request.args.get('video_id')
    if not video_id:
        return "Hata: video_id eksik", 400

    youtube_url = f"https://www.youtube.com/watch?v={video_id}"

    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'quiet': True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(youtube_url, download=False)
            audio_url = info['url']
            # JSON yerine direkt linki düz metin olarak gönderiyoruz
            return str(audio_url) 
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    # Bilgisayarının yerel ağdaki IP adresinden erişilebilmesi için:
    app.run(host='0.0.0.0', port=10000)
