from abc import ABC
from datetime import date

class Field(ABC):
    """
    Abstract Base Class for all types of fields.

    Attributes:
        display_name (str): display name of the field
        value (any): value of the field
    """
    def __init__(self, display_name : str, value : any):
        self.field_type = None
        self.display_name = display_name
        self.value = value
        self.field_type = self.__class__.__name__
    def to_dict(self):
        return self.__dict__

class Textbox(Field):
    """
    Field to store plain text data.

    Attributes:
        display_name (str): display name of the textbox
        value (str): value of the field
    """
    def __init__(self, display_name : str, value : str):
        super().__init__(display_name, value)
    def __str__(self):
        return f'Textbox "{self.display_name}": Value = {self.value}'

class Date(Field):
    """
    Field to store text data in date-format.

    Attributes:
        display_name (str): display name of the date field
        value (datetime.date): value of the field
    """
    def __init__(self, display_name : str, value : date):
        super().__init__(display_name, value)

    def __str__(self):
        return f'Date "{self.display_name}": Value = {self.value}'

class Dropdown(Field):
    """
    Field to select from a list of options. Can only select one option at a time.

    Args:
        display_name (str): display name of the field
        values_list (list): list of options to choose from
        value (int): the index of the value chosen from the list of options
    """
    def __init__(self, display_name : str, values_list : list, value : int):
        super().__init__(display_name, value)
        self.values_list = values_list

    def __str__(self):
        return f'Dropdown "{self.display_name}":\nOptions = {self.values_list} \nValue = {self.values_list[self.value]}'

class Checkbox(Field):
    """
    Field to indicate whether a value is selected or not.
    Args:
        display_name (str): display name of field
        value (bool): stores whether the value of selected or not
    """
    def __init__(self, display_name : str, value : bool):
        super().__init__(display_name, value)
    def __str__(self):
        return f'Checkbox "{self.display_name}": Selected: {self.value}'

class File(Field):
    """
    Field to store files (pdf, png, jpg, etc). It stores the pathname/URL to the
    actual file.

    Attributes:
        display_name (str): the display name of the file field
        value (str): path of the file
    """
    def __init__(self, display_name : str, value : str):
        super().__init__(display_name, value)
    def __str__(self):
        return f'File "{self.display_name}"' #+ f': Path = {self.value}'

def FieldFactory(field_type:str, arg_list:list) -> Field:
    field_entry=False
    if field_type=="Textbox":
        field_entry=Textbox(arg_list[0],arg_list[-1])
    elif field_type=="Date":
        field_entry=Date(arg_list[0],arg_list[-1])
    elif field_type=="Checkbox":
        field_entry=Checkbox(arg_list[0],arg_list[-1])
    elif field_type=="Dropdown":
        field_entry=Dropdown(arg_list[0],arg_list[1],arg_list[-1])
    elif field_type=="File":
        field_entry=File(arg_list[0],arg_list[-1])
    else :
        raise Exception("INVALID FIELD VALUE")
    return field_entry