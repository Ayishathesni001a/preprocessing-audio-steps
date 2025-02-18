import csv
import os
import shutil

# List of TSV files to process (train.tsv and validated.tsv)
tsv_files = [
    "speech_recognition/data/train.tsv",
    "speech_recognition/data/validated.tsv"
]

# Directory where the raw audio (WAV files) are stored
AUDIO_DIR = "speech_recognition/preprocessing/output_normalized"  # Update if needed

# Directory where the corpus for forced alignment will be created
OUTPUT_CORPUS_DIR = "speech_recognition/preprocessing/output_transcript"

# Create the output corpus directory if it doesn't exist
if not os.path.exists(OUTPUT_CORPUS_DIR):
    os.makedirs(OUTPUT_CORPUS_DIR)

print("Preparing corpus for forced alignment...")

for tsv_file in tsv_files:
    print(f"\nProcessing TSV file: {tsv_file}")
    try:
        with open(tsv_file, newline='', encoding='utf-8') as tsvfile:
            reader = csv.DictReader(tsvfile, delimiter='\t')
            for row in reader:
                # Extract the audio file name and transcript
                audio_filename = row["path"].replace(".mp3", ".wav")  # Convert MP3 to WAV if needed
                transcript = row["sentence"]

                # Construct the full path to the audio file
                audio_full_path = os.path.join(AUDIO_DIR, audio_filename)
                if not os.path.exists(audio_full_path):
                    print(f"Audio file not found: {audio_full_path}")
                    continue

                # Define the destination paths in the corpus folder
                dest_audio_path = os.path.join(OUTPUT_CORPUS_DIR, audio_filename)
                transcript_filename = os.path.splitext(audio_filename)[0] + ".lab"  # Fixed issue here
                transcript_path = os.path.join(OUTPUT_CORPUS_DIR, transcript_filename)

                # Copy the audio file if it doesn't already exist in the corpus folder
                if not os.path.exists(dest_audio_path):
                    shutil.copy(audio_full_path, dest_audio_path)
                    print(f"Copied audio: {audio_filename}")
                else:
                    print(f"Audio {audio_filename} already exists, skipping copy.")

                # Write the transcript file if it doesn't already exist
                if not os.path.exists(transcript_path):
                    with open(transcript_path, "w", encoding="utf-8") as f:
                        f.write(transcript)
                    print(f"Created transcript: {transcript_filename}")
                else:
                    print(f"Transcript {transcript_filename} already exists, skipping.")
    except Exception as e:
        print(f"Error processing {tsv_file}: {e}")

print("\nCorpus preparation complete.")
