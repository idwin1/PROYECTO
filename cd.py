import yt_dlp as youtube_dl

def descargar_video(url):

    ydl_opts = {
        'format':'bestvideo/best',
        'outtmp1':'%(title)s.%(ext)s'
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

url ="https://www.youtube.com/watch?v=nHNLUanxUUM"

descargar_video(url)