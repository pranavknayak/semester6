import pytest
from Model.form import Form
from Model.formMetaData import FormMetaData
from Model.level import Level
from Model.data import Data

def test_default_init_with_no_ID():
    f = Form()
    assert f.ID==None

def test_default_init_with_ID():
    id = '643ff5dd326f4d6638bea447'
    f = Form(ID= id)
    assert f.ID==id

def test_member_values_for_empty_form():
    f = Form()
    assert f.ID == None
    assert f.ID == None
    assert f.form_meta.to_dict() == FormMetaData(input_dict = None).to_dict()
    assert f.cur_level_no == None
    assert f.cur_level.to_dict() == Level(inp_dict = None).to_dict()
    assert f.data.to_dict() == Data(inp_dict = None).to_dict()
    assert f.applicant_id == None
    assert f.status == None
    assert f.version == 0
    
def test_save_to_db_with_no_ID():
    f = Form()
    f.save_to_db()
    id = f.ID

    f2 = Form(ID =id)

    assert f.to_dict() == f2.to_dict()

def test_save_to_db_with_ID():
    id = '643ff5dd326f4d6638bea447'
    f = Form(ID= id)
    f.cur_level_no = -1
    f.save_to_db()
    f2 = Form(ID = id)

    assert f.to_dict() == f2.to_dict()
