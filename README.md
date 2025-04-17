# 🎙️ Audio Preprocessing Steps

A modular and customizable pipeline for preprocessing raw audio data to make it suitable for machine learning applications such as speech recognition, audio classification, and voice activity detection.

---

## ✅ Pipeline Steps

- [x] **1. Audio Conversion** (`conversion.py`)  
  Converts audio to `.wav` format.

- [x] **2. Resampling** (`resampling.py`)  
  Resamples audio to a standard frequency (e.g., 16kHz).

- [x] **3. Normalization** (`normalisation.py`)  
  Adjusts the loudness to a standard amplitude.

- [x] **4. Noise Reduction** (`noise_reduction.py`)  
  Reduces unwanted background noise.

- [x] **5. Silence Removal** (`silence_removal.py`)  
  Removes long silent segments.

- [x] **6. Audio Splitting** (`splting.py`)  
  Splits long files into smaller chunks.

- [x] **7. Audio Segmentation** (`segment.py`)  
  Segments speech for sentence/phrase-level processing.

- [x] **8. Data Augmentation** (`augmented.py`)  
  Applies transformations like speed, pitch shift, etc.

- [x] **9. Feature Extraction** (`feature_extraction_normali.py`)  
  Extracts MFCCs, spectrograms, etc., for model input.

- [x] **10. Transcript Cleaning** (`clean_dictionary.py`)  
  Cleans and prepares the transcript/dictionary data.

---



---

## 🚀 Getting Started

### Installation
Clone this repo:
```bash
git clone https://github.com/Ayishathesni001a/preprocessing-audio-steps.git
cd preprocessing-audio-steps
