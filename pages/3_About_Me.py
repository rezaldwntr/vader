import streamlit as st
from PIL import Image
import os

st.set_page_config(
    page_title="About Me",
    page_icon="👨‍💻", # Menggunakan icon dari kode lama Anda
    layout="wide"
)

# --- CSS STYLING ---
# Membuat foto profil bulat dan styling font
st.markdown("""
<style>
    .profile-img {
        border-radius: 50%;
        display: block;
        margin-left: auto;
        margin-right: auto;
        object-fit: cover;
        border: 4px solid #FF4B4B;
        box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);
    }
    .main-title {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        color: #31333F;
    }
    .subtitle {
        font-size: 1.2rem;
        color: #666;
        font-style: italic;
        margin-bottom: 1.5rem;
    }
    .social-link {
        margin-right: 15px;
        text-decoration: none;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# --- SETUP PATH ---
current_dir = os.path.dirname(os.path.abspath(__file__))
img_dir = os.path.join(current_dir, '..', 'img')

# --- HEADER SECTION ---
col1, col2 = st.columns([1, 2.5], gap="large")

with col1:
    # Load foto profil (profile.png di folder img)
    profile_pic_path = os.path.join(img_dir, 'profile.png')
    
    if os.path.exists(profile_pic_path):
        image = Image.open(profile_pic_path)
        # Menampilkan gambar dengan class CSS untuk membuatnya bulat (perlu trik st.image atau markdown html)
        # Streamlit standard image:
        st.image(image, width=220, caption="Husna Rezal Dewantara")
    else:
        # Placeholder jika foto belum diupload
        st.info("⚠️ Silakan upload foto profil bernama 'profile.png' ke folder 'img'.")
        st.write("📷 [Foto Profil]")

with col2:
    st.markdown('<div class="main-title">Husna Rezal Dewantara, S.Kom</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Computer Science Graduate | NLP Enthusiast</div>', unsafe_allow_html=True)
    
    st.write("""
    Halo! Saya lulusan S-1 Ilmu Komputer dari **Universitas Lambung Mangkurat (ULM)**, Indonesia. 
    Saya memiliki ketertarikan mendalam pada Data Science, khususnya dalam pemrosesan bahasa alami (NLP).
    Project ini adalah demonstrasi kemampuan analisis sentimen menggunakan algoritma VADER.
    """)
    
    st.markdown("---")
    
    # --- SOCIAL LINKS ---
    st.write("### 📬 Connect with Me")
    c_btn1, c_btn2, c_btn3 = st.columns(3)
    
    with c_btn1:
        # Link LinkedIn dari data Anda
        st.link_button("👔 LinkedIn", "https://www.linkedin.com/in/husna-rezal-dewantara/")
    
    with c_btn2:
        # Link Instagram dari data Anda
        st.link_button("📸 Instagram", "https://www.instagram.com/rezaldwntr/")
        
    with c_btn3:
        # Link GitHub (Diasumsikan dari username repo)
        st.link_button("💻 GitHub", "https://github.com/rezaldwntr")

# --- DETAIL TABS ---
st.markdown("<br>", unsafe_allow_html=True)
tab_edu, tab_skill, tab_about = st.tabs(["🎓 Pendidikan", "🛠️ Keahlian", "📌 Tentang Project"])

with tab_edu:
    st.subheader("Riwayat Pendidikan")
    st.markdown("""
    **S-1 Ilmu Komputer (Computer Science)**
    * **Universitas Lambung Mangkurat (ULM)** - Indonesia
    * **Tahun Lulus:** 2022
    """)

with tab_skill:
    st.subheader("Technical Skills")
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("**Bahasa & Framework:**")
        st.markdown("- Python")
        st.markdown("- Streamlit")
        st.markdown("- SQL")
    with col_b:
        st.markdown("**Data Science:**")
        st.markdown("- Natural Language Processing (VADER, NLTK)")
        st.markdown("- Data Analysis (Pandas, NumPy)")
        st.markdown("- Data Visualization")

with tab_about:
    st.subheader("Tentang Dashboard Ini")
    st.info("""
    Dashboard ini dibangun sebagai bagian dari portofolio/tugas akhir untuk mendemonstrasikan 
    penerapan **VADER (Valence Aware Dictionary and sEntiment Reasoner)** dalam menganalisis sentimen 
    ulasan aplikasi Zoom di Google Play Store.
    """)
    st.markdown("Fitur utama meliputi: Analisis Teks Real-time, Dukungan Multi-bahasa, dan Pemrosesan File Batch (TSV/CSV).")

# --- FOOTER ---
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #888; font-size: 0.8em;'>
        © 2022 Husna Rezal Dewantara | Built with Streamlit
    </div>
    """, 
    unsafe_allow_html=True
)
