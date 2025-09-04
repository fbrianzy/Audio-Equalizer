# 🎛️ Audio-Equalizer (Python + Librosa)

An educational audio equalizer built with Python. It demonstrates basic digital signal processing (DSP) concepts such as filtering, gain per band, and visualization (waveform / spectrogram).

> Course context: Digital Signal Processing — Bachelor of Data Science, State University of Surabaya.

---

## ✨ Features
- Apply multi-band EQ to WAV/MP3 inputs (e.g., bass/low-mid/high-shelf).
- Visualize waveform and spectrogram before/after processing.
- Ready for scripting or extension into a simple GUI/CLI.

---

## 🚀 Quickstart

### 1) Environment
```bash
# Python 3.10+ is recommended
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
```

### 2) Run
```bash
# Minimal run (edit paths as needed)
python Audio-Equalizer.py
```

## 📁 Project Structure
```bash
Audio-Equalizer/
├─ Audio-Equalizer.py       # main script
├─ requirements.txt         # dependencies
├─ README.md
└─ LICENSE                  # MIT
```

## 🧪 Try It with Sample Audio
- Use any short WAV (16-bit PCM, 44.1 kHz) or grab a free sample from:
  - https://freesound.org (royalty-free community samples)
- Place it in `examples/` and adjust the script path.

---

## 🧠 How It Works (High-Level)
1. **Load audio** (mono or stereo) using Librosa/SoundFile.
2. **Filter per band** (e.g., low, mid, high) with gains you set.
3. **Mix** processed bands back together.
4. **Export** the equalized audio and **plot** before/after visuals.

> For study: peek into filter design (IIR/FIR), Q factor (bandwidth), and stability considerations.

---

## 📸 Visualization
- Waveform before vs after
- Spectrogram (STFT) to see frequency-domain changes

*(Add images/gifs here once you save plots from the script, e.g., `plots/before_after.png`.)*

---

## 🧩 Dependencies
See `requirements.txt`. Typical stack:
- `librosa`
- `numpy`
- `scipy`
- `soundfile`
- `matplotlib`

> Pin versions in `requirements.txt` to improve reproducibility.

---

## 🛣️ Roadmap
- [ ] Add CLI via `argparse` (`--in`, `--out`, `--bands`, `--sr`, `--plot`)
- [ ] Presets: `bass_boost`, `vocal_clarity`, `podcast_warmth`
- [ ] Save plots automatically to `plots/`
- [ ] Include `examples/input.wav` (short, royalty-free clip)
- [ ] Unit tests for simple tone (e.g., 1 kHz sine) to verify gain

---

## 🤝 Contributing
PRs are welcome! For larger changes, please open an issue first to discuss what you’d like to add or modify.

---

## 📜 License
MIT — see [LICENSE](./LICENSE).

---

## 🙌 Credits
- Built with Python & Librosa for DSP learning and demonstration.

