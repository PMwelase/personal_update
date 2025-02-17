import spotipy
from spotipy.oauth2 import SpotifyOAuth
import html

def create_spotify_playlist(playlist_name, description="", public=True):
    """
    Create a new Spotify playlist and return its ID.
    
    Args:
        playlist_name (str): Name of the playlist
        description (str): Description of the playlist
        public (bool): Whether the playlist should be public
    
    Returns:
        str: ID of the created playlist
    """
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id='YOUR_CLIENT_ID',
        client_secret='YOUR_CLIENT_SECRET',
        redirect_uri='YOUR_REDIRECT_URI',
        scope='playlist-modify-public playlist-modify-private'
    ))

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id='0d1bd5f0c3ed421a95517aa198ee8019',
        client_secret='12b4fa724ed54919afe16608c7e1fd3a',
        redirect_uri='http://localhost:8000/spotify_callback',
        scope='playlist-modify-public playlist-modify-private'
    ))
    
    user_id = sp.current_user()['id']
    playlist = sp.user_playlist_create(
        user=user_id,
        name=playlist_name,
        public=public,
        description=description
    )
    
    return playlist['id']

def clean_text(text):
    """
    Clean text by unescaping HTML entities and removing featuring artists.
    """
    # Unescape HTML entities
    text = html.unescape(text)
    
    # Remove 'Featuring' or '&' and everything after
    if ' Featuring ' in text:
        text = text.split(' Featuring ')[0]
    if ' & ' in text:
        text = text.split(' & ')[0]
    
    return text.strip()

def search_track(sp, title, artist):
    """
    Search for a track using title and artist, with fallback options.
    
    Args:
        sp: Spotify client instance
        title (str): Track title
        artist (str): Artist name
    
    Returns:
        str or None: Spotify track URI if found, None otherwise
    """
    # Clean the title and artist
    title = clean_text(title)
    artist = clean_text(artist)
    
    # Try exact match first
    query = f"track:{title} artist:{artist}"
    results = sp.search(q=query, type='track', limit=1)
    
    if results['tracks']['items']:
        return results['tracks']['items'][0]['uri']
    
    # Try with just title and artist without track: and artist: specifiers
    query = f"{title} {artist}"
    results = sp.search(q=query, type='track', limit=1)
    
    if results['tracks']['items']:
        return results['tracks']['items'][0]['uri']
    
    # Try with just the title as last resort
    results = sp.search(q=title, type='track', limit=1)
    
    if results['tracks']['items']:
        return results['tracks']['items'][0]['uri']
    
    return None

def create_playlist_from_billboard_data(billboard_data, playlist_name="Billboard Top Tracks", description=""):
    """
    Create a Spotify playlist from Billboard chart data.
    
    Args:
        billboard_data (dict): Dictionary containing Billboard chart data
        playlist_name (str): Name for the new playlist
        description (str): Description for the new playlist
    
    Returns:
        tuple: (playlist_id, list of found tracks, list of not found tracks)
    """
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id='YOUR_CLIENT_ID',
        client_secret='YOUR_CLIENT_SECRET',
        redirect_uri='YOUR_REDIRECT_URI',
        scope='playlist-modify-public playlist-modify-private'
    ))
    
    # Create the playlist
    playlist_id = create_spotify_playlist(playlist_name, description)
    
    # Search for each track
    track_uris = []
    not_found = []
    
    for track_info in billboard_data.values():
        title = track_info['title']
        artist = track_info['artist']
        
        track_uri = search_track(sp, title, artist)
        
        if track_uri:
            track_uris.append(track_uri)
        else:
            not_found.append(f"{title} by {artist}")
    
    # Add found tracks to playlist
    if track_uris:
        sp.playlist_add_items(playlist_id, track_uris)
    
    return playlist_id, track_uris, not_found

# Example usage
import json
with open('songs.json') as file:
    data = json.load(file)

# chart_data = json.loads(data.decode("utf-8"))

sorted_songs = sorted(data, key=lambda x: int(x['rank']))
top_ten_songs = sorted_songs[:10]

def dict_of_songs(data) -> dict:
    songs = {}
    for song in data:
        songs[song['title']] = {
            'title': song['title'],
            'artist': song['artist'],
            'rank': song['rank'],
            'thumbnail': song['image']
        }

    return songs

def main():
    billboard_data = dict_of_songs(top_ten_songs)
    
    playlist_id, found_tracks, not_found = create_playlist_from_billboard_data(
        billboard_data,
        playlist_name="Billboard Top Tracks 2025",
        description="Top tracks from the Billboard charts"
    )
    
    print(f"Created playlist with ID: {playlist_id}")
    print(f"Found and added {len(found_tracks)} tracks")
    if not_found:
        print("\nCouldn't find these tracks:")
        for track in not_found:
            print(f"- {track}")