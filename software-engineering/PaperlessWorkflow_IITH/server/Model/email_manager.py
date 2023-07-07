from queue import Queue
from threading import Lock
from pymongo import MongoClient
from bson.objectid import ObjectId
from time import time, sleep
import threading
from datetime import datetime, timedelta
from Model.database_manager import DbManager
import smtplib
from email.message import EmailMessage

class SingletonMetaClass(type):
    my_instances = {}
    thread_lock: Lock = Lock()

    def __call__(cls, *args, **kwargs):
        with cls.thread_lock:
            if cls not in cls.my_instances:
                inst = super().__call__(*args, **kwargs)
                cls.my_instances[cls] = inst
        return cls.my_instances[cls]

class EmailManager(metaclass = SingletonMetaClass):
    """An thread safe singleton object pool class for MongoClient.client
    Intended use:\n
    with DbManager().get_client() as c:
        c.get_database('example)\n
        ... 
    """
    
    def __init__(self) -> None:
        self.queue = Queue()
        self.lock = Lock()
        self.emailing_thread = threading.Thread(target = self.email_function, args=())
        self.emailing_thread.start()
    def schedule_email(self, receiver_email:str, content:str):
        self.lock.acquire()
        self.queue.put((receiver_email, content))
        self.lock.release()
    def email_function(self):
        """meant to run in a separate thread and send emails every morniing"""

        now = datetime.now()
        morning_milestone = datetime(year = now.year, month=now.month, day =now.day, hour=0)

        while(True):
            sleep(60*5)  # sleep for 5 mins, recheck for emails in the queue every 5 min

            if self.queue.empty(): continue # if no emails in queue then skip 

            #save whatever is the queue and empty the queue to accept new email requests
            self.lock.acquire()
            cur_queue = self.queue
            self.queue = Queue()
            self.lock.release()


            #sending emails in queue
            try: 
                s = smtplib.SMTP('smtp.gmail.com', 587)
                s.starttls()
                s.login('ppwnotification@gmail.com', "jqsgxbagdndwkqnp")
                while not cur_queue.empty():
                    (email, content) = cur_queue.get()
                    msg = EmailMessage()
                    msg.set_content(content)
                    msg['Subject'] = "Update from Paperless Workflow App"
                    msg['From'] = "ppwnotification@gmail.com"
                    msg['To'] = email
                    s.sendmail("ppwnotification@gmail.com", email, msg.as_string())

            except Exception as e:
                print('Couldnt send some emails. Error: ', e)
            finally:
                s.quit()


            #queuing emails at the start of the day
            if(datetime.now()> morning_milestone):
                with DbManager().get_client() as c:
                    users = c['PaperlessWorkflow']['Users']
                    search_query ={'notification_freq' : "DAILY"}
                    if morning_milestone.weekday() ==0: #if day is monday, include WEEKLY users as well
                        search_query = {'notification_freq' :{ '$in' : ["DAILY", "WEEKLY"] }} 
                    users_to_notify = users.find(search_query, {'pending_approvals'})
            
                    for cur_user in users_to_notify:
                        user_id = cur_user['_id']
                        with DbManager().get_client() as c:
                            forms = c['PaperlessWorkflow']['Forms']
                            num_of_pending = len([f for f in forms.find({'cur_level.approvers_id':user_id}, {})])
                        if num_of_pending>0:
                            msg = f"Hello\n\nYou have {num_of_pending} pending approvals.\n\nHave a nice day."
                            self.schedule_email(receiver_email=user_id, content=msg)

                morning_milestone+=timedelta(days=1) # =datetime(morning_milestone.year, morning_milestone.month, morning_milestone.day+1, hour = morning_milestone.hour, minute =morning_milestone.minute)