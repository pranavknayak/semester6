from flask import Flask, request
from flask_cors import CORS
from Controller.command import Accept

app = Flask(__name__)
CORS(app)

@app.route('/form/<string:action>', methods=['POST'])
def handleSubmit(action): # No guarantee that this works, the user_submit function isn't working yet
    if action == "submit":
        post_data = request.get_json()
        formData = post_data['formData']
        user = post_data['user']
        user_id = user.email
        accepter = Accept(_user_id = user_id, _field_vals = formData)
        accepter.user_submit(form_name='default')

    if action == 'approve':
        pass

    return("")


if __name__ == "__main__":
    app.run(debug=True)

