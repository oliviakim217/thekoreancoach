from flask import Flask, render_template, redirect, url_for, flash, request, send_from_directory
import sounddevice as sd
import soundfile as sf
import os

application = Flask(__name__)
application.config['SECRET_KEY'] = os.urandom(12).hex()


# def play_original(file_num):
#     filename = f'audio/audio{file_num}.wav'
#     # Extracts the raw audio data & the sampling rate of the file as stored in its RIFF header
#     data, fs = sf.read(filename, dtype='float32')
#     sd.play(data, fs)
#     sd.wait()


def sound_effect():
    filename = 'static/assets/audio/sound_effect.wav'
    data, fs = sf.read(filename, dtype='float32')
    sd.play(data, fs)
    sd.wait()


def record():
    sr = 44100
    duration = 5
    my_recording = sd.rec(int(duration * sr), samplerate=sr, channels=2)
    sd.wait()
    sf.write("static/assets/audio/user_record.wav", my_recording, sr)
    print("Done recording")


def play_recording():
    filename = 'static/assets/audio/user_record.wav'
    # Extracts the raw audio data, as well as the sampling rate of the file as stored in its RIFF header,
    data, fs = sf.read(filename, dtype='float32')
    sd.play(data, fs)
    sd.wait()


practice_list = ["안녕하세요 Hi", "안녕히 가세요 Bye", "감사합니다 Thanks", "죄송합니다 Sorry", "영어 하세요? Do you speak English?"]


@application.route("/")
def home():
    return render_template("index.html", list=practice_list)


@application.route("/practice")
def practice():
    index_num = int(request.args.get("num"))
    return render_template("practice.html", list=practice_list, num=index_num)


@application.route("/play")
def play():
    index_num = request.args.get("num")
    print(index_num)
    play_original(index_num)
    sound_effect()
    record()
    flash("Well done! Now click Compare.")
    return redirect(url_for("practice", num=index_num))


@application.route('/audio/<path:filename>')
def download_file(filename):
    return send_from_directory('static/assets/audio/', filename)


@application.route("/compare")
def compare():
    index_num = request.args.get("num")
    print(index_num)
    play_recording()
    play_original(index_num)
    return redirect(url_for("practice", num=index_num))


if __name__ == "__main__":
    application.debug = True
    application.run(host="0.0.0.0", port=8080)


