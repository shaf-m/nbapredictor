import pandas as pd
import streamlit as st
from PIL import Image
from os import listdir

st.set_page_config(page_title="Today's NBA Predictions", layout='wide')
st.header('NBA Predictions of The Day')
st.subheader('Sunday, December 25th, 2022')
st.write('#####')
st.write('#####')

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


winnerList = []
homeTeamList = []
oppTeamList = []
for index in df3.index:
    homeTeamList.append((df3['Home/Neutral'][index]))
    oppTeamList.append((df3['Visitor/Neutral'][index]))
    winnerList.append((df3['Winners'][index]))


for x in range(len(homeTeamList)):
    st.write('#####')
    col1, col2, col3 = st.columns(3)
    with st.container():
        with col1:
            full_name = homeTeamList[x]
            last_name = (full_name.split(' '))[1]
            st.subheader("Home")
            st.subheader(full_name)
            image = Image.open(getLogo(last_name))
            st.image(image, width=100)

        with col2:
            full_name = oppTeamList[x]
            last_name = (full_name.split(' '))[1]
            st.subheader("Away")
            st.subheader(full_name)
            image = Image.open(getLogo(last_name))
            st.image(image, width=100)

        with col3:
            full_name = winnerList[x]
            last_name = (full_name.split(' '))[1]
            st.subheader("Pred. Winner")
            st.subheader(full_name)
            image = Image.open(getLogo(last_name))
            st.image(image, width=100)

        st.write('#####')
        st.write('#####')
        st.write('#####')

st.write('#####')
st.write('#####')
st.write('#####')
st.write('#####')
st.write('#####')
st.write('© Created by Shaf Muhammad')
st.write('Logos owned by the NBA')
st.write('shafmuhammad3@gmail.com')
st.write('Version 1.0.0')
