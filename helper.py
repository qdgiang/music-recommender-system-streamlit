import pandas as pd

# read data 
song_data = pd.read_csv('data/meta_data.csv')

# set listen_count as int
song_data['listen_count'] = song_data['listen_count'].astype(int)

# load item_sim_df from pickle
item_sim_df = pd.read_pickle('data/item_sim_df.pkl')

# load user_sim_df from pickle
user_sim_df = pd.read_pickle('data/user_sim_df.pkl')

# load pivot from pickle
pivot = pd.read_pickle('data/pivot.pkl')

def get_song_id(title, artist_name):
    global song_data
    try:
        return song_data[song_data.artist_name == artist_name][song_data.title == title]['song_id'].values[0]
    except:
        return None

def get_similar_song(song_id):
    global item_sim_df
    #if song_id not in pivot_norm.index:
    if song_id not in item_sim_df.index:
        print(None)
        return None, None
    else:
        sim_songs = item_sim_df.sort_values(by=song_id, ascending=False).index[1:].tolist()
        sim_scores = item_sim_df.sort_values(by=song_id, ascending=False).loc[:, song_id].tolist()[1:]
        # return songs and scores in one dataframe
        print(type(sim_songs))
        print(type(sim_scores))
        df = pd.DataFrame({'song_id': sim_songs, 'score': sim_scores})

        # merge with song_data
        df = df.merge(song_data, on='song_id', how='left')

        # keep title, artist_name, score and listen_count
        df = df[['title', 'artist_name', 'score', 'listen_count']]

        # reset index
        df = df.reset_index(drop=True)
        return df.head(30)

# return list of similar users as well
def get_similar_song_from_user(user_id, no_of_neighbours):
    global user_sim_df
    user_row = user_sim_df.loc[user_id]
    user_row.drop(index=user_id, inplace=True)
    user_row = user_row.sort_values(ascending=False).head(no_of_neighbours)

    target_user = pivot.loc[user_id]
    target_user = target_user[target_user > 0]
    
    songs = pivot.loc[user_row.index]
    songs = songs[songs > 0]
    songs = songs.dropna(axis=1, how='all')
    songs = songs.columns.drop_duplicates().tolist()
    songs = [song for song in songs if song not in target_user.index]

    pivot_songs = pivot.loc[user_row.index, songs]
    weighted_avg = pivot_songs.mul(user_row.values, axis=0).sum(axis=0) / user_row.sum()
    weighted_avg = weighted_avg.sort_values(ascending=False)
    weighted_avg = weighted_avg.to_frame()
    weighted_avg = weighted_avg.merge(song_data, left_index=True, right_on='song_id')
    # set first column name to score
    weighted_avg.columns = ['score', 'title', 'listen_count', 'song_id', 'release','artist_name', 'year']
    weighted_avg = weighted_avg[['title', 'artist_name', 'release', 'score', 'listen_count']]
    #weighted_avg = weighted_avg[['song_id', 'title', 'artist_name', 'listen_count']]
    weighted_avg = weighted_avg.reset_index(drop=True)

    # rename user row column to score
    user_row = user_row.to_frame()
    user_row.columns = ['score']
    user_row = user_row.reset_index()
    return weighted_avg.head(30), user_row
# user history from pivot and song_data. Use listen_count on pivot
def get_user_history(user_id):
    global pivot, song_data
    user_history = pivot.loc[user_id]
    user_history = user_history[user_history > 0]
    user_history = user_history.to_frame()
    # rename second column to listen_count
    user_history.columns = ['listen_count']
    # song data drop listen_count
    user_history = user_history.merge(song_data.drop(columns=['listen_count']), left_index=True, right_on='song_id')
    
    user_history = user_history[['song_id', 'title', 'artist_name', 'listen_count']]
    user_history = user_history.sort_values(by='listen_count', ascending=False)
    user_history = user_history.reset_index(drop=True)
    return user_history

# use 5 songs for each artists
def most_listened_songs(artist_1, artist_2, artist_3):
    global song_data
    df = song_data[song_data.artist_name == artist_1].sort_values(by='listen_count', ascending=False).head(5)
    if artist_2:
        df = df.append(song_data[song_data.artist_name == artist_2].sort_values(by='listen_count', ascending=False).head(5))
    if artist_3:
        df = df.append(song_data[song_data.artist_name == artist_3].sort_values(by='listen_count', ascending=False).head(5))
    # sort by listen_count
    df = df.sort_values(by='listen_count', ascending=False)
    df = df.reset_index(drop=True)
    return df
    


        

