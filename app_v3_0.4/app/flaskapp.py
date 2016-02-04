from flask import Flask
app = Flask(__name__)
import views
app.run(debug = True)
