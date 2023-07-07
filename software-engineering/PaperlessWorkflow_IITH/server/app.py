from flask import Flask
from flask_cors import CORS
import threading
from Model.util import *
app = Flask(__name__)
CORS(app)

@app.route("/contri") 
def index():
    return {
        "project": "SOAP",
        "contributer": ["aman", "ojas", "shreya", "pranav"]
        }

if __name__ == "__main__":
    threading.Thread(target = email_function,args=()).start()
    app.run(debug=True)