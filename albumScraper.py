import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import csv

## Client credentials
client_id = "348f1025993b4b01a0d84eccc3e97bf0"
client_secret = "a1d600b318d5407690ac712671070685"
client_credentials_manager = SpotifyClientCredentials(
    client_id=client_id, client_secret=client_secret)
# spotify object to access API
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

## Target artists
artist_list = ['Coldplay',
               'Justin Bieber',
               'The Weeknd',
               'Drake',
               'Dua Lipa',
               'J Balvin',
               'Ed Sheeran',
               'Ariana Grande',
               'Cardi B',
               'Khalid',
               'Jason Derulo',
               'Marshmello',
               'Travis Scott',
               'Maroon 5',
               'Shawn Mendes',
               'Halsey',
               'Lady Gaga',
               'Post Malone',
               'Harry Styles',
               'Daddy Yankee',
               'Bad Bunny'
               ]

def scrape(artist_list):
    spotify_albums = {}
    for artist in artist_list:
        result = sp.search(artist)  # search query
        artist_uri = result['tracks']['items'][0]['artists'][0]['uri']
        artist_id = result['tracks']['items'][0]['artists'][0]['id']
        sp_albums = sp.artist_albums(artist_uri, album_type='album')

        for i in range(len(sp_albums['items'])):
            uri = sp_albums['items'][i]['uri']
            spotify_albums[uri] = {}

            spotify_albums[uri]['name'] = sp_albums['items'][i]['name']
            spotify_albums[uri]['artistID'] = artist_id
            spotify_albums[uri]['id'] = sp_albums['items'][i]['id']
            spotify_albums[uri]['imageURL'] = sp_albums['items'][i]['images'][0]['url']
            spotify_albums[uri]['uri'] = uri

    final_list = []
    for s in spotify_albums:
        final_list.append(spotify_albums[s])
    
    csv_file = "album_list.csv"
    csv_columns = ['name', 'artistID', 'id', 'imageURL', 'uri']
    with open(csv_file, "w") as outfile:
        writer = csv.DictWriter(outfile, fieldnames=csv_columns)
        writer.writeheader()
        for s in final_list:
            writer.writerow(s)
        print("album_list.csv generated")

### Run Scrape
scrape(artist_list)
