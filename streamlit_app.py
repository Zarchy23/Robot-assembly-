import streamlit as st
import pandas as pd
import requests

API = "http://localhost:5000/ads"

st.title("Ad Tracker Dashboard")
r = requests.get(API)
data = r.json()
df = pd.DataFrame(data)
if df.empty:
    st.info("No ads yet")
else:
    st.dataframe(df)
    st.download_button("Download CSV", df.to_csv(index=False), "ads.csv")
    sel = st.selectbox("Select ad id", df['id'])
    ad = df[df['id']==sel].iloc[0]
    if ad['creative']:
        st.image(ad['creative'])