<div align="center">
  <img src="static/img/logo.png" alt="TempoTune Logo"/>
  <h1>TempoTune</h1>
  <p>Create personalized music playlists based on mood, energy, and your favorite tracks</p>
</div>

## 📚 Overview

TempoTune is a web application that leverages the Spotify API to generate personalized music playlists. By adjusting different parameters like energy, danceability, and acousticness, users can create custom playlists matching their specific mood or taste.

## 📹 Demo

<div align="center">
  <a href="https://www.youtube.com/watch?v=fc4AYiUY7rI" target="_blank">
    <img src="https://img.youtube.com/vi/fc4AYiUY7rI/0.jpg" alt="TempoTune Preview" width="600">
  </a>
  <p>Preview:</p>
</div>

<div align="center">
  <a href="https://www.youtube.com/watch?v=D9MR4F8a4zY" target="_blank">
    <img src="https://img.youtube.com/vi/D9MR4F8a4zY/0.jpg" alt="TempoTune Saving to Spotify" width="600">
  </a>
  <p>Saving to Spotify:</p>
</div>

## ✨ Features

- Generate playlists based on seed tracks or random genres
- Customize playlists using mood parameters:
  - Instrumentalness
  - Energy
  - Danceability
  - Valence (mood/positivity)
  - Popularity
  - Acousticness
- Control the number of songs in your playlist (up to 50)
- Save playlists to your account
- Export playlists directly to your Spotify account
- Listen to 30-second previews of songs when available
- User account system to save and manage playlists

## 🖥️ Technologies

- **Backend**: Python, Flask
- **Database**: MongoDB
- **Authentication**: Session-based authentication
- **API Integration**: Spotify Web API
- **Deployment**: Waitress WSGI server

## 🚀 Getting Started

### Prerequisites

- Python 3.7+
- MongoDB
- Spotify Developer Account

### Environment Variables

Set up the following environment variables:

```
MONGO_URI=your_mongodb_connection_string
CLIENT_ID=your_spotify_client_id
CLIENT_SECRET=your_spotify_client_secret
SECRET_KEY=your_flask_secret_key
PORT=8000 (optional)
```

### Installation

1. Clone the repository
```bash
git clone https://github.com/xpxzpvck/tempotune
cd tempotune
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Start the application
```bash
python app.py
```

The application will be available at `http://localhost:8000`

## 💡 How to Use

1. **Create a Playlist**:
   - Navigate to the "Generate" page
   - Optionally enter a seed track (Spotify URL or search query)
   - Adjust the mood parameters to your preference
   - Set the number of songs you want
   - Click "Generate"

2. **Save a Playlist**:
   - After generating a playlist, give it a name
   - Click "Save Playlist"
   - The playlist will be saved to your account

3. **Export to Spotify**:
   - Open a saved playlist
   - Click "Export to Spotify"
   - Authorize TempoTune to access your Spotify account
   - The playlist will be created in your Spotify library

4. **Manage Playlists**:
   - View all your saved playlists on the "Playlists" page
   - Delete unwanted playlists or individual songs