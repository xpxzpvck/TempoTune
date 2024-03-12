from flask import Flask, render_template, request, redirect, url_for, session
from pymongo import MongoClient
from bson.objectid import ObjectId
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
from random import getrandbits
from datetime import datetime
from ast import literal_eval

uri = "mongodb+srv://yurora:tempotune123official@cluster0.pkxylky.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(uri)
db = client['TempoTune']
users = db["users"]
app = Flask(__name__)
app.secret_key=['very_secret']
spotify_client=spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id="f17426cd426c406eb0909cb148cb0981",client_secret='0f16e1667986460c9841c0aa0944415a'))

def milliseconds_to_string_duration(milliseconds):
    seconds, milliseconds = divmod(milliseconds, 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)

    duration_string = "{:02}:{:02}".format(minutes, seconds)

    if hours > 0:
        duration_string = "{:02}:{:02}".format(hours, duration_string)

    return duration_string

class Song:
    def __init__(self, name, artist, url, duration,
                 preview_url, cover_big, cover_medium, cover_small):
        self.name = name
        self.artist = artist
        self.url = url
        self.duration = duration
        self.preview_url = preview_url
        self.cover_big = cover_big
        self.cover_medium = cover_medium
        self.cover_small = cover_small

    def __repr__(self):
        return f'{self.name} by {self.artist}'

class Playlist:
    def __init__(self, track, limit, instrumentalness, energy, danceability, valence, popularity, acousticness):
        self.id = getrandbits(128)
        self.songs = []
        self.total_duration=0
        current_day = datetime.now().day
        current_month = datetime.now().month
        current_year = datetime.now().year
        self.date = f'{current_day}.{current_month}.{current_year}'
        recomendations = spotify_client.recommendations(seed_tracks=[track], limit=limit, target_instrumentalness=instrumentalness, target_energy=energy, target_danceability=danceability, target_valence=valence, target_popularity=popularity, target_acousticness=acousticness)
        recomendations = recomendations['tracks']
        for track in recomendations:
            name = track['name']
            artist = ', '.join([artist['name'] for artist in track['artists']])
            url = track['external_urls']['spotify']
            duration = track['duration_ms']
            self.total_duration+=duration
            duration=milliseconds_to_string_duration(duration)
            preview_url = track['preview_url']
            cover_big = track['album']['images'][0]['url']
            cover_medium = track['album']['images'][1]['url']
            cover_small = track['album']['images'][2]['url']
            song = Song(name, artist, url, duration, preview_url,
                        cover_big, cover_medium, cover_small)
            self.songs.append(song.__dict__)
        self.total_duration=milliseconds_to_string_duration(self.total_duration)

    def __repr__(self):
        return f'{self.total_duration}{[(song.url, song.duration) for song in self.songs]}'

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if "email" in session:
        return redirect(url_for('playlists'))
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        f_user=users.find_one({'email':email})
        if not username or not email or not password:
            message = 'All fields are required'
            return render_template('login.html', message=message)
        if not f_user:
            message = 'User with such email does not exist'
            return render_template('login.html', message=message)
        if f_user['username']!=username or f_user['password']!=password:
            message = 'Wrong username or password'
            return render_template('login.html', message=message)
        session["email"]=email
        return redirect(url_for('index'))
    return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if "email" in session:
        return redirect(url_for('playlists'))
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        if not username or not email or not password:
            message = 'All fields are required'
            return render_template('signup.html', message=message)
        if users.find_one({'email':email}):
            message = 'User with such email already exists'
            return render_template('signup.html', message=message)
        users.insert_one(
            {'username': username, 'email': email, 'password': password, 'playlists': []})
        return redirect(url_for('index'))
    return render_template('signup.html')


@app.route('/playlists')
def playlists():
    user = users.find_one({"email" : session["email"]})
    name = user['username']
    playlists = user['playlists']
    playlists = [literal_eval(playlist) for playlist in playlists]
    return render_template('playlists.html', name=name, playlists=playlists)


@app.route('/songs/<playlist_id>')
def songs(playlist_id):
    playlists_ = users.find_one({"email" : session["email"]})['playlists']
    playlists = [literal_eval(playlist) for playlist in playlists_]
    playlist = [playlist for playlist in playlists if playlist['id'] == int(playlist_id)][0]
    return render_template('songs.html', playlist=playlist)

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    if "email" in session:
        session.pop("email", None)
    return render_template("index.html")


@app.route('/generate', methods=['GET', 'POST'])
def generate():
    if request.method == 'POST':
        song = request.form['song']
        if 'open.spotify.com' not in song:
            song = spotify_client.search(q=song, type='track')['tracks']['items'][0]['external_urls']['spotify']
        song_amount = request.form['song_amount']
        instrumentalness = request.form['instrumentalness']*0.01 if request.form['instrumentalness']!=0.5 else None
        energy = request.form['energy']*0.01 if request.form['energy']!=0.5 else None
        danceability = request.form['danceability']*0.01 if request.form['danceability']!=0.5 else None
        valence = request.form['valence']*0.01 if request.form['valence']!=0.5 else None
        popularity = request.form['popularity'] if request.form['popularity']!=50 else None
        acousticness = request.form['acousticness']*0.01 if request.form['acousticness']!=0.5 else None
        playlist = Playlist(song, int(song_amount), instrumentalness, energy, danceability, valence, popularity, acousticness)
        return render_template('generate.html', playlist=playlist)
    return render_template('generate.html')


if __name__ == '__main__':
    app.run(debug=True)
