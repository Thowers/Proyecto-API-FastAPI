import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os

SPOTIFY_CLIENT_ID = "88e2d6bfce714876a7615cdd75939408"
SPOTIFY_CLIENT_SECRET = "0df91d516465499fa84a4fb1810e2633"

client_credentials_manager = SpotifyClientCredentials(
    client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET
)

sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)