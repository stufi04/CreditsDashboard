from flask import Flask
from flask_cors import CORS

from api.credits.credits_service import CreditsService

app = Flask(__name__)
CORS(app)

creditsService = CreditsService()

@app.route("/usage")
def get_usage():
    return creditsService.get_usage()

if __name__ == "__main__":
    app.run(host="::", port=5000)
