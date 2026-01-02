import streamlit as st

st.set_page_config(
    page_title="Introduction",
    page_icon="📊",
    layout="wide"
)

# --- CSS STYLING ---
st.markdown("""
<style>
    .main-title {
        font-size: 3rem;
        font-weight: 800;
        text-align: center;
        color: #FF4B4B; /* Warna aksen Streamlit */
        margin-bottom: 10px;
    }
    .sub-title {
        font-size: 1.2rem;
        text-align: center;
        color: #555;
        margin-bottom: 30px;
    }
    .info-box {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #FF4B4B;
    }
</style>
""", unsafe_allow_html=True)

# --- HERO SECTION ---
st.markdown('<div class="main-title">VADER Sentiment Analysis Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Final Project Visualization & Implementation</div>', unsafe_allow_html=True)

st.markdown("---")

# --- CONTENT SECTION ---
col1, col2 = st.columns([2, 1.2], gap="large")

with col1:
    st.markdown("### 🧐 Apa itu VADER?")
    st.markdown("""
    **VADER** (*Valence Aware Dictionary and sEntiment Reasoner*) adalah alat analisis sentimen berbasis leksikon dan aturan yang secara khusus disesuaikan untuk sentimen yang diekspresikan di media sosial.
    
    Berbeda dengan metode Machine Learning tradisional yang membutuhkan data latih (training data), VADER menggunakan **kamus kata** (lexicon) yang memiliki nilai intensitas emosi.
    """)
    
    st.markdown("#### Keunggulan VADER:")
    st.success("""
    * ✅ **Sensitif terhadap Tanda Baca**: Mengenali "Good!!!" lebih positif daripada "Good".
    * ✅ **Memahami Kapitalisasi**: Mengenali "GREAT" lebih intens daripada "great".
    * ✅ **Menangani Negasi**: Paham bahwa "not good" artinya negatif.
    * ✅ **Mengenali Emoticon & Slang**: Sangat efektif untuk teks informal (seperti tweet atau ulasan).
    """)

with col2:
    st.markdown("### 🚀 Fitur Dashboard")
    with st.container(border=True):
        st.markdown("""
        **1. 📖 Introduction** Penjelasan teori dasar metode VADER.
        
        **2. 📊 Argumentation Result** Studi kasus analisis ulasan aplikasi **ZOOM** dan perbandingan akurasi dengan label manual.
        
        **3. 🎮 Live Demo** Uji coba analisis sentimen secara *real-time* dengan input teks Anda sendiri atau file batch.
        
        **4. 👤 About Me** Profil pengembang proyek ini.
        """)

# --- CITATION SECTION ---
st.markdown("---")
st.markdown("### 📚 Referensi Akademik")

st.info("""
Alat ini dibuat berdasarkan penelitian oleh **C.J. Hutto** dan **Eric Gilbert**. Jika Anda menggunakan alat ini untuk keperluan akademis, silakan merujuk pada paper berikut:

> **Hutto, C.J. & Gilbert, E.E. (2014).** > *VADER: A Parsimonious Rule-based Model for Sentiment Analysis of Social Media Text*.  
> Eighth International Conference on Weblogs and Social Media (ICWSM-14). Ann Arbor, MI, June 2014.
""")

col_link, col_empty = st.columns([1, 4])
with col_link:
    st.link_button("🔗 Lihat Repository Asli VADER", "https://github.com/cjhutto/vaderSentiment")
