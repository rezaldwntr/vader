import streamlit as st
import langid
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from deep_translator import GoogleTranslator

st.set_page_config(
    page_title="Demo",
    page_icon="📝"
)

# Caching Analyzer
@st.cache_resource
def get_analyzer():
    return SentimentIntensityAnalyzer()

sid = get_analyzer()

# Fungsi Helper untuk Translasi
def translate_text(text, target='en'):
    try:
        return GoogleTranslator(source='auto', target=target).translate(text)
    except Exception as e:
        st.error(f"Translation failed: {e}")
        return text

# Fungsi Helper untuk Download
def convert_df(data_files):
    # Menggunakan index=False agar file output lebih bersih
    return data_files.to_csv(index=False).encode('utf-8')

# --- KONTEN HALAMAN ---
st.write("""
# VADER Sentiment Analysis
""")

tab1, tab2 = st.tabs(['Sentence', 'Files'])

# --- TAB 1: KALIMAT ---
with tab1:
    vas = st.text_input("Enter the word or sentence you want to do sentiment analysis.", value='')
    st.caption("This version supports auto-translation to English for analysis.")
    
    col1, col2 = st.columns([1, 5])
    with col1:
        pro = st.button("Process")
    with col2:
        rr = st.button("Reset / Clear")

    if pro and vas:
        # Deteksi Bahasa
        lang_detected, confidence = langid.classify(vas)
        st.write(f'Detected Language: **{lang_detected}**')
        
        with st.spinner('Performing Analytical Calculations...'):
            text_to_analyze = vas
            
            # Jika bukan bahasa Inggris, translate dulu
            if lang_detected != 'en':
                translated_text = translate_text(vas)
                st.info(f"Translated to English: *{translated_text}*")
                text_to_analyze = translated_text
            
            scr = sid.polarity_scores(text_to_analyze)
            
            # Tampilkan Hasil Skor
            st.json(scr)
            
            cmp = scr["compound"]
            if cmp >= 0.05:
                st.success(f"Positive (Compound: {cmp})")
            elif cmp <= -0.05:
                st.error(f"Negative (Compound: {cmp})")
            else:
                st.warning(f"Neutral (Compound: {cmp})")
        
    if rr:
        st.rerun()  # Mengganti experimental_rerun

# --- TAB 2: FILE UPLOAD ---
with tab2:
    file = st.file_uploader("Upload File (TSV/CSV)", type=['tsv', 'csv'])
    
    if file is not None:
        try:
            # Otomatis deteksi separator (tab atau koma)
            if file.name.endswith('.tsv'):
                data_files = pd.read_csv(file, sep='\t')
            else:
                data_files = pd.read_csv(file)
                
            st.dataframe(data_files.head())
            
            columns = data_files.columns.tolist()
            option = st.selectbox(
                'Select the column containing text to analyze',
                columns
            )
            
            prf = st.button('Process File')
            
            if prf:
                with st.spinner('Calculating Sentiment Scores...'):
                    # Pastikan data dikonversi ke string
                    data_files['scores'] = data_files[option].astype(str).apply(
                        lambda content: sid.polarity_scores(content)
                    )
                
                with st.spinner('Assigning Labels...'):
                    data_files['compound'] = data_files["scores"].apply(
                        lambda score_dict: score_dict['compound']
                    )
                    data_files['label'] = data_files['compound'].apply(
                        lambda c: 'Positive' if c >= 0.05 else 'Negative' if c <= -0.05 else 'Neutral'
                    )
                
                st.write("Analysis Result:")
                st.dataframe(data_files)
                
                # Download Button
                file_csv = convert_df(data_files)
                st.download_button(
                    label="Download Result as CSV",
                    data=file_csv,
                    file_name="vader_result.csv",
                    mime='text/csv',
                )
        except Exception as e:
            st.error(f"Error processing file: {e}")
            
    else:
        st.info('Upload a TSV or CSV file to start batch analysis.')
        st.write('You can convert your file into tsv/csv online if needed.')
