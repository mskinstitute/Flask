from flask import Flask # pip install flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello From Python Flask"

if __name__ == "__main__":
    app.run(debug=True)