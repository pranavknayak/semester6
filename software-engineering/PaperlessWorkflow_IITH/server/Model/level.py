import json
class Level:
    def __init__(self,_users_id=None,_fields=None,_approvers_id=None,_lvl_no=None, inp_dict = None) -> None:
        """Constructor for Level class

        Args:
            _users_id (_type_, optional): The list of all possible users who can make change to this level. Defaults to None.
            _fields (_type_, optional): The field meta information of this level. Defaults to None.
            _approvers_id (_type_, optional): the subset of users who are allowed to make changes at this level. Defaults to None.
            _lvl_no (_type_, optional): Current level number of the form. Defaults to None.
            inp_dict (_type_, optional): Internal stuff for ORM,dont touch. Defaults to None.
        """
        if inp_dict==None:
            self.fields=_fields
            self.total_fields=len(_fields) if _fields != None else None
            self.user_id=_users_id #what does this do?
            self.approvers_id=_approvers_id
            self.lvl=_lvl_no
        else:
            json_dict = inp_dict
            self.fields=json_dict['fields']
            self.total_fields=json_dict['total_fields']
            self.user_id=json_dict['user_id']
            self.approvers_id=json_dict['approvers_id']
            self.lvl=json_dict['lvl']
    
    def get_field_at(self,index):
        if(index> len(self.fields)):
            raise Exception("Invalid index requested")
        return self.fields[index]
    
    def get_level_no(self):
        return self.lvl
    
    def get_tot_fields(self):
        return self.total_fields
    
    def to_dict(self):
        json_dic = {}
        json_dic["fields"]=self.fields
        json_dic["total_fields"]=self.total_fields
        json_dic["user_id"]=self.user_id
        json_dic["approvers_id"]=self.approvers_id
        json_dic["lvl"]=self.lvl
        return json_dic