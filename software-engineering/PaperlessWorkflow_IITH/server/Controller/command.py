import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__))+'/..')
from  Model.form import Form
from Model.util import show_form
from Model.formMetaData import FormMetaData
from Model.level import Level
from Model.fields import Field
from Model.data import Data
import time

class Command:
    def execute(self):
        pass

class Accept:
    """This function is used when the officer has filled the fields and approved the form to the next level
    """
    def __init__(self,_form_id,_user_id,_field_vals) -> None:
        """This initalilizes the paramters of the function

        Args:
            _form_id (_type_): ID of the form
            _user_id (_type_): User ID making changes
            _field_vals (_type_): List of field values from front end ,in index order where you want to make changes
        """
        self.form_id=_form_id
        self.user_id=_user_id
        self.field_vals=_field_vals
    
    def officer_approve(self,remarks:str) -> bool:
        """_summary_

        Returns:
            bool: Tells if the execution of the Accept request was successfull,can fault due to invalid parameters

        """
        #This function internally faults if invalid form_id requested
        F_instance =Form(ID=self.form_id)
        if self.user_id in F_instance.cur_level.approvers_id and F_instance.status=="PENDING":
            for x in range(len(self.field_vals)):
                F_instance.update_field(x,self.user_id,self.field_vals[x])
            F_instance.data.append_approval(time.time(),self.user_id,F_instance.cur_level_no,"APPROVED",remarks)
            F_instance.cur_level_no+=1
            # n levels total ,last level is n-1 ,equality implies  all levels exhausted,ie accpeted
            if F_instance.cur_level_no>=F_instance.form_meta.n_levels:
                F_instance.status="ACCEPTED"
                # F_instance.cur_level=None
            else:
                users_info,field_info=F_instance.form_meta.get_level(F_instance.cur_level_no)
                F_instance.cur_level=Level(users_info,field_info,users_info,F_instance.cur_level_no)
            #POST BACK TO DB
            if F_instance.save_to_db():
                return True
            else :
                print("Error,DB not updated")
                return False
        else:
            print("Invalid call,User not valid/ Invalid Form")
            return False
    
    def user_submit(self,form_name:str):
        F_new=Form()
        F_new.form_meta=FormMetaData(form_type=form_name)
        # Initilizing current level in special manner,
        # Modify Current level to have applicant id in level 0 of form metadata copy of form
        # This way even in reviews when formis sent back to applicant ,applicant can see the form

        F_new.form_meta.users[0].append(self.user_id)
        F_new.applicant_id=self.user_id
        F_new.cur_level_no=0

        
        field_lvl0_info=F_new.form_meta.get_level(0)[1]
        F_new.cur_level=Level([F_new.applicant_id],field_lvl0_info,[F_new.applicant_id],0)
        F_new.status="PENDING"
        F_new.data=Data()

        #Add the vals the user gave to the form
        for i in range(len(self.field_vals)):
            F_new.update_field(i,self.user_id,self.field_vals[i])

        F_new.cur_level_no+=1
        user_info,field_info=F_new.form_meta.get_level(1)
        F_new.cur_level=Level(user_info,field_info,user_info,1)
        F_new.data.append_approval(time.time(),self.user_id,0,"SUBMITTED","NA")

        #POST BACK TO DB
        if(F_new.save_to_db()):
            print(F_new.ID)
            return True, F_new.ID
        else: 
            print("Created form not posted to DB")
            return False, F_new.ID
        
    def notify():
        pass

class Reject:
    def __init__(self,_form_id,_user_id,_rejection_remarks) -> None:
        self.form_id=_form_id
        self.user_id=_user_id
        self.reject_reason=_rejection_remarks

    def execute(self):
        #This function internally faults if invalid form_id requested
        F_instance =Form(ID=self.form_id)
        if self.user_id in F_instance.cur_level.approvers_id and F_instance.status=="PENDING":
            F_instance.status="REJECTED"
            F_instance.data.append_approval(time.time(),self.user_id,F_instance.cur_level_no,"REJECTED",self.reject_reason)
            #POST BACK TO DB
            if(F_instance.save_to_db()):
                print(F_instance.ID)
                return True
            else: 
                print("Error,DB not updated")
                return False
        else: 
            print("Invalid call,User not valid/ Invalid Form")
            return False
    def notify():
        pass

class Review:
    def __init__(self,_form_id:str,_user_id:str,_review_remark:str) -> None:
        self.form_id=_form_id
        self.user_id=_user_id
        self.review_reason=_review_remark
    def execute(self):
        F_instance =Form(ID=self.form_id)
        if self.user_id in F_instance.cur_level.approvers_id and F_instance.status=="PENDING":
            #Applicant layer(0) cant send for review
            if F_instance.cur_level_no==0:
                print("Invalid request applicant (layer 0) cannot send form for review")
                return False
            F_instance.data.append_approval(time.time(),self.user_id,F_instance.cur_level_no,"REVIEW",self.review_reason)
            F_instance.cur_level_no-=1
            
            users_info,field_info=F_instance.form_meta.get_level(F_instance.cur_level_no)
            F_instance.cur_level=Level(users_info,field_info,users_info,F_instance.cur_level_no)
            
            #POST BACK TO DB
            if F_instance.save_to_db():
                print(F_instance.ID)
                return True
            else :
                print("Error,DB not updated")
                return False
        else: 
            print("Invalid call,User not valid/ Invalid Form")
            return False   
        pass
    def notify():
        pass
