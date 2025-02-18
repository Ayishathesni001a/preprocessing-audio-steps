import os
import librosa
import soundfile as sf

# Configuration: Update these paths as needed.
INPUT_WAV_DIR = "speech_recognition/preprocessing/output_noise_reduced"
OUTPUT_NORM_DIR = "speech_recognition/preprocessing/output_normalized"

# Create the output directory if it doesn't exist.
if not os.path.exists(OUTPUT_NORM_DIR):
    os.makedirs(OUTPUT_NORM_DIR)

print("Starting amplitude normalization...")

for root, dirs, files in os.walk(INPUT_WAV_DIR):
    for file in files:
        if file.lower().endswith(".wav"):
            input_path = os.path.join(root, file)
            output_path = os.path.join(OUTPUT_NORM_DIR, file)
            
            # Skip processing if output file already exists
            if os.path.exists(output_path):
                print(f"File {output_path} already exists. Skipping...")
                continue

            try:
                # Read the audio file
                audio, sr = sf.read(input_path)
                
                # If the file is stereo (multi-channel), convert to mono by averaging channels
                if audio.ndim > 1:
                    audio = audio.mean(axis=1)
                
                # Apply amplitude normalization so that the maximum absolute amplitude becomes 1.0
                normalized_audio = librosa.util.normalize(audio)
                
                # Write the normalized audio to the output file
                sf.write(output_path, normalized_audio, sr)
                print(f"Amplitude normalized file saved to {output_path}")
            except Exception as e:
                print(f"Error processing {input_path}: {e}")

print("Amplitude normalization complete.")
