import pickle
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from helper import *
import base64

def img_to_bytes(img_path):
    img_bytes = Path(img_path).read_bytes()
    encoded = base64.b64encode(img_bytes).decode()
    return encoded



html_temp = """ 
<div style ="background-color:yellow;padding:13px"> 
<h1 style ="color:black;text-align:center;">Music Recommender System</h1> 
</div> 
"""
reason = """Why there are two types of sentence?
\nBecause during model training, I discover that word capitalization is THE most important factor that influence whether a word is a 
named entity, which makes a lot of sense since all names are capitalized. Therefore, I trained two models, one for formal, grammatically correct
sentence, and one for casual sentence that doesn't care about the capitalization aspect of each word"""
st.markdown(html_temp, unsafe_allow_html = True) 
st.sidebar.markdown('''[<img src='data:image/png;base64,{}' class='img-fluid' width=128 height=128>](https://streamlit.io/)'''.format(img_to_bytes("./logo2.jpg")), unsafe_allow_html=True)
st.sidebar.header('Data Mining Project')

navigation=st.sidebar.selectbox('Navigation',['Popularity-based','Collaborative Filtering','About this'])
if navigation == "Popularity-based":

    st.markdown('## **Popularity-based Recommendation**')
    col1, col2, col3 = st.columns(3)
    # 3 artists named
    with col1:
        artist1 = st.text_input('Artist 1')
    with col2:
        artist2 = st.text_input('Artist 2')
    with col3:
        artist3 = st.text_input('Artist 3')

    df = most_listened_songs(artist1, artist2, artist3)
    st.markdown('## **Users listened to these songs the most**')
    st.write(df)
    

if navigation == "Collaborative Filtering":
    st.markdown('## **Collaborative Filtering Recommendation**')
    method = st.radio("Choose the method", ("User-based", "Item-based"))

    if method == "User-based":
        user_id = st.text_input("User ID", key="user_id_user_based")
        if user_id:
            df, sim_users = get_similar_song_from_user(user_id, 10)
            user_history = get_user_history(user_id)
            st.markdown('## **User History**')
            st.write(user_history)
            st.markdown('## **Similar users ID**')
            st.write(sim_users)
            st.markdown('## **Users like you also listen to**')
            df
    else:

        col1, col2 = st.columns(2)
        with col1:
            song_name = st.text_input("Song Name", key="song_name_item_based", value="The Scientist")
        with col2:
            artist_name = st.text_input("Artist Name", key="artist_name_item_based", value="Coldplay")
        if st.button("Submit"):
            if song_name and artist_name:
                song_id = get_song_id(song_name, artist_name)
                if song_id is None:
                    st.markdown('**No such song in the database**')
                df = get_similar_song(song_id)
                st.markdown('## **Users listened to this song also listen to**')
                df

            else:
                st.write("Please enter both song name and artist name")


if navigation == "About this":
    st.markdown("")
    st.markdown("This is a web app for assigment for the **Data Mining** course. Notebooks for generating the models are included in the **Github** repository, please check it out :D.")
    st.markdown("*https://github.com/qdgiang01*")