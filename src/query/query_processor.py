import logging

class Query_Processor:
    def __init__(self, graph):
        self.logger = logging.getLogger(__name__)
        
    def accept_query(self):
        while True:
            query = input(">")
            commands = query.split()
            if len(commands) == 0:
                print("error parsing query")
                continue
            elif commands[0] == "path":
                path_query(commands[1:])
            elif commands[0] == "range":
                range_query(commands[1:])
            elif commands[0] == "nearest":
                nearst_query(commands[1:])
            else:
                print("error parsing query")

    def path_query(self, commands):
        # Todo
    
    def range_query(self, commands):
        # Todo

    def nearst_query(self, commands):
        # Todo

