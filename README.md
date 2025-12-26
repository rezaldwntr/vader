# 📊 VADER Sentiment Analysis Dashboard

Aplikasi web interaktif berbasis **Streamlit** untuk mendemonstrasikan analisis sentimen menggunakan algoritma **VADER** (Valence Aware Dictionary and sEntiment Reasoner).

Project ini dirancang untuk memvisualisasikan bagaimana VADER mendeteksi polaritas sentimen (Positif, Negatif, Netral) dalam teks, serta menampilkan hasil analisis argumentasi dari dataset yang diuji.

![Python](https://img.shields.io/badge/Python-3.x-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red)
![NLP](https://img.shields.io/badge/NLP-VADER-green)

## ✨ Fitur Aplikasi

Aplikasi ini memiliki beberapa modul halaman:

* **🏠 Introduction:** Pengantar teori tentang metode VADER dan Lexicon-based approach.
* **📈 Argumentation Result:** Visualisasi hasil analisis sentimen pada dataset argumentasi (Tabel & Grafik).
* **🎮 Live Demo:** Coba langsung kemampuan VADER dengan memasukkan kalimat Anda sendiri secara *real-time*.
* **👤 About Me:** Profil pengembang.

## 🛠️ Teknologi

* **Framework:** [Streamlit](https://streamlit.io/)
* **NLP Library:** `vaderSentiment`
* **Data Processing:** Pandas
* **Visualization:** Altair / Built-in Streamlit Charts

## 🚀 Cara Menjalankan (Local)

Ikuti langkah ini untuk menjalankan dashboard di komputer Anda:

1.  **Clone Repository**
    ~~~bash
    git clone https://github.com/rezaldwntr/vader.git
    cd vader
    ~~~

2.  **Install Dependencies**
    ~~~bash
    pip install -r requirements.txt
    ~~~

3.  **Jalankan Streamlit**
    ~~~bash
    streamlit run VADER_Introduction.py
    ~~~
    Aplikasi akan otomatis terbuka di browser Anda (biasanya di `http://localhost:8501`).

## 📂 Struktur Folder

~~~text
vader/
├── data/                  # Dataset (TSV) dan resource teks
├── img/                   # Aset gambar untuk UI
├── pages/                 # Halaman-halaman dashboard (Multipage App)
│   ├── 1_VADER_Argumentation_Result.py
│   ├── 2_VADER_Demo.py
│   └── 3_About_Me.py
├── vaderSentiment/        # Modul/Library core VADER
├── VADER_Introduction.py  # Halaman Utama (Main Entry)
└── requirements.txt       # Daftar dependensi
~~~

---
© 2022 Rezal Dewantara.
