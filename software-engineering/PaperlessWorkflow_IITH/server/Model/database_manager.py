from queue import Queue
from threading import Lock
from pymongo import MongoClient
from bson.objectid import ObjectId

class SingletonMetaClass(type):
    my_instances = {}
    thread_lock: Lock = Lock()

    def __call__(cls, *args, **kwargs):
        with cls.thread_lock:
            if cls not in cls.my_instances:
                inst = super().__call__(*args, **kwargs)
                cls.my_instances[cls] = inst
        return cls.my_instances[cls]

class DbManager(metaclass = SingletonMetaClass):
    """An thread safe singleton object pool class for MongoClient.client
    Intended use:\n
    with DbManager().get_client() as c:
        c.get_database('example)\n
        ... 
    """
    class ClientWrapper:
        """a context managing class. sole purpose of this class is to allow DbManager.get_client() to be used in a 'with' statement"""
        def __init__(self, client) -> None:
            self.client = client
        def __enter__(self):
            return self.client
        def __exit__(self, a, b, c):
            DbManager().return_client(self.client)
        def __call__(self, *args, **kwds):
            return self.client

    def __init__(self) -> None:
        self.max_size = 10 #total number of clients
        self.clientQ = Queue(maxsize= self.max_size) #saves the clients available for use
        self.host = 'mongodb+srv://cs20btech11004:Y1JDdwqWBLgOWp2g@cluster0.iz8c5af.mongodb.net/?retryWrites=true&w=majority'
        for _ in range(self.max_size):
            try: self.clientQ.put(MongoClient(self.host))
            except: raise Exception('Cannot connect to db :(')
        self.lock = Lock()
    def get_client(self):
        """returns a client wrapper object containing the MongoClient
        Returns:
            a ClientWrapper obj.
        to get MongoClient obj\n
        client =  ClientWrapper() or client = ClientWrapper().client
        """
        while self.clientQ.empty():
            continue
        with self.lock:
            return self.ClientWrapper(self.clientQ.get())
    def return_client(self, client):
        """saves the client back into the DbManager"""
        if self.clientQ.full()==False:
            with self.lock:
                self.clientQ.put(client)

#############################
#       intended use        #
#############################        
# with DbManager().get_client() as c:
    # forms = c['PaperlessWorkflow']['Forms']
    # obj = forms.find_one({"_id" : ObjectId('643ff5dd326f4d6638bea447')})
    # print(type(obj))
    # for x in obj:
    #     print(f"{x} ({type(obj[x])}): {obj[x]}")



    # forms = c['PaperlessWorkflow']['Forms']
    # submitted_forms_query = {'applicant_id':'aman.panwar2002@gmail.com'}
    # for x in forms.find(submitted_forms_query, {}):
    #     print(type(x))
    #     print(x)
    #     print("")
    