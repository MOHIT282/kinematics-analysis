import streamlit as st 
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(
    page_title="Kinematics Analysis",
    layout="wide",  # optional
    initial_sidebar_state="expanded",  # optional
)


st.header("Kinematics Analysis...")

file = st.sidebar.file_uploader(
    label='Upload your File here...',
    type=['csv','xlsx','txt']
)

if file:
    # cols = ['Time',
    #         'Ankle right dorsi-/plantarflexion filt (Right Leg) X *norm* X',
    #         'Torso flexion/extension (Left Leg) X *norm* X',
    #         'Ground reaction force Z X',
    #         'Hip left flexion/extension X',
    #         'Hip right flexion/extension X']
    ext = file.name.split('.')[-1]

    df = None
    if ext == 'csv':
        df = pd.read_csv(file).iloc[:10000,]
    elif ext == 'xlsx':
        df = pd.read_excel(file, engine='openpyxl').iloc[:10000]
    else:
        df = pd.read_csv(file,delimiter='\t').iloc[:10000,]
    
    df = df.drop(index=0)

    range = (df['Time'].min(), df['Time'].max())
    time_range = st.sidebar.slider(label="Select Time Range",
                      min_value=1.0,
                      max_value=range[1],
                      value=10.0)
    
    option = st.sidebar.multiselect(
        label='Select your Desired Parameter :)',
        options= df.columns[1:]
    )
    
    if time_range:
        df = df[df['Time'] <= time_range]
    fig = px.line(data_frame=df, x='Time', y=option)
    st.plotly_chart(fig, use_container_width=True)

else:
    file = None