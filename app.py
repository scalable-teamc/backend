from flask import Flask

app = Flask(__name__)

if __name__ == '__main__':
    # run app in debug mode on port 8082
    app.run(debug=True, port=8082)
