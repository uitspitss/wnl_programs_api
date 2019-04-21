from flask import Flask, request, jsonify

from main import get_programs, format_slack

app = Flask(__name__)


@app.route('/')
def _entrypoint():
    format = request.args.get('format', 'json')

    programs = get_programs()
    if format == 'slack':
        return format_slack(programs)

    return jsonify(programs)


if __name__ == '__main__':
    app.run(debug=False)
