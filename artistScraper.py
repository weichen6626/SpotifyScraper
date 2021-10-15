import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import csv

## Client credentials
client_id = "348f1025993b4b01a0d84eccc3e97bf0"
client_secret = "a1d600b318d5407690ac712671070685"
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager) #spotify object to access API

## Target artist
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
    spotify_artists = {}
    
    for artist in artist_list:
        result = sp.search(artist) #search query
        artist_uri = result['tracks']['items'][0]['artists'][0]['uri']
        artist_data = sp.artist(artist_uri)

        spotify_artists[artist_uri] = {}
        spotify_artists[artist_uri]['name'] = artist
        spotify_artists[artist_uri]['uri'] = artist_uri
        spotify_artists[artist_uri]['id'] = artist_data['id']
        spotify_artists[artist_uri]['image'] = artist_data['images'][0]['url']
        spotify_artists[artist_uri]['genre'] = artist_data['genres'][0]

    final_list = []
    for s in spotify_artists:
        final_list.append(spotify_artists[s])
    
    csv_file = "artist_list.csv"
    csv_columns = ['name', 'uri', 'id', 'image', 'genre']
    with open(csv_file, "w") as outfile:
        writer = csv.DictWriter(outfile, fieldnames=csv_columns)
        writer.writeheader()
        for s in final_list:
            writer.writerow(s)
        print("artist_list.csv generated")

### run scrape
scrape(artist_list)



