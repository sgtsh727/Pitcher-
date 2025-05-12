# MLB Pitch Tracker 2025

This Streamlit app allows you to track and compare two MLB pitchers by pitch type, velocity, and location using Statcast data via [pybaseball](https://github.com/jldbc/pybaseball).

## Features

- Compare two pitchers side-by-side
- View pitch type distributions, average velocities
- Pitch location heatmaps
- Velocity trends over time
- Export CSV of raw pitch data

## Setup

```bash
pip install -r requirements.txt
```

## Run the App

```bash
streamlit run app.py
```

## Example

Select two pitchers and a date range to analyze and compare their 2025 season performance.

## Data Source

- Statcast data via pybaseball
