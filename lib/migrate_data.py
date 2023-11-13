from config.config import *
import os
from lib.stream_processing import process_wav_file
from lib.print_status import create_progress_bar, clear_previous_lines, get_current_status, reset_previous_lines
from .typing import DetectionState
import time

def check_migration():
    version_detected = CURRENT_VERSION
    recording_dirs = os.listdir(RECORDINGS_FOLDER)
    for file in recording_dirs:
        if os.path.isdir(os.path.join(RECORDINGS_FOLDER, file)):
            segments_folder = os.path.join(RECORDINGS_FOLDER, file, "segments")
            if not os.path.exists(segments_folder):
                version_detected = 0
                break
            else:
                source_files = os.listdir(os.path.join(RECORDINGS_FOLDER, file, "source"))
                for source_file in source_files:
                    srt_file = source_file.replace(".wav", ".v" + str(CURRENT_VERSION) + ".srt")
                    if not os.path.exists(os.path.join(segments_folder, srt_file)):
                        version_detected = 0
                        break

    if version_detected < CURRENT_VERSION:
        print("----------------------------")
        print("!! Improvement to segmentation found !!")
        print("This can help improve the data gathering from your recordings which make newer models better")
        print("Resegmenting your data may take a while")
        migrate_data()

def migrate_data():
    print("----------------------------")
    recording_dirs = os.listdir(RECORDINGS_FOLDER)
    for label in recording_dirs:
        source_dir = os.path.join(RECORDINGS_FOLDER, label, "source")
        if os.path.isdir(source_dir):
            segments_dir = os.path.join(RECORDINGS_FOLDER, label, "segments")
            if not os.path.exists(segments_dir):
                os.makedirs(segments_dir)
            wav_files = [x for x in os.listdir(source_dir) if os.path.isfile(os.path.join(source_dir, x)) and x.endswith(".wav")]            
            if len(wav_files) == 0:
                continue
            print( "Resegmenting " + label + "..." )
            progress = 0
            progress_chunk = 1 / len( wav_files )
            skipped_amount = 0
            for index, wav_file in enumerate(wav_files):
                wav_file_location = os.path.join(source_dir, wav_file)
                srt_file_location = os.path.join(segments_dir, wav_file.replace(".wav", ".v" + str(CURRENT_VERSION) + ".srt"))
                output_file_location = os.path.join(segments_dir, wav_file.replace(".wav", "_detection.wav"))
                
                # Only resegment if the new version does not exist already
                if not os.path.exists(srt_file_location):
                    process_wav_file(wav_file_location, srt_file_location, output_file_location, [label], \
                        lambda internal_progress, state: print_migration_progress(progress + (internal_progress * progress_chunk), state) )
                else:
                    skipped_amount += 1
                progress = index / len( wav_files ) + progress_chunk
                
            if progress == 1 and skipped_amount < len(wav_files):
                clear_previous_lines(1)

            clear_previous_lines(1)
            print( label + " resegmented!" if skipped_amount < len(wav_files) else label + " already properly segmented!" )

    time.sleep(1)
    print("Finished migrating data!")
    print("----------------------------")

def print_migration_progress(progress, state: DetectionState):
    status_lines = get_current_status(state)
    line_count = 1 + len(status_lines) if progress > 0 or state.state == "processing" else 0
    reset_previous_lines(line_count) if progress < 1 else clear_previous_lines(line_count)
    print( create_progress_bar(progress) )
    if progress != 1:
        for line in status_lines:
            print( line )