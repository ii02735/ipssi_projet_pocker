import app
import os

os.environ["APP_ENV"] = "DEV"
os.environ["APP_DEBUG"] = "1"
app.app.run()
