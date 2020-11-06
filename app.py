from flask import Flask
from modules.Controller import Controller
import os

os.environ["FLASK_ENV"] = "development"

app = Flask(__name__)

controller = Controller()

app.add_url_rule('/', view_func=controller.homepage, methods=["GET"])
app.add_url_rule('/restart',view_func=controller.restart, methods=["GET"])
app.add_url_rule('/video-poker/start',view_func=controller.start_video_poker, methods=["POST"])
app.add_url_rule('/video-poker/second',view_func=controller.second_shuffle, methods=["POST"])

app.secret_key = 'ik1Al4dTI3-DccI-XVQmjg'

if __name__ == "__main__":
    app.run(debug=True)
