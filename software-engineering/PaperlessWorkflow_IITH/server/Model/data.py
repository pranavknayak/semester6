import time
import json
from Model.fields import *

from copy import deepcopy
class Data:
    """Holds the log value as json

    """

    def __init__(self, data: str = "", inp_dict: dict = None) -> None:
        """initializes the data object

        Args:
            data (str, optional): _description_. Defaults to "".
        """
        json_dict = {}
        if inp_dict == None:
            json_dict['log'] = []
            json_dict['approval_log'] = []
        else:
            json_dict = inp_dict
            temp = []
            for l in json_dict['log']:
                fe= l['field_entry']
                arg_list = [fe['display_name'],fe['value']]
                if 'values_list' in fe.keys():
                    arg_list = arg_list[0:-1]+ [fe['values_list']]+ [arg_list[-1]]
                l['field_entry'] = FieldFactory(field_type=fe['field_type'],arg_list=arg_list)
                temp.append(l)
            json_dict['log'] = temp

        self.log = json_dict['log']
        self.approval_log = json_dict['approval_log']

    def to_dict(self):
        json_dict = {}
        json_dict["log"] = deepcopy(self.log)
        for l in json_dict['log']:
            l['field_entry'] = l['field_entry'].to_dict()
        json_dict["approval_log"] = self.approval_log
        return json_dict

    def append_field(self, time: time.time, u_id: str, level_no: int, field_index: int, field_entry: Field):
        """Adds the data(field) submitted by user to the log object

        Args:
            time (time.time): time at which this update is being made
            u_id (str): user_id who made this update
            level_no (int): The level at which this update is being made
            field_index (int): the index of the field where update is being made
            field_entry (Field): The actual field value getting stored
        """
        # it was storing actual time of save. i ask the caller for time now
        # also shouldn;t log save multiple fields in one entry. i'e all the field filled by the user
        # this works too but we are saving unnecessary data... :(
        self.log.append({'time': time,
                         'uid': u_id,
                         'level_no': level_no,
                         'field_index': field_index,
                         'field_entry': field_entry})

    def append_approval(self, time: time.time, u_id: str, level_no: int, action: str, remarks: str):
        """Adds the layer approval/rejection/review to the approval_log object

        Args:
            time (time.time): time of this layer action
            u_id (str): user_id who made said action
            level_no (int): level at which this action is being made
            action (str): SUBMITTED APPROVED REVIEW or REJECTED
            remarks (str): officer remarks
        """
        self.approval_log.append({'time': time,
                                  'uid': u_id,
                                  'level_no': level_no,
                                  'action': action,
                                  'remark': remarks})

    def get_form_state(self) -> list[dict]:
        """return the cur state of form instance as a list of dictionaries

        Returns:
            list[dict]: form as list of dictionaries each containing the most recent value of a field,
            along with the level_no and field_index,user id and time of last update,
            can be accessed using the keys 'level_no', 'field_index', 'time', 'uid', 'field_entry'

        """
        #First we create a temp dict in order to get all the most recent fields
        temp = {}
        for ele in self.log:
            key_to_sort = (ele['level_no'], ele['field_index'])
            if key_to_sort in temp:
                if(temp[key_to_sort][0] < ele['time']):
                    temp[key_to_sort] = (ele['time'], ele['uid'], ele['field_entry'])
            else:
                temp[key_to_sort] = (ele['time'], ele['uid'], ele['field_entry'])
        #Next we create our return dictionary
        return_val=[]
        for key in temp:
            return_val.append({ 'level_no': key[0], 
                                'field_index': key[1],
                                'time': temp[key][0],
                                'uid': temp[key][1],
                                'field_entry': temp[key][2],
                                } ) 
        return return_val

    def get_log(self) -> list:
        """returns log made so far

        Returns:
            list: the object log
        """
        return self.log

    def get_approval_log(self) -> list:
        """returns approval log made so far

        Returns:
            list: returns a list of dictionaries each containing the time, uid, level_no, action, remark
        """
        return self.approval_log

    def get_update_cnt(self) -> int:
        """returns the total number of entries/updates to fields made so far

        Returns:
            int: _description_
        """
        return len(self.log)

    def get_field_cnt(self) -> int:
        """returns the total number of fields filled so far,
        should be equal to the number of unique fields uptill last level

        Returns:
            int: _description_
        """
        temp = set()
        for ele in self.log:
            filled_field = (ele['level_no'], ele['field_index'])
            temp.add(filled_field)
        return len(temp)

# d = Data()
# # d.append_approval(time.time(), "sd", "sd", "ds", "SDf")
# # time.sleep(1)
# # d.append_approval(time.time(), "sd", "sd", "ds", "SDf")
# f = Dropdown("dfdf", ['sdfsd', 'kkkkk'],"SDFsd")
# d.append_field(time.time(), "sdf", 4, 34, f)
# dic = d.to_dict()
# print("="*40)


# nd = Data(inp_dict=dic)
# print(nd.to_dict())
