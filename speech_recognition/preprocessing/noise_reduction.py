import noisereduce as nr
import soundfile as sf
import os

INPUT_WAV_DIR = "speech_recognition/preprocessing/output_resampling"
OUTPUT_WAV_NR_DIR = "speech_recognition/preprocessing/output_noise_reduced"

if not os.path.exists(OUTPUT_WAV_NR_DIR):
    os.makedirs(OUTPUT_WAV_NR_DIR)

for root, dirs, files in os.walk(INPUT_WAV_DIR):
    for file in files:
        if file.lower().endswith(".wav"):
            wav_path = os.path.join(root, file)
            output_path = os.path.join(OUTPUT_WAV_NR_DIR, file)
            
            # Skip processing if output file already exists
            if os.path.exists(output_path):
                print(f"File {output_path} already exists. Skipping...")
                continue
            
            try:
                audio, sr = sf.read(wav_path)
            except Exception as e:
                print(f"Error reading {wav_path}: {e}")
                continue
            
            try:
                reduced_noise = nr.reduce_noise(y=audio, sr=sr)
            except Exception as e:
                print(f"Error during noise reduction for {wav_path}: {e}")
                continue
            
            try:
                sf.write(output_path, reduced_noise, sr)
                print(f"Noise reduced file saved to {output_path}")
            except Exception as e:
                print(f"Error writing file {output_path}: {e}")
