import pytest
from Model.form import Form
from Model.formMetaData import FormMetaData
from Model.level import Level
from Model.data import Data
from Model.user import User



def test_default_init_with_ID():
    id = "test_id@test.com"
    u = User(email= id)
    assert u.ID==id

def test_save_to_db_with_ID():
    id = "test_id@test.com"
    u = User(email= id)
    u.notification_freq = "WRONG_NOTIFICATION_FREQ"
    u.save_to_db()
    u2 = User(email=id)
    assert u.to_dict() == u2.to_dict()

def test_set_notif_frequency():
    id = "test_id@test.com"
    u = User(email= id)
    u.set_notification_frequency('DAILY')
    assert u.notification_freq == 'DAILY'

def test_set_user_role():
    id = "test_id@test.com"
    u = User(email= id)
    u.set_user_role('ADMIN')
    assert u.role == 'ADMIN'