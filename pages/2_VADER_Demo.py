import streamlit as st
import langid
import pandas as pd
import io
import altair as alt
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from deep_translator import GoogleTranslator

# --- CONFIGURATION ---
st.set_page_config(
    page_title="Live Demo",
    page_icon="🎮",
    layout="wide"
)

# --- CSS STYLING ---
st.markdown("""
<style>
    .stTextArea textarea {
        font-size: 16px;
    }
    .result-card {
        padding: 20px;
        border-radius: 10px;
        margin-top: 20px;
        border: 1px solid #e6e6e6;
    }
    .big-font {
        font-size: 18px !important;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# --- INITIALIZATION ---
@st.cache_resource
def get_analyzer():
    return SentimentIntensityAnalyzer()

sid = get_analyzer()

# --- HELPER FUNCTIONS ---
def translate_text(text, target='en'):
    try:
        return GoogleTranslator(source='auto', target=target).translate(text)
    except Exception as e:
        st.error(f"Translation failed: {e}")
        return text

def convert_to_excel(df):
    """Konversi DataFrame ke Bytes Excel"""
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Sentiment Results')
    return output.getvalue()

def get_sentiment_color(compound):
    if compound >= 0.05: return "#28a745" # Green
    elif compound <= -0.05: return "#dc3545" # Red
    return "#ffc107" # Yellow/Orange

# --- MAIN CONTENT ---
st.title("🎮 VADER Live Demo")
st.markdown("Uji kemampuan analisis sentimen VADER secara *real-time* atau menggunakan file dataset.")

tab1, tab2 = st.tabs(['💬 Single Sentence', '📂 Bulk File Upload'])

# ==========================================
# TAB 1: KALIMAT (SENTENCE ANALYSIS)
# ==========================================
with tab1:
    st.markdown("#### Input Text Analysis")
    
    col_input, col_result = st.columns([1.5, 1], gap="large")
    
    with col_input:
        vas = st.text_area(
            "Masukkan kalimat atau paragraf:", 
            height=150,
            placeholder="Contoh: I really love this new feature! It makes my life so much easier."
        )
        st.caption("ℹ️ Mendukung deteksi bahasa otomatis & terjemahan ke Inggris.")
        
        c_act1, c_act2 = st.columns([1, 4])
        with c_act1:
            pro = st.button("🚀 Analyze", type="primary", use_container_width=True)
        with c_act2:
            rr = st.button("🔄 Reset", use_container_width=False)

    with col_result:
        if pro and vas:
            with st.spinner('🔍 Analyzing sentiment...'):
                # 1. Deteksi Bahasa
                lang_detected, confidence = langid.classify(vas)
                
                # 2. Translasi jika perlu
                text_to_analyze = vas
                is_translated = False
                if lang_detected != 'en':
                    text_to_analyze = translate_text(vas)
                    is_translated = True
                
                # 3. Analisis VADER
                scr = sid.polarity_scores(text_to_analyze)
                cmp = scr["compound"]
                
                # --- TAMPILAN HASIL ---
                st.markdown("### Result")
                
                # Badge Bahasa
                if is_translated:
                    st.info(f"🌐 Translated from **{lang_detected}**: \n\n_{text_to_analyze}_")
                else:
                    st.success(f"🌐 Language Detected: **{lang_detected}**")

                # Kartu Skor
                sentiment_color = get_sentiment_color(cmp)
                sentiment_label = "Positive" if cmp >= 0.05 else "Negative" if cmp <= -0.05 else "Neutral"
                
                with st.container(border=True):
                    col_metric1, col_metric2 = st.columns(2)
                    col_metric1.metric("Sentiment Label", sentiment_label)
                    col_metric2.metric("Compound Score", f"{cmp:.4f}")
                    
                    # Custom Progress Bar
                    progress_val = (cmp + 1) / 2
                    st.progress(progress_val)
                    st.caption(f"Polarity Scale: {cmp} (Red: Neg, Yellow: Neu, Green: Pos)")

                # Detail JSON
                with st.expander("View Detailed Scores (JSON)"):
                    st.json(scr)

        if rr:
            st.rerun()

# ==========================================
# TAB 2: FILE UPLOAD (EXCEL SUPPORT)
# ==========================================
with tab2:
    st.markdown("#### 📂 Batch Analysis from Excel")
    st.info("Upload file Excel (`.xlsx`) yang berisi data teks. Sistem akan memproses seluruh baris sekaligus.")
    
    # 1. File Uploader khusus XLSX
    file = st.file_uploader("Upload Excel File", type=['xlsx'])
    
    if file is not None:
        try:
            # Baca Excel dengan engine openpyxl
            data_files = pd.read_excel(file, engine='openpyxl')
            
            st.write("### Preview Data")
            st.dataframe(data_files.head(), use_container_width=True)
            
            # Pilihan Kolom
            columns = data_files.columns.tolist()
            col_sel1, col_sel2 = st.columns([1, 2])
            
            with col_sel1:
                option = st.selectbox('Pilih Kolom Teks untuk Dianalisis:', columns)
            
            with col_sel2:
                st.write("") # Spacer
                st.write("") 
                prf = st.button('⚡ Process Entire File', type="primary")
            
            # Proses Data
            if prf:
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                # Simulasi progress
                status_text.text('⏳ Calculating Sentiment Scores...')
                progress_bar.progress(30)
                
                # Pastikan kolom string
                data_files['scores'] = data_files[option].astype(str).apply(
                    lambda content: sid.polarity_scores(content)
                )
                
                progress_bar.progress(60)
                status_text.text('🏷️ Assigning Labels...')
                
                # Ekstrak compound & label
                data_files['compound'] = data_files["scores"].apply(lambda d: d['compound'])
                data_files['label'] = data_files['compound'].apply(
                    lambda c: 'Positive' if c >= 0.05 else 'Negative' if c <= -0.05 else 'Neutral'
                )
                
                progress_bar.progress(100)
                status_text.text('✅ Done!')
                
                # --- VISUALISASI HASIL (CHART) ---
                st.markdown("---")
                st.markdown("### 📊 Visualisasi Hasil")
                
                # 1. Hitung Jumlah Label
                label_counts = data_files['label'].value_counts().reset_index()
                label_counts.columns = ['Sentiment', 'Count']
                
                # 2. Tampilkan Metrik
                col_m1, col_m2, col_m3 = st.columns(3)
                
                # Helper untuk ambil nilai aman
                def get_count(label):
                    val = label_counts[label_counts['Sentiment'] == label]['Count'].values
                    return val[0] if len(val) > 0 else 0
                
                with col_m1:
                    st.metric("Positive Reviews", int(get_count('Positive')), border=True)
                with col_m2:
                    st.metric("Neutral Reviews", int(get_count('Neutral')), border=True)
                with col_m3:
                    st.metric("Negative Reviews", int(get_count('Negative')), border=True)
                
                # 3. Buat Chart dengan Altair (Warna Kustom)
                # Skala Warna: Positive=Hijau, Neutral=Kuning, Negative=Merah
                chart = alt.Chart(label_counts).mark_bar().encode(
                    x=alt.X('Sentiment', sort=['Positive', 'Neutral', 'Negative']),
                    y='Count',
                    color=alt.Color(
                        'Sentiment', 
                        scale=alt.Scale(
                            domain=['Positive', 'Neutral', 'Negative'],
                            range=['#28a745', '#ffc107', '#dc3545']
                        ),
                        legend=None
                    ),
                    tooltip=['Sentiment', 'Count']
                ).properties(
                    height=350
                ).interactive()
                
                st.altair_chart(chart, use_container_width=True)
                
                # --- TABEL DATA ---
                st.markdown("### 📋 Tabel Data Lengkap")
                st.dataframe(
                    data_files,
                    column_config={
                        "compound": st.column_config.ProgressColumn(
                            "Score",
                            format="%.4f",
                            min_value=-1,
                            max_value=1,
                            help="VADER Compound Score"
                        )
                    },
                    use_container_width=True
                )
                
                # Download Section (EXCEL FORMAT)
                st.success("Analisis Selesai! Silakan unduh hasilnya.")
                
                excel_data = convert_to_excel(data_files)
                
                st.download_button(
                    label="📥 Download Result as Excel (.xlsx)",
                    data=excel_data,
                    file_name="vader_analysis_result.xlsx",
                    mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                )

        except ImportError:
            st.error("❌ Library `openpyxl` belum terinstall. Mohon tambahkan ke requirements.txt.")
        except Exception as e:
            st.error(f"❌ Terjadi kesalahan saat memproses file: {e}")
            
    else:
        # Tampilan kosong yang rapi
        st.markdown(
            """
            <div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px; border: 1px dashed #ccc; text-align: center;">
                <p style="margin: 0; color: #666;">Drag and drop file Excel (.xlsx) di sini</p>
            </div>
            """, 
            unsafe_allow_html=True
        )
