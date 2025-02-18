import os
import librosa
import soundfile as sf

# Input directory containing raw MP3 files
input_dir = "speech_recognition/data/clips"
# Output directory for WAV files
output_dir = "speech_recognition/preprocessing/output_conversion"

# Create the output directory if it doesn't exist

# Iterate through all MP3 files in the directory
for file in os.listdir(input_dir):
    if file.endswith(".mp3"):
        mp3_path = os.path.join(input_dir, file)
        wav_filename = file.replace(".mp3", ".wav")
        wav_path = os.path.join(output_dir, wav_filename)

        print(f"🔄 Converting {file} to WAV...")

        try:
            # Load MP3 and resample to 16kHz
            audio, sr = librosa.load(mp3_path, sr=16000)
            # Save as WAV
            sf.write(wav_path, audio, sr)
            print(f"✅ Saved {wav_path}")

        except Exception as e:
            print(f"❌ Error converting {file}: {e}")

print("🎯 MP3 to WAV conversion complete!")
