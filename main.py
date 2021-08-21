from flask import Flask, render_template, redirect, url_for, flash, request
import sounddevice as sd
import soundfile as sf
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(12).hex()


def play_original():
    filename = 'audio/day1_audio.wav'
    # Extracts the raw audio data & the sampling rate of the file as stored in its RIFF header
    data, fs = sf.read(filename, dtype='float32')
    sd.play(data, fs)
    status = sd.wait()


def record():
    sr = 44100
    duration = 5
    my_recording = sd.rec(int(duration * sr), samplerate=sr, channels=2)
    sd.wait()
    sd.play(my_recording, sr)
    sf.write("audio/New Record.wav", my_recording, sr)
    print("Done recording")


def play_recording():
    filename = 'audio/New Record.wav'
    # Extracts the raw audio data, as well as the sampling rate of the file as stored in its RIFF header,
    data, fs = sf.read(filename, dtype='float32')
    sd.play(data, fs)
    status = sd.wait()  


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/<int:day>")
def page(day):
    return render_template("day.html", day=day)


@app.route("/play", methods=["GET", "POST"])
def play():
    if request.method == "POST":
        flash("Listen carefully")
        play_original()
        record()
        play_recording()
        play_original()
        return redirect(url_for("home"))

    return render_template("index.html")


@app.route("/stop", methods=["GET", "POST"])
def stop():
    sd.stop()
    return redirect(url_for("home"))



if __name__ == "__main__":
    app.run(debug=True)


