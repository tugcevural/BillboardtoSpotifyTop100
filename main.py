import requests

import spotipy
from spotipy.oauth2 import SpotifyOAuth

from bs4 import BeautifulSoup

Spotify_client_id= "93bf756a65b04860987ddc54a9fa8141"
Client_secret = "1e1fdbf398b848779806fae322ccbdd9"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="93bf756a65b04860987ddc54a9fa8141",
                                               client_secret="1e1fdbf398b848779806fae322ccbdd9",
                                               redirect_uri="http://example.com",
                                               scope="playlist-modify-private"))

user_id=sp.current_user()["id"]

date=input("Which year do you want to travel to? Type the date in this format YYY-MM-DD:")

URL="https://www.billboard.com/charts/hot-100/"+ date

top_100_songs_url=requests.get(URL)

top100_web_page=top_100_songs_url.text

soup=BeautifulSoup(top100_web_page,"html.parser")
all_top100_songs=soup.find_all(name="h3", class_="c-title a-no-trucate a-font-primary-bold-s u-letter-spacing-0021 lrv-u-font-size-18@tablet lrv-u-font-size-16 u-line-height-125 u-line-height-normal@mobile-max a-truncate-ellipsis u-max-width-330 u-max-width-230@tablet-only")

song_list=[]
for song in all_top100_songs:
    ss =song.getText()
    a=ss.split("\n")

    song_list.append(a[5].strip())

print(song_list)


year= date.split("-")[0]
song_id_list=[]
for track in song_list:

    track_id=sp.search(q="track:"+ track + " year:" + year, type="track")

    try:
        trackId = track_id['tracks']["items"][0]["uri"]

        song_id_list.append(trackId)
    except:
        print(f"Spotify do not know this track: {track} ")

print(song_id_list)

name=f"{date} Billboard 100"
playlist=sp.user_playlist_create(user_id, name, public=False, collaborative=False, description='Top 100 songs from Billboard')

playlist_id=playlist["id"]
playlist_items=sp.playlist_add_items(playlist_id, song_id_list, position=None)











