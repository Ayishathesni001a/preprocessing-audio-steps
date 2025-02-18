import os
import librosa
import soundfile as sf

# Input directory containing WAV files (already converted from MP3)
input_dir = "speech_recognition/preprocessing/output_conversion"
# Output directory for resampled WAV files
output_dir = "speech_recognition/preprocessing/output_resampling"

# Create the output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Target sample rate
TARGET_SR = 16000

# Iterate through all WAV files in the directory
for file in os.listdir(input_dir):
    if file.endswith(".wav"):
        wav_path = os.path.join(input_dir, file)
        resampled_wav_path = os.path.join(output_dir, file)

        print(f"🔄 Resampling {file} to {TARGET_SR} Hz...")

        try:
            # Load WAV file
            audio, sr = librosa.load(wav_path, sr=None)

            # Only resample if the sample rate is different
            if sr != TARGET_SR:
                audio = librosa.resample(audio, orig_sr=sr, target_sr=TARGET_SR)

            # Save the resampled audio
            sf.write(resampled_wav_path, audio, TARGET_SR)
            print(f"✅ Saved {resampled_wav_path}")

        except Exception as e:
            print(f"❌ Error resampling {file}: {e}")

print("🎯 Resampling complete!")
