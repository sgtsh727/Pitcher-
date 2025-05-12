import streamlit as st
import pandas as pd
from pybaseball import statcast_pitcher, playerid_lookup
from datetime import datetime
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import io

st.set_page_config(page_title="MLB Pitch Tracker 2025", layout="wide")
st.title("MLB Pitcher Comparison - 2025 Season")

# Sidebar - Pitcher 1
st.sidebar.header("Pitcher 1")
first_name1 = st.sidebar.text_input("First Name", "Shohei")
last_name1 = st.sidebar.text_input("Last Name", "Ohtani")

# Sidebar - Pitcher 2
st.sidebar.header("Pitcher 2")
first_name2 = st.sidebar.text_input("First Name ", "Gerrit")
last_name2 = st.sidebar.text_input("Last Name ", "Cole")

# Date range
st.sidebar.header("Date Range")
start_date = st.sidebar.date_input("Start Date", datetime(2025, 3, 28))
end_date = st.sidebar.date_input("End Date", datetime.today())

if st.sidebar.button("Compare Pitchers"):
    def get_pitcher_data(first, last):
        info = playerid_lookup(last, first)
        if info.empty:
            return None, None
        pid = info.iloc[0]["key_mlbam"]
        name = f"{first} {last}"
        data = statcast_pitcher(start_date.strftime('%Y-%m-%d'),
                                end_date.strftime('%Y-%m-%d'),
                                pid)
        return name, data

    name1, df1 = get_pitcher_data(first_name1, last_name1)
    name2, df2 = get_pitcher_data(first_name2, last_name2)

    if df1 is None or df1.empty or df2 is None or df2.empty:
        st.error("One or both pitchers not found or no data available.")
    else:
        col1, col2 = st.columns(2)

        with col1:
            st.subheader(f"{name1} - Pitch Summary")
            pitch_counts1 = df1['pitch_type'].value_counts().reset_index()
            pitch_counts1.columns = ['Pitch Type', 'Count']
            st.dataframe(pitch_counts1)
            fig1 = px.bar(pitch_counts1, x='Pitch Type', y='Count', title=f"{name1} - Pitch Types")
            st.plotly_chart(fig1)

            avg_velo1 = df1.groupby('pitch_type')['release_speed'].mean().reset_index()
            avg_velo1.columns = ['Pitch Type', 'Avg Velocity']
            fig2 = px.bar(avg_velo1, x='Pitch Type', y='Avg Velocity',
                          title=f"{name1} - Velocity by Pitch")
            st.plotly_chart(fig2)

        with col2:
            st.subheader(f"{name2} - Pitch Summary")
            pitch_counts2 = df2['pitch_type'].value_counts().reset_index()
            pitch_counts2.columns = ['Pitch Type', 'Count']
            st.dataframe(pitch_counts2)
            fig3 = px.bar(pitch_counts2, x='Pitch Type', y='Count', title=f"{name2} - Pitch Types")
            st.plotly_chart(fig3)

            avg_velo2 = df2.groupby('pitch_type')['release_speed'].mean().reset_index()
            avg_velo2.columns = ['Pitch Type', 'Avg Velocity']
            fig4 = px.bar(avg_velo2, x='Pitch Type', y='Avg Velocity',
                          title=f"{name2} - Velocity by Pitch")
            st.plotly_chart(fig4)

        # Combine for trend
        st.subheader("Pitch Velocity Over Time")
        df1['date'] = pd.to_datetime(df1['game_date'])
        df2['date'] = pd.to_datetime(df2['game_date'])
        df1['Pitcher'] = name1
        df2['Pitcher'] = name2
        combined = pd.concat([df1, df2])

        trend_data = combined.groupby(['date', 'Pitcher'])['release_speed'].mean().reset_index()
        trend_fig = px.line(trend_data, x='date', y='release_speed', color='Pitcher',
                            title='Average Pitch Velocity Over Time')
        st.plotly_chart(trend_fig)

        # Heatmaps
        st.subheader("Pitch Location Heatmaps")
        h1, h2 = st.columns(2)
        if 'plate_x' in df1.columns and 'plate_z' in df1.columns:
            with h1:
                fig5, ax1 = plt.subplots()
                sns.kdeplot(x=df1['plate_x'], y=df1['plate_z'], fill=True, cmap='coolwarm', bw_adjust=0.5, ax=ax1)
                ax1.set_xlim(-2, 2)
                ax1.set_ylim(0, 5)
                ax1.set_title(f"{name1} - Pitch Location")
                st.pyplot(fig5)

        if 'plate_x' in df2.columns and 'plate_z' in df2.columns:
            with h2:
                fig6, ax2 = plt.subplots()
                sns.kdeplot(x=df2['plate_x'], y=df2['plate_z'], fill=True, cmap='coolwarm', bw_adjust=0.5, ax=ax2)
                ax2.set_xlim(-2, 2)
                ax2.set_ylim(0, 5)
                ax2.set_title(f"{name2} - Pitch Location")
                st.pyplot(fig6)

        # Export options
        st.subheader("Export Data")
        csv1 = df1.to_csv(index=False).encode('utf-8')
        csv2 = df2.to_csv(index=False).encode('utf-8')

        st.download_button(
            label=f"Download {name1} Data as CSV",
            data=csv1,
            file_name=f"{name1.replace(' ', '_')}_data.csv",
            mime='text/csv')

        st.download_button(
            label=f"Download {name2} Data as CSV",
            data=csv2,
            file_name=f"{name2.replace(' ', '_')}_data.csv",
            mime='text/csv')
