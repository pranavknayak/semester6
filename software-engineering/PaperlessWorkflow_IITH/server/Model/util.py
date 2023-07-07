import time
import smtplib
from datetime import datetime
from Model.database_manager import DbManager
from Model.user import User


def email_function():
    """meant to run in a separate thread and send emails every morniing
    """
    print('email. function running ...')
    set_time = datetime.now()
    set_time =datetime(set_time.year, set_time.month, set_time.day, hour=8)
    while(True):
        time.sleep(60)
        if(datetime.now()> set_time):
            print("runnning daily update for today")
            with DbManager().get_client() as c:
                users = c['PaperlessWorkflow']['Users']
                search_query ={'notification_freq' : "DAILY"}
                if set_time.weekday() ==0: #if day in monday
                    search_query = {'notification_freq' :{ '$in' : ["DAILY", "WEEKLY"] }} 
                users_to_notify = users.find(search_query, {'pending_approvals'})
                for cur_user in users_to_notify:
                    u = User(cur_user['_id'])
                    num_of_pending  = len(u.pending_forms)
                    if num_of_pending>0:
                        print('sending notification to ', u.ID)
                        u.send_notification(f'You have {num_of_pending} pending form.')
            set_time =datetime(set_time.year, set_time.month, set_time.day+1, hour=8)
            
def show_form(d, indent =0 ):
    if(isinstance(d,list)):
        for x in d:
            print('')
            print("    "*indent + f">{x}:", end=' ')
            if isinstance(x, dict):
                print('')
                show_form(x, indent=indent+1)
            elif isinstance(x, list):
                print('')
                print("    "*indent+ '[')
                for i ,ele in enumerate(x):
                    print('    '*indent,'>', f"ele {i} {type(ele)}")
                    show_form(ele, indent=indent+1)
                print("    "*indent+ ']')
    elif(isinstance(d,dict)):
        for x in d:
            print("    "*indent + f">{x} {type(d[x])}:", end=' ')
            if isinstance(d[x], dict):
                print('')
                show_form(d[x], indent=indent+1)
            elif isinstance(d[x], list):
                print('')
                print("    "*indent+ '[')
                for i ,ele in enumerate(d[x]):
                    print('    '*indent,'>', f"ele {i} {type(ele)}")
                    show_form(ele, indent=indent+1)
                print("    "*indent+ ']')
            else: print(d[x])
    else:
        print('    '*indent, '>',d)
