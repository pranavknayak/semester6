from flask import Flask, request, jsonify
from flask_cors import CORS

from Model.formMetaData import FormMetaData
from Controller.command import *
app = Flask(__name__)
CORS(app)

@app.route('/form/submit', methods=["POST"])
def handle_submit():
    data=request.json
    formdata=data["formdata"]
    form_type=data["form_type"]
    app_id=data["user_id"]["email"]
    form_meta=FormMetaData(form_type=form_type)
    fields=form_meta.get_level(0)[1]
    field_vals=[]
    for x in fields:
        field_vals.append(formdata[x[0]])
    val=Accept(form_id=None,user_id=app_id,field_vals=field_vals).user_submit(form_name=form_type)
    response = {"success": val}
    return jsonify(response)

@app.route('/form/approve', methods=["POST"])
def handle_approve():
    data=request.json
    formdata=data["formdata"]
    form_remarks=data["remarks"]
    F_id=data["form_id"]
    form_type=data["form_type"]
    app_id=data["user_id"]["email"]
    form_meta=FormMetaData(form_type=form_type)
    fields=form_meta.get_level(0)[1]
    field_vals=[]
    for x in fields:
        field_vals.append(formdata[x[0]])
    val=Accept(form_id=F_id,user_id=app_id,field_vals=field_vals).officer_approve(remarks=form_remarks)
    response = {"success": val}
    return jsonify(response)

@app.route('/form/reject', methods=["POST"])
def handle_reject():
    data=request.json
    form_remarks=data["remarks"]
    F_id=data["form_id"]
    app_id=data["user_id"]["email"]
    val=Reject(form_id=F_id,user_id=app_id).officer_reject(remarks=form_remarks)
    response = {"success": val}
    return jsonify(response)

@app.route('/form/review', methods=["POST"])
def handle_review():
    data=request.json
    form_remarks=data["remarks"]
    F_id=data["form_id"]
    app_id=data["user_id"]["email"]
    val=Review(form_id=F_id,user_id=app_id).officer_review(remarks=form_remarks)
    response = {"success": val}
    return jsonify(response)

@app.route('/form/render', methods=["GET"])
def handle_render():
    return ''
