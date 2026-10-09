from flask import Flask, render_template, jsonify, request
import threading
import time
from translator import speak, listen, translate_to_hindi

app = Flask(__name__)

# Global state
state = {
    "running": False,
    "english": "",
    "hindi": "",
    "status": "Idle"
}

worker_thread = None


def background_worker():
    """Background me mic sunta rahega"""
    global state

    state["status"] = "🔊 Greeting..."
    speak("Hello, I am an English to Hindi translator. Today how can I help you?", lang='en')

    while state["running"]:
        state["status"] = "🎤 Listening..."
        english_text = listen()

        if english_text:
            state["english"] = english_text
            state["status"] = "🔄 Translating..."
            hindi_text = translate_to_hindi(english_text)

            if hindi_text:
                state["hindi"] = hindi_text
                state["status"] = "🔊 Speaking..."
                speak(hindi_text, lang='hi')

        time.sleep(0.3)

    state["status"] = "Stopped ⏹️"


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/start', methods=['POST'])
def start():
    global worker_thread
    if not state["running"]:
        state["running"] = True
        worker_thread = threading.Thread(target=background_worker, daemon=True)
        worker_thread.start()
    return jsonify({"success": True})


@app.route('/stop', methods=['POST'])
def stop():
    state["running"] = False
    return jsonify({"success": True})


@app.route('/status')
def status():
    return jsonify({
        "running": state["running"],
        "english": state["english"],
        "hindi": state["hindi"],
        "status": state["status"]
    })


if __name__ == '__main__':
    print("🚀 Server chalu ho gaya!")
    print("🌐 Browser me kholo: http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=False)