from flask import Flask, render_template, jsonify, request
from threading import Thread
import os
from play import start_recording, stop_listening
from analyze import analyze_replay

app = Flask(__name__)

recording_thread = None
last_replay_file = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start', methods=['POST'])
def start():
    global recording_thread, last_replay_file
    if not recording_thread:
        recording_thread = Thread(target=start_recording)
        recording_thread.start()
        last_replay_file = None  # Reset the last replay file
    return jsonify(status="started")

@app.route('/stop', methods=['POST'])
def stop():
    global recording_thread, last_replay_file
    if recording_thread:
        stop_listening()
        recording_thread.join()
        recording_thread = None
        last_replay_file = get_last_replay_file()
    return jsonify(status="stopped")

@app.route('/analyze', methods=['GET'])
def analyze():
    global last_replay_file
    if last_replay_file:
        results = analyze_replay(last_replay_file)
        return jsonify(results)
    else:
        return jsonify({'error': 'No replay file found'}), 400

def get_last_replay_file():
    replays_folder = 'data/replays'  # Assuming REPLAYS_FOLDER is 'replays'
    replay_files = [os.path.join(replays_folder, f) for f in os.listdir(replays_folder) if f.endswith('.csv')]
    if replay_files:
        return max(replay_files, key=os.path.getctime)
    else:
        return None

if __name__ == '__main__':
    app.run(debug=True)
