# # Code to download All videos in youtube Playlist
from pytube import Playlist
# # Get the playlist url
# playlist_url = "https://www.youtube.com/playlist?list=PLAoF4o7zqskQPz0_ntyNs5yvq39937W-x" 
# playlist = Playlist(playlist_url)

# # Get the range of videos to download
# vid_range = (0, 55)
# if vid_range[1] > len(playlist.videos):
#         vid_range = (vid_range[0], len(playlist.videos))
#         for video in range(vid_range[0], vid_range[1]):
#                 print(f"Downloading {playlist.videos[video].title}...")
#                 print(playlist.videos[video].streams.get_highest_resolution().filesize)
#                 playlist.videos[video].streams.get_highest_resolution().download()
#                 # Calculate and print the progress percentage of each video
#                 print(f"Downloaded {round(((video+1)/len(playlist.videos))*100, 2)}% of videos")

# Write a flask app to run the code
from flask import Flask, render_template, request, redirect, url_for,Response,send_file
from pytube import YouTube
from io import BytesIO
import os

app = Flask(__name__)

@app.route('/')
def index():
        return render_template('index.html')

# when user clicks on download button div is shown with checkbox and video title and thumbnail
@app.route('/downloadPlaylist/', methods=['GET', 'POST'])
def downloadPlaylist():
        if request.method == 'POST':
                url = request.form['url']
                playlist = Playlist(url)
                print(playlist.videos[0].title)
                return render_template('download.html', videos=playlist.videos)
        return render_template('download.html')

# When user clicks on download selected videos button the selected videos are downloaded
@app.route('/downloadSelected/', methods=['GET', 'POST'])
def downloadSelected():
        if request.method == 'POST':
                # url = request.form['url']
                # playlist = Playlist(url)
                selected = request.form.getlist('video')
                print(selected)

                buffer = BytesIO()
                for i in selected:
                        yt = YouTube(f"https://youtube.com/watch?v={i}")
                        # print(playlist.videos[int(i)].title)
                        stream = yt.streams.get_highest_resolution()
                        stream.stream_to_buffer(buffer=buffer)
                        buffer.seek(0)
                        return send_file( buffer,   as_attachment=True,  download_name=f"{selected.index(i)}. {yt.title}.mp4", mimetype="video/mp4",)
    
                return redirect(url_for('downloaded'))
        return render_template('downloaded.html')

# When user clicks on download all videos button all videos are downloaded
@app.route('/downloadAll/', methods=['GET', 'POST'])
def downloadAll():
        if request.method == 'POST':
                url = request.form['url']
                playlist = Playlist(url)
                buffer = BytesIO()
                for i in range(len(playlist.videos)):
                        yt =playlist.videos[i]
                        stream = yt.streams.get_highest_resolution()
                        stream.stream_to_buffer(buffer=buffer)
                        buffer.seek(0)
                        return send_file( buffer,   as_attachment=True,  download_name=f"{i}. {yt.title}.mp4", mimetype="video/mp4",)
                return redirect(url_for('downloaded'))
        return render_template('downloaded.html')
@app.route('/download/', methods=['GET', 'POST'])
def download():
        if request.method == 'POST':
                url = request.form['url']
                yt = YouTube(url)
                video = yt.streams.first()
                video.download('static/')
                return redirect(url_for('download'))
        return render_template('download.html')

@app.route('/downloaded')
def downloaded():
        return render_template('downloaded.html')

if __name__ == '__main__':
        app.run(debug=True)

