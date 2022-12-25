import pandas as pd
import streamlit as st
from PIL import Image
from os import listdir

st.set_page_config(page_title="Today's NBA Predictions")
st.header('NBA Predictions of The Day')
st.subheader('Sunday, December 25th, 2022')

st.empty()

df3 = pd.read_excel('predictions.xlsx')

from os import listdir
from os.path import isfile, join
mypath = '/Users/shafmuhammad/PycharmProjects/nbaapitest/nba logos'
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
onlyfiles = [x.lower() for x in onlyfiles]


def getLogo(teamLastName):
    logo = ''
    # teamLastName = 'raptors'
    for fileName in onlyfiles:
        if teamLastName.lower() in fileName:
            logo = fileName
    return f"nba logos/{logo}"


col1, col2, col3 = st.columns(3)
# st.dataframe(df3['Winners'])
with st.container():
    with col1:
        full_name = 'Toronto Raptors'
        last_name = (full_name.split(' '))[1]
        st.subheader("Home")
        st.subheader(full_name)
        image = Image.open(getLogo(last_name))
        st.image(image, width=100)

    with col2:
        full_name = 'Toronto Raptors'
        last_name = (full_name.split(' '))[1]
        st.subheader("Away")
        st.subheader(full_name)
        image = Image.open(getLogo(last_name))
        st.image(image, width=100)

    with col3:
        full_name = 'Toronto Raptors'
        last_name = (full_name.split(' '))[1]
        st.subheader("Pred. Winner")
        st.subheader(full_name)
        image = Image.open(getLogo(last_name))
        st.image(image, width=100)
