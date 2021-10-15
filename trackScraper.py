import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd

# https://medium.com/@RareLoot/extracting-spotify-data-on-your-favourite-artist-via-python-d58bc92a4330

## Client credentials
client_id = "348f1025993b4b01a0d84eccc3e97bf0"
client_secret = "a1d600b318d5407690ac712671070685"
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager) #spotify object to access API

## Target artist
artist_list = ['Coldplay'
            #    'Justin Bieber',
            #    'The Weeknd',
            #    'Drake',
            #    'Dua Lipa',
            #    'J Balvin',
            #    'Ed Sheeran',
            #    'Ariana Grande',
            #    'Cardi B',
            #    'Khalid',
            #    'Jason Derulo',
            #    'Marshmello',
            #    'Travis Scott',
            #    'Maroon 5',
            #    'Shawn Mendes',
            #    'Halsey',
            #    'Lady Gaga',
            #    'Post Malone',
            #    'Harry Styles',
            #    'Daddy Yankee',
            #    'Bad Bunny'
               ]

def scrape(name):
    result = sp.search(name) #search query

    # Extract Artist's uri
    # Pull all of the artist's albums
    artist_uri = result['tracks']['items'][0]['artists'][0]['uri']
    artist_id = result['tracks']['items'][0]['artists'][0]['id']

    # Store artist's albums' names' and uris in separate lists
    sp_albums = sp.artist_albums(artist_uri, album_type='album')
    album_names = []
    album_uris = []
    for i in range(len(sp_albums['items'])):
        album_names.append(sp_albums['items'][i]['name'])
        album_uris.append(sp_albums['items'][i]['uri'])

    def albumSongs(uri):
        album = uri
        
        spotify_albums[album] = {} #Creates dictionary for that specific album
        
        # Create keys-values of empty lists inside nested dictionary for album
        spotify_albums[album]['albumID'] = [] #create empty list
        spotify_albums[album]['track_number'] = []
        spotify_albums[album]['id'] = []
        spotify_albums[album]['name'] = []
        spotify_albums[album]['uri'] = []
        spotify_albums[album]['artistID'] = []
        
        tracks = sp.album_tracks(album) #pull data on album tracks
        
        for n in range(len(tracks['items'])): #for each song track
            spotify_albums[album]['albumID'].append(album[14:]) #append album name tracked via album_count
            spotify_albums[album]['track_number'].append(tracks['items'][n]['track_number'])
            spotify_albums[album]['id'].append(tracks['items'][n]['id'])
            spotify_albums[album]['name'].append(tracks['items'][n]['name'])
            spotify_albums[album]['uri'].append(tracks['items'][n]['uri'])
            spotify_albums[album]['artistID'].append(artist_id)


    spotify_albums = {}
    album_count = 0
    for i in album_uris:  # each album
        albumSongs(i)
        print("Album " + str(album_names[album_count]) +
            " songs has been added to spotify_albums dictionary")
        album_count += 1  # Updates album count once all tracks have been added

    ## Add data to a new dataframe
    dic_df = {}

    dic_df['albumID'] = []
    dic_df['track_number'] = []
    dic_df['id'] = []
    dic_df['name'] = []
    dic_df['uri'] = []
    dic_df['artistID'] = []

    for album in spotify_albums:
        for feature in spotify_albums[album]:
            dic_df[feature].extend(spotify_albums[album][feature])

    df = pd.DataFrame.from_dict(dic_df)

    ## Remove duplicates
    print(len(df))
    final_df = df.drop_duplicates('name').sort_index()
    print(len(final_df))


    ## Save to CSV
    #final_df.to_csv(name + "_tracks.csv")

for artist in artist_list:
    scrape(artist)

