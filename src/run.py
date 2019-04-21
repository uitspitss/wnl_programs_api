from flask import Flask, request, jsonify

from main import programs_api

app = Flask(__name__)


@app.route('/')
def _entrypoint():
    return programs_api(request)


if __name__ == '__main__':
    app.run(debug=True)
