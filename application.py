from flask import Flask, render_template, redirect, url_for, flash, request, send_from_directory
import os

application = Flask(__name__)
application.config['SECRET_KEY'] = os.urandom(12).hex()


practice_list = ["안녕하세요 Hi", "안녕히 가세요 Bye", "감사합니다 Thanks", "죄송합니다 Sorry", "영어 하세요? Do you speak English?"]


@application.route("/")
def home():
    return render_template("index.html", list=practice_list)


@application.route("/practice")
def practice():
    index_num = int(request.args.get("num"))
    return render_template("practice.html", list=practice_list, num=index_num)


# @application.route("/play")
# def play():
#     index_num = request.args.get("num")
#     print(index_num)
#     # play_original(index_num)
#     # sound_effect()
#     # record()
#     flash("Well done! Now click Compare.")
#     return redirect(url_for("practice", num=index_num))


@application.route('/audio/<path:filename>')
def download_file(filename):
    return send_from_directory('static/assets/audio/', filename)


# @application.route("/compare")
# def compare():
#     index_num = request.args.get("num")
#     print(index_num)
#     # play_recording()
#     # play_original(index_num)
#     return redirect(url_for("practice", num=index_num))


if __name__ == "__main__":
    application.run(port=8080)


