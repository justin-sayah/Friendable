from flask import Flask, request, render_template
import os

app = Flask(__name__)

@app.route('/')
def test():
    return render_template("index.html")

# @app.route('/information', methods=['GET'])
# def info():
#     return render_template('info.html')

