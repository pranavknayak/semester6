from flask import Flask, request, jsonify
from flask_cors import CORS
from Model.user import User
from Model.formMetaData import FormMetaData
from Controller.command import *
from Model.database_manager import DbManager
from bson.objectid import ObjectId
from Model.email_manager import EmailManager


app = Flask(__name__)
CORS(app)

def get_form_names(form_ids:list):
    ret = []
    with DbManager().get_client() as c:
        forms = c['PaperlessWorkflow']['Forms']
        for id in form_ids:
            data_dict = forms.find_one({"_id": ObjectId(id)})
            print(data_dict['form_meta'])
            ret.append(data_dict['form_meta']['display_name'])
    return ret


@app.route('/login/fetch_data', methods=['GET'])
def fetch_data():
    email = str(request.args.get('email'))
    logged_in_user = User(email=email)
    pending_form_ids = logged_in_user.pending_forms
    pending_form_names = get_form_names(pending_form_ids)
    response_data = {'pending_form_ids': pending_form_ids, 'pending_form_names': pending_form_names}
    return jsonify(response_data)

@app.route('/demo/submit', methods=["POST"])
def demo_submit():
    data=request.json
    formdata=data["data"]
    form_type=data["form_type"]
    app_id=data["user"]["email"]
    form_meta=FormMetaData(form_type=form_type)
    fields=form_meta.get_level(0)[1]
    field_vals=[]
    for x in fields:
        field_vals.append(formdata[x[0]])

    val, id=Accept(_form_id=None,_user_id=app_id,_field_vals=field_vals).user_submit(form_name=form_type)
    
    if val == True:#sending emails
        f = Form(Id= id)
        for email in f.cur_level.approvers_id:
            u =User(email=email)
            u.send_notification("You have a new form to approve")
                
    response = {"success": val}
    return jsonify(response)

@app.route('/demo/render', methods = ['GET'])
def handle_render():
    formID = request.args.get('formID')
    f = Form(formID)
    
    formHistory = f.data.get_form_state()
    formData = {}
    for fieldMeta in formHistory:
        field = fieldMeta['field_entry']
        fieldName = field.display_name
        fieldValue = field.value
        formData[fieldName] = fieldValue
    return formData

if __name__ == "__main__":
    app.run()
