from Model.database_manager import DbManager
import smtplib
from email.message import EmailMessage
from Model.email_manager import EmailManager
class User:
    def __init__(self, email: str) -> None:
        data_dict: dict = {} #initilises data from this dict 
        with DbManager().get_client() as c:
            users = c['PaperlessWorkflow']['Users']
            data_dict = users.find_one({"_id": email})
            if data_dict == None: data_dict = {} #if user is not present already . data is empty

            #init submitted forms and pending forms
            forms = c['PaperlessWorkflow']['Forms']
            data_dict['past_forms'] = []
            for f in forms.find({'status': {'$in': ["ACCEPTED", "REJECTED"]}}, {'form_meta'}):
                for  fmeta in f['form_meta']:
                    for u in fmeta['users']:
                        if email in u:
                            data_dict['past_forms'].append(str(f['_id']))
            data_dict['submitted_forms'] = [str(f['_id']) for f in forms.find({'applicant_id':email}, {})]
            data_dict['pending_forms'] = [str(f['_id']) for f in forms.find({'cur_level.approvers_id':email}, {})]
            
        self.ID = data_dict.setdefault('email', email)
        self.pending_forms = data_dict.setdefault('pending_forms', [])
        self.submitted_forms = data_dict.setdefault('submitted_forms', [])
        self.past_forms = data_dict.setdefault('past_forms', [])
        self.notification_freq = data_dict.setdefault('notification_freq', "DAILY")
        self.role = data_dict.setdefault('role', "APPLICANT")
        self.version = data_dict.setdefault('version', 0)

    def save_to_db(self) -> bool:
        """saves the user to db

        Returns:
            bool: if a change was made to the db. returns False when update is not valid or if no change was made to the db entry 
        """
        with DbManager().get_client() as c:
            users = c['PaperlessWorkflow']['Users']

            search_field = {'_id': self.ID, 'version': self.version}

            my_data = self.to_dict()
            my_data['version'] += 1
            
            try: replace_result = users.replace_one(search_field, my_data, upsert=True)
            except: return False
            return replace_result.acknowledged

    def set_notification_frequency(self, frequency: str):
        valid_options = ["NEVER", "DAILY", "WEEKLY", "EVERY_FORM"]
        if frequency in valid_options:
            self.notification_freq = frequency
        else:
            raise Exception(
                f"Invalid frequency selected. Valid options are: {valid_options}")

    def to_dict(self) -> dict:
        json_dict = {}
        json_dict['_id'] = self.ID
        json_dict['pending_forms'] = self.pending_forms
        json_dict['submitted_forms'] = self.submitted_forms
        json_dict['notification_freq'] = self.notification_freq
        json_dict['role'] = self.role
        json_dict['version'] = self.version
        return json_dict

    def set_user_role(self, role):
        valid_options = ["APPLICANT", "OFFICER", "ADMIN"]
        if role in valid_options:
            self.role = role
        else:
            raise Exception(
                f"Invalid role selected. Valid roles are: {valid_options}")
    def send_notification(self, message:str):
        EmailManager().schedule_email(receiver_email=self.ID,
                                      content=f"You have {len(self.pending_forms)} pending forms")
        # try:
        #     msg = EmailMessage()
        #     msg.set_content(message)
        #     msg['Subject'] = "Update from Paperless Workflow App"
        #     msg['From'] = "ppwnotification@gmail.com"
        #     msg['To'] = self.ID
    
        #     s = smtplib.SMTP('smtp.gmail.com', 587)
        #     s.starttls()
        #     s.login('ppwnotification@gmail.com', "jqsgxbagdndwkqnp")
        #     s.sendmail("ppwnotification@gmail.com", self.ID, msg.as_string())
        #     s.quit()
        # except:
        #     return False
        # return True
    
# u = User('aman.panwar2002@gmail.com')
# u.send_email("test content")
# print('submitted: ', u.submitted_forms)
# print('approvals: ', u.pending_forms)
