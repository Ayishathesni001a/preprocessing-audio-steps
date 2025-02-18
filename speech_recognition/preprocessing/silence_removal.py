import os
import numpy as np
import librosa
import soundfile as sf

# Configuration: Update these paths as needed.
INPUT_NORM_DIR = "speech_recognition/preprocessing/output_segmented"
OUTPUT_VAD_DIR = "speech_recognition/preprocessing/output_silence_removal"

# Create the output directory if it doesn't exist.
if not os.path.exists(OUTPUT_VAD_DIR):
    os.makedirs(OUTPUT_VAD_DIR)

print("Starting silence removal / VAD...")

# Silence threshold (adjust as needed)
TOP_DB = 30  

for root, dirs, files in os.walk(INPUT_NORM_DIR):
    for file in files:
        if file.lower().endswith(".wav"):
            input_path = os.path.join(root, file)
            print(f"Processing file: {input_path}")
            try:
                # Load the audio file
                y, sr = librosa.load(input_path, sr=None)
                
                # Detect non-silent intervals
                intervals = librosa.effects.split(y, top_db=TOP_DB)
                print(f"Detected {len(intervals)} non-silent intervals.")

                # If silent, skip or create an empty file
                if len(intervals) == 0:
                    print(f"Skipping {file} (completely silent)")
                    continue  

                # Concatenate non-silent audio
                non_silent_audio = np.concatenate([y[start:end] for start, end in intervals])

                # Preserve folder structure in OUTPUT_VAD_DIR
                relative_path = os.path.relpath(root, INPUT_NORM_DIR)
                output_dir = os.path.join(OUTPUT_VAD_DIR, relative_path)
                os.makedirs(output_dir, exist_ok=True)

                # Save the processed audio
                output_path = os.path.join(output_dir, file)
                sf.write(output_path, non_silent_audio, sr)
                print(f"Silence removed file saved to: {output_path}\n")

            except Exception as e:
                print(f"Error processing {input_path}: {e}")

print("Silence removal completed.")
