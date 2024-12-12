import streamlit as st # Library UI
import numpy as np # Library Perhitungan
import librosa # Library yang mendukung file audio (wav)
import soundfile as sf # Library audio
import matplotlib.pyplot as plt # Library visualisasi
import io # Library file-buffer memory
import pandas as pd # Library untuk dataframe

# Function Equalizer Audio
def equalize_audio(audio, sr, bass_gain=1.0, mid_gain=1.0, treble_gain=1.0):

    # Fungsi untuk merubah audio menjadi frekuensi
    stft = np.fft.fft(audio) # Menggunakan FFT, yaitu merubah domain waktu menjadi domain frekuensi
    freqs = np.fft.fftfreq(len(stft), 1 / sr) # Menggunakan fungsi np.fft.fftfreq, menghasilkan array freqs yang merepresentasikan nilai frekuensi untuk setiap elemen di stft.

    # Inisialisasi Rentang Equalizer
    bass_band = (freqs < 300) # Rentang bass dari 0-300 Hz
    mid_band = (freqs >= 300) & (freqs < 3000) # Rentang middle dari 300-3000 Hz
    treble_band = (freqs >= 3000) & (freqs <= 25000) # Rentang treble dari 3000-25000 Hz

    # Fungsi untuk memanipulasi frekuensi, frekuensi akan diperkuat berdasarkan settingan user
    stft[bass_band] *= bass_gain # Fungsi untuk memperkuat bass
    stft[mid_band] *= mid_gain # Fungsi untuk memperkuat middle
    stft[treble_band] *= treble_gain # Fungsi untuk memperkuat treble

    # Menyimpan hasil equalizer audio
    equalized_audio = np.fft.ifft(stft).real
    return equalized_audio # Mengembalikan audio hasil equalizer

# Fungsi untuk menghitung nilai magnitude
def compute_frequency_spectrum(audio, sr):

    # Fungsi untuk merubah audio menjadi frekuensi
    stft = np.fft.fft(audio)
    freqs = np.fft.fftfreq(len(stft), 1 / sr)
    magnitude = np.abs(stft) # Menghitung magnitudo dari dari domain frekuensi
    return freqs, magnitude # Mengembalikan nilai frekuensi dan magnitudo

# Fungsi untuk menghitung nilai rata-rata dari rentang frekuensi yang ada
def compute_band_means(freqs, magnitudes):
    
    # Inisialisasi Rentang Equalizer
    bass_band = (freqs >= 0) & (freqs < 300) # Rentang bass dari 0-300 Hz
    mid_band = (freqs >= 300) & (freqs < 3000) # Rentang middle dari 300-3000 Hz
    treble_band = (freqs >= 3000) & (freqs <= 25000) # Rentang treble dari 3000-25000 Hz

    # Menghitung nilai rata-rata dari setiap rentang frekuensi
    bass_mean = np.mean(magnitudes[bass_band]) # Menghitung nilai rata-rata dari bass
    mid_mean = np.mean(magnitudes[mid_band]) # Menghitung nilai rata-rata dari midle
    treble_mean = np.mean(magnitudes[treble_band]) # Menghitung nilai rata-rata dari treble

    return bass_mean, mid_mean, treble_mean # Mengembalikan nilai rata-rata dari setiap rentang frekuensi

st.title("Audio Equalizer")
st.write("Project by Tim 2 Digital Signal Processing 2023C - Bachelor of Data Science - State University of Surabaya")

# Fungsi untuk user bisa mengupload file audio
uploaded_file = st.file_uploader("Upload an audio file (WAV format)", type=["wav"])

# Program Berjalan jika ada file yang diupload
if uploaded_file:
    
    # Load Audio
    audio_data, sr = librosa.load(uploaded_file, sr=None)

    # Menampilkan widget untuk memutar audio hasil upload user
    st.audio(uploaded_file, format="audio/wav")
    
    # Equalizer settings
    st.write("Adjust equalizer settings:")

    # Slider dimulai dari 0.0 dari 5.0, nilai default yang ditampilkan 1.0, dan nilai per step 0.1
    bass_gain = st.slider("Bass Gain", 0.0, 5.0, 1.0, 0.1)
    mid_gain = st.slider("Mid Gain", 0.0, 5.0, 1.0, 0.1)
    treble_gain = st.slider("Treble Gain", 0.0, 5.0, 1.0, 0.1)

    # Mengaplikasikan fungsi equalizer ke audio inputan user
    equalized_audio = equalize_audio(audio_data, sr, bass_gain, mid_gain, treble_gain)

    # Menyimpan equalized audio ke file sementara di memori
    output_buffer = io.BytesIO()
    sf.write(output_buffer, equalized_audio, sr, format='WAV')
    output_buffer.seek(0)

    # Menampilkan widget untuk memutar audio hasil equalizer
    st.audio(output_buffer, format="audio/wav")

    # Menampilkan tombol download
    st.download_button(
        label="Download Equalized Audio",
        data=output_buffer,
        file_name="equalized_audio.wav",
        mime="audio/wav"
    )

    # Fungsi untuk menghitung frekuensi spektrum audio
    freqs_orig, mag_orig = compute_frequency_spectrum(audio_data, sr)
    freqs_eq, mag_eq = compute_frequency_spectrum(equalized_audio, sr)

    # Fungsi untuk menghitung nilai rata-rata frekuensi audio
    bass_orig, mid_orig, treble_orig = compute_band_means(freqs_orig, mag_orig)
    bass_eq, mid_eq, treble_eq = compute_band_means(freqs_eq, mag_eq)

    # Fungsi untuk menampilkan tabel numerik dari nilai frekuensi audio
    st.write("Numeric Frequency Result (Mean per Band):")
    combined_df = pd.DataFrame({
        "Band": ["Bass", "Mid", "Treble"],
        "Magnitude (Original)": [bass_orig, mid_orig, treble_orig],
        "Magnitude (Equalized)": [bass_eq, mid_eq, treble_eq]
    })

    # Menampilkan tabel dengan streamlit
    st.dataframe(combined_df, hide_index=True)

    # Fungsi untuk menampikan visualiasi nilai frekuensi keduanya
    plt.figure(figsize=(10, 12))
    plt.subplot(3, 1, 1)
    plt.title("Musik Original vs Equalized")
    plt.plot(audio_data, color="blue", label='Original')
    plt.plot(equalized_audio, color="orange", alpha=0.45, label="Equalized")
    plt.xlim(0, len(audio_data))
    plt.xlabel("Sample")
    plt.ylabel("Amplitude")
    plt.legend(fontsize=10, loc='upper right')

    # Menampilkan grafik dengan Streamlit
    st.write("Audio Visualization: Original vs EQ Result")
    st.pyplot(plt)
