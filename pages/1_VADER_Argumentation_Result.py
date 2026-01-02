import streamlit as st
import pandas as pd
import os
from PIL import Image
# Menggunakan library resmi dari pip, bukan folder lokal
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

st.set_page_config(
    page_title="Argumentation",
    page_icon="📊"
)

# Inisialisasi Analyzer dengan Caching agar tidak dimuat ulang setiap interaksi
@st.cache_resource
def get_analyzer():
    return SentimentIntensityAnalyzer()

sid = get_analyzer()

# Setup Path Dinamis (Mengatasi masalah File Not Found)
current_dir = os.path.dirname(os.path.abspath(__file__))
# Mundur satu folder dari 'pages' ke root, lalu masuk ke 'data'
data_dir = os.path.join(current_dir, '..', 'data')
img_dir = os.path.join(current_dir, '..', 'img')

# --- KONTEN HALAMAN ---

st.write("""
# Argumentation VADER Sentiment Analysis
In using VADER for this final project using review data from the Google Play Store
""")
st.write("This is review data from the ZOOM application which was scraped using Google Collaboratory")

# Load Data Ulasan dengan Path Dinamis
try:
    df_path = os.path.join(data_dir, 'Data Ulasan.tsv')
    df = pd.read_csv(df_path, sep='\t')
    st.dataframe(df)

    # Implementation
    st.write("""
    # Implementation
    This is review data that has been implemented using VADER
    """)
    # Menambahkan type conversion ke string untuk keamanan
    df['scores'] = df['content'].apply(lambda content: sid.polarity_scores(str(content)))
    st.dataframe(df)
    st.write("The results obtained are compound, negative, neutral and positive values")

    # Labeling
    st.write("""
    # Labeling
    In this table, sentiment analysis has been applied using VADER and labeled according to the compound value.
    """)
    df['compound'] = df['scores'].apply(lambda score_dict: score_dict['compound'])
    df['label'] = df['compound'].apply(lambda c: 'P' if c >= 0.05 else 'N' if c <= -0.05 else 'NT')
    st.dataframe(df)
    st.markdown("""
    Explanation:
    - N = Negative
    - P = Positive
    - NT = Neutral
    """)
    st.write("The following are the number of positive, negative and neutral results from labeling results using VADER")
    st.table(df['label'].value_counts())

    # Manual Labeling Comparison
    st.write("""
    # Manual Labeling
    In the table below the results of the VADER labeling which have been added with manual labeling carried out by the researchers themselves.
    """)
    
    cm_path = os.path.join(data_dir, 'CM.tsv')
    if os.path.exists(cm_path):
        df1 = pd.read_csv(cm_path, sep='\t')
        st.dataframe(df1)
        st.markdown("""
        Explanation:
        - N = Negative
        - P = Positive
        - NT = Neutral
        """)
        st.write("The following are the number of positive, negative and neutral results from manual labeling")
        st.table(df1['label_manual'].value_counts())

        # Chart Comparison
        st.write("""
        # Comparison
        In the graph below shows a comparison of the results of labeling using VADER and manual labeling.
        """)
        c1, c2 = st.columns(2)
        c1.write("VADER Labeling")
        c1.bar_chart(df['label'].value_counts())
        c2.write("Manual Labeling")
        c2.bar_chart(df1['label_manual'].value_counts())
        
        y_mnl = df1['label_manual']
        # Pastikan kolom ini ada di CM.tsv, jika tidak sesuaikan nama kolomnya
        if 'label_vader' in df1.columns:
            y_vd = df1['label_vader']
            st.write("The following is the result of a cross-comparison between manual labeling and labeling using VADER")
            st.table(pd.crosstab(y_mnl, y_vd))
    else:
        st.warning("File CM.tsv not found in data folder.")

    # Conclusion & Image
    st.write("The following accuracy results are generated")
    img_path = os.path.join(img_dir, 'f1.png')
    if os.path.exists(img_path):
        image = Image.open(img_path)
        st.image(image, caption='Accuracy Results')
    
    st.write("""
    # Conclusion
    Based on the accuracy results obtained as much as 0.85 or 85%, it shows that VADER can perform sentiment analysis on a sentence or word with very good accuracy and speed.
    """)

except FileNotFoundError as e:
    st.error(f"Error loading file: {e}. Please check if the 'data' folder and files exist.")
