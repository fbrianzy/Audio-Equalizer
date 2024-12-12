import streamlit as st
import numpy as np
import librosa
import soundfile as sf
import matplotlib.pyplot as plt
import io

def equalize_audio(audio, sr, bass_gain=1.0, mid_gain=1.0, treble_gain=1.0):
    stft = np.fft.fft(audio)
    freqs = np.fft.fftfreq(len(stft), 1 / sr)

    bass_band = (freqs < 300)
    mid_band = (freqs >= 300) & (freqs < 3000)
    treble_band = (freqs >= 3000) & (freqs <= 12000)

    stft[bass_band] *= bass_gain
    stft[mid_band] *= mid_gain
    stft[treble_band] *= treble_gain

    equalized_audio = np.fft.ifft(stft).real
    return equalized_audio

st.title("Audio Equalizer")
st.write("Project by Tim 2 Digital Signal Processing 2023C - Bachelor of Data Science - State University of Surabaya")

uploaded_file = st.file_uploader("Upload an audio file (WAV format)", type=["wav"])
if uploaded_file:
    # Load the uploaded audio file
    audio_data, sr = librosa.load(uploaded_file, sr=None)
    st.audio(uploaded_file, format="audio/wav")
    
    # Equalizer settings
    st.write("Adjust equalizer settings:")
    bass_gain = st.slider("Bass Gain", 0.0, 5.0, 1.0, 0.1)
    mid_gain = st.slider("Mid Gain", 0.0, 5.0, 1.0, 0.1)
    treble_gain = st.slider("Treble Gain", 0.0, 5.0, 1.0, 0.1)

    # Apply equalizer
    equalized_audio = equalize_audio(audio_data, sr, bass_gain, mid_gain, treble_gain)

    # Save equalized audio to a temporary file in memory
    output_buffer = io.BytesIO()
    sf.write(output_buffer, equalized_audio, sr, format='WAV')
    output_buffer.seek(0)

    # Provide audio player for equalized audio
    st.audio(output_buffer, format="audio/wav")

    # Display download button
    st.download_button(
        label="Download Equalized Audio",
        data=output_buffer,
        file_name="equalized_audio.wav",
        mime="audio/wav"
    )

    
    # Display waveforms
    plt.figure(figsize=(6, 4))
    plt.subplot(2, 1, 1)  # Baris 1 dari 2
    plt.title("Musik orisinil")
    plt.plot(audio_data, color="blue")
    plt.xlim(0, len(audio_data))
    plt.xlabel("Sample")
    plt.ylabel("Amplitude")

    # Menampilkan grafik dengan Streamlit
    st.write("Visualisasi Audio: Orisinil")
    st.pyplot(plt)

    plt.figure(figsize=(6,4))
    plt.subplot(2, 1, 2)  # Baris 2 dari 2
    plt.title("Musik Hasil EQ")
    plt.plot(equalized_audio, color="orange")
    plt.xlim(0, len(equalized_audio))
    plt.xlabel("Sample")
    plt.ylabel("Amplitude")

    # Menampilkan grafik dengan Streamlit
    st.write("Visualisasi Audio: Hasil EQ")
    st.pyplot(plt)
