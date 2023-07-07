import pytest
from Model.fields import *


def test_Textbox():
    f = Textbox("temp", 'temp')
    assert f.to_dict()['field_type']=='Textbox'

def test_Date():
    f = Date("temp", 'temp')
    assert f.to_dict()['field_type'] =='Date'

def test_Checkbox():
    f = Checkbox("temp", 'temp')
    assert f.to_dict()['field_type']=='Checkbox'

def test_Dropdown():
    f = Dropdown("temp", ["temp"],'temp')
    assert f.to_dict()['field_type'] == 'Dropdown'

def test_File():
    f = File("temp", 'temp')
    assert f.to_dict()['field_type'] == 'File'

def test_factory_textbox():
    f = FieldFactory('Textbox', ["temp", "temp"])
    assert f.to_dict()['field_type']=='Textbox'


def test_factory_date():
    f = FieldFactory('Date', ["temp", "temp"])
    assert f.to_dict()['field_type']=='Date'

def test_factory_Checkbox():
    f = FieldFactory('Checkbox', ["temp", "temp"])
    assert f.to_dict()['field_type']=='Checkbox'

def test_factory_dropdown():
    f = FieldFactory('Dropdown', ["temp", [],"temp"])
    assert f.to_dict()['field_type']=='Dropdown'

def test_factory_file():
    f = FieldFactory('File', ["temp", "temp"])
    assert f.to_dict()['field_type']=='File'


