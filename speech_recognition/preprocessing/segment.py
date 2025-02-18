import os
import glob
import librosa
import soundfile as sf
from textgrid import TextGrid

# Directories
audio_dir = "/home/user/Desktop/voice-to-text/speech_recognition/preprocessing/output_transcript"
textgrid_dir = "/home/user/Desktop/voice-to-text/speech_recognition/preprocessing/output_alignment"
output_folder = "/home/user/Desktop/voice-to-text/speech_recognition/preprocessing/output_segmented"
os.makedirs(output_folder, exist_ok=True)

# Set TEST_BATCH_SIZE to a small number for testing (e.g., 10).
# Set to None or 0 to process all files.
TEST_BATCH_SIZE = None

# Get list of all WAV files in the audio directory
audio_files = glob.glob(os.path.join(audio_dir, "*.wav"))
if TEST_BATCH_SIZE and TEST_BATCH_SIZE > 0:
    audio_files = audio_files[:TEST_BATCH_SIZE]

print(f"Found {len(audio_files)} audio files to process.")

# Loop over each audio file
for audio_file in audio_files:
    base_name = os.path.splitext(os.path.basename(audio_file))[0]
    textgrid_file = os.path.join(textgrid_dir, base_name + ".TextGrid")
    
    if not os.path.exists(textgrid_file):
        print(f"TextGrid for {base_name} not found. Skipping.")
        continue

    try:
        audio, sr = librosa.load(audio_file, sr=None)
    except Exception as e:
        print(f"Error loading {audio_file}: {e}")
        continue

    try:
        tg = TextGrid.fromFile(textgrid_file)
    except Exception as e:
        print(f"Error reading TextGrid {textgrid_file}: {e}")
        continue

    # Process each tier and its intervals in the TextGrid
    for tier in tg.tiers:
        for i, interval in enumerate(tier.intervals):
            label = interval.mark.strip()
            # Skip intervals with empty labels (or assign a default label if desired)
            if not label:
                continue

            start_time = interval.minTime
            end_time = interval.maxTime
            start_sample = int(start_time * sr)
            end_sample = int(end_time * sr)
            segment_audio = audio[start_sample:end_sample]

            segment_filename = f"{base_name}_segment_{i}_{label.replace(' ', '_')}.wav"
            segment_path = os.path.join(output_folder, segment_filename)

            try:
                sf.write(segment_path, segment_audio, sr)
                print(f"Saved segment: {segment_filename}")
            except Exception as e:
                print(f"Error saving {segment_filename}: {e}")

print("Segmentation complete for all audio files.")
