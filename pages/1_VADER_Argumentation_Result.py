import streamlit as st
import pandas as pd
import os
from PIL import Image
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# --- CONFIGURATION ---
st.set_page_config(
    page_title="Argumentation Results",
    page_icon="📊",
    layout="wide"
)

# --- CSS STYLING ---
st.markdown("""
<style>
    .header-style {
        font-size: 26px;
        font-weight: 700;
        color: #31333F;
        margin-bottom: 20px;
    }
    .sub-header {
        font-size: 18px;
        color: #666;
        margin-bottom: 10px;
    }
    .metric-card {
        background-color: #f9f9f9;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #ddd;
    }
</style>
""", unsafe_allow_html=True)

# --- INITIALIZATION ---
@st.cache_resource
def get_analyzer():
    return SentimentIntensityAnalyzer()

sid = get_analyzer()

# Setup Path
current_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(current_dir, '..', 'data')
img_dir = os.path.join(current_dir, '..', 'img')

# --- HEADER ---
st.title("📊 Argumentation: VADER Analysis Result")
st.markdown("Studi kasus analisis sentimen pada ulasan aplikasi **ZOOM** (Google Play Store).")
st.markdown("---")

# --- MAIN CONTENT ---
try:
    # 1. LOAD DATA SECTION
    df_path = os.path.join(data_dir, 'Data Ulasan.tsv')
    df = pd.read_csv(df_path, sep='\t')
    
    with st.expander("📂 Klik untuk melihat Dataset Awal (Raw Data)", expanded=False):
        st.dataframe(df, use_container_width=True)

    # 2. IMPLEMENTATION SECTION
    st.markdown('<div class="header-style">1. VADER Implementation & Scoring</div>', unsafe_allow_html=True)
    
    col_desc, col_process = st.columns([1, 2])
    with col_desc:
        st.info("""
        Proses ini menghitung skor polaritas untuk setiap ulasan.
        Skor **Compound** adalah metrik utama normalisasi (-1 s/d 1).
        """)
    
    with col_process:
        # Proses Analisis
        df['scores'] = df['content'].apply(lambda content: sid.polarity_scores(str(content)))
        
        # Ekstrak compound untuk visualisasi dataframe
        df['compound'] = df['scores'].apply(lambda d: d['compound'])
        
        # Tampilkan Dataframe dengan Bar Chart mini pada kolom Compound
        st.dataframe(
            df[['content', 'compound']],
            column_config={
                "compound": st.column_config.ProgressColumn(
                    "Sentiment Score",
                    help="Nilai Compound VADER",
                    format="%.4f",
                    min_value=-1,
                    max_value=1,
                ),
            },
            use_container_width=True,
            height=300
        )

    st.markdown("---")

    # 3. LABELING SECTION
    st.markdown('<div class="header-style">2. Labeling & Distribution</div>', unsafe_allow_html=True)

    # Logika Labeling
    df['label'] = df['compound'].apply(lambda c: 'Positive' if c >= 0.05 else 'Negative' if c <= -0.05 else 'Neutral')
    
    # Hitung Distribusi
    label_counts = df['label'].value_counts()
    
    # Tampilkan Metrik Besar
    m1, m2, m3 = st.columns(3)
    m1.metric("Positive Reviews", label_counts.get('Positive', 0), ">= 0.05")
    m2.metric("Neutral Reviews", label_counts.get('Neutral', 0), "-0.05 < x < 0.05")
    m3.metric("Negative Reviews", label_counts.get('Negative', 0), "<= -0.05")
    
    # Grafik Distribusi
    st.bar_chart(label_counts, color=["#4CAF50"]) # Hijau sederhana

    st.markdown("---")

    # 4. COMPARISON SECTION (MANUAL VS VADER)
    st.markdown('<div class="header-style">3. Validation: Manual vs VADER</div>', unsafe_allow_html=True)
    
    cm_path = os.path.join(data_dir, 'CM.tsv')
    if os.path.exists(cm_path):
        df1 = pd.read_csv(cm_path, sep='\t')
        
        # Mapping label agar seragam jika di file CM masih singkatan
        # Asumsi: label_manual di file CM berisi 'P', 'N', 'NT' atau 'Positive' dst.
        # Kita biarkan apa adanya untuk chart, tapi pastikan data terbaca
        
        tab_comp1, tab_comp2 = st.tabs(["📉 Visual Comparison", "📋 Confusion Matrix Data"])
        
        with tab_comp1:
            c1, c2 = st.columns(2)
            with c1:
                st.subheader("VADER Prediction")
                # Gunakan data df utama
                st.bar_chart(df['label'].value_counts(), color="#FF4B4B")
            
            with c2:
                st.subheader("Manual Ground Truth")
                # Gunakan data CM
                st.bar_chart(df1['label_manual'].value_counts(), color="#0068C9")
        
        with tab_comp2:
            st.write("Cross-tabulation (Confusion Matrix) antara Manual vs VADER:")
            if 'label_vader' in df1.columns:
                 ct = pd.crosstab(df1['label_manual'], df1['label_vader'])
                 st.dataframe(ct, use_container_width=True)
            else:
                st.warning("Kolom 'label_vader' tidak ditemukan di CM.tsv")

    else:
        st.warning("File CM.tsv (Data Pembanding) tidak ditemukan.")

    st.markdown("---")

    # 5. CONCLUSION SECTION
    st.markdown('<div class="header-style">4. Conclusion & Accuracy</div>', unsafe_allow_html=True)
    
    col_con_img, col_con_text = st.columns([1, 2])
    
    with col_con_img:
        img_path = os.path.join(img_dir, 'f1.png')
        if os.path.exists(img_path):
            image = Image.open(img_path)
            st.image(image, caption='F1-Score / Accuracy Matrix', use_container_width=True)
        else:
            st.text("Image not found")
            
    with col_con_text:
        # Menggunakan Container berborder untuk kesimpulan
        with st.container(border=True):
            st.markdown("### 🏆 Final Accuracy: 85%")
            st.markdown("""
            Berdasarkan hasil pengujian komparasi antara VADER dan pelabelan manual:
            
            * **Akurasi Tinggi:** VADER mencapai tingkat akurasi **85%** pada dataset ulasan Zoom.
            * **Efisiensi:** Mampu memproses ribuan ulasan dalam hitungan detik tanpa memerlukan pelatihan model (training) yang berat.
            * **Kesimpulan:** VADER terbukti efektif sebagai solusi *Lexicon-based* untuk analisis sentimen cepat pada teks berbahasa Inggris.
            """)

except FileNotFoundError as e:
    st.error(f"❌ Error loading file: {e}. Please ensure 'Data Ulasan.tsv' exists in the 'data' folder.")
except Exception as e:
    st.error(f"⚠️ An unexpected error occurred: {e}")
