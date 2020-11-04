from flask import Flask

app = Flask(__name__)

app.secret_key = 'ik1Al4dTI3-DccI-XVQmjg'

import modules.routes