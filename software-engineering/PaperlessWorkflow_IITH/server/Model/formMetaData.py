import json
import os

filepath = os.path.dirname(os.path.abspath(__file__))+"/forminfo.json"
class FormMetaData:
    """
    Contains metadata for every form instance.

    Attributes:
        form_uid (str): unique id of the form
        display_name (str): display name of the form
        n_levels (int): number of levels in the chain of approval (including applicant level)
        users (list): contains the list of users at each level
        req_fields (list): contains the list of required fields at each level
    """
    def __init__(self, form_type:str = None, input_dict:str = None):

        if input_dict != None:
            json_dict = input_dict
            self.form_type = json_dict["form_type"]
            self.display_name = json_dict["display_name"] 
            self.n_levels = json_dict["n_levels"]
            self.users = json_dict["users"]
            self.req_fields = json_dict["req_fields"]
        elif form_type != None:
            self.set_type(form_type)

    def set_type(self, form_type: str):
        with open(filepath) as f:
            forminfo = json.load(f)
            if form_type not in forminfo:
                raise ValueError(f"Form with name '{form_type}' does not exist!")
            forminfo = forminfo[form_type]

            self.form_type = form_type
            self.display_name = forminfo["name"]
            self.n_levels = forminfo["n_levels"]
            self.users = [[]]*self.n_levels
            self.req_fields = [[]]*self.n_levels

            for i, level in enumerate(forminfo["level_data"]):
                self.users[i] = level["users"]
                self.req_fields[i] = level["req_fields"]

    def get_level(self,index):
        return self.users[index],self.req_fields[index]
    
    def get_field_cnt_at_level(self,index):
        return len(self.req_fields[index])
    
    def to_dict(self)->str:
        json_dict = {}
        json_dict["form_type"]= self.form_type if hasattr(self, 'form_type') else None
        json_dict["display_name"] = self.display_name if hasattr(self, 'display_name') else None
        json_dict["n_levels"] = self.n_levels if hasattr(self, 'n_levels') else None
        json_dict["users"] = self.users if hasattr(self, 'users') else None
        json_dict["req_fields"] = self.req_fields if hasattr(self, 'req_fields') else None
        return json_dict
# Testing code
# f = FormMetaData("leave")
# print(f.form_uid)
# print(f.display_name)
# print(f.n_levels)
# print(f.users[2])
# print(f.req_fields[2])
