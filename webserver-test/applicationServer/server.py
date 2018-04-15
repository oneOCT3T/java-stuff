import socket
import inspect

"""
    If it were me, I would've implemented the Java web server
    using non-blocking sockets (asynchronous) and likewise with this server
    for handling multiple clients at once

    For now I have tried making it as scalable as possible
"""
class Server:
    def __init__(self, host : str, port : int, on_data_func : callable):

        #validate the provided callback
        self.is_valid_data_callback(on_data_func)

        self.host = host
        self.port = port
        self.BUFFER_SIZE = 516
        self.on_incoming_data = on_data_func

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.shutdown = True
        
    
    def start(self):
        self.socket.bind((self.host, self.port))
        self.socket.listen()
        self.shutdown = False

        while not self.shutdown:
            (sock, addr) = self.socket.accept()
            with sock:
                data = sock.recv(self.BUFFER_SIZE).decode("utf-8")

                if(data):
                    response = self.on_incoming_data(data)
                    sock.send(response.encode())
                else:
                    pass

                sock.close()

    def close(self):
        self.shutdown = True

            
    def is_valid_data_callback(self, func : callable):
        params = inspect.signature(func).parameters
        return_type = inspect.signature(func).return_annotation
        if str(params['data']) != "data:str":
            print("ServerFunctionError: function {0} must have a 'data:str' parameter.".format(func))
            exit()

        if len(params) != 1:
            print("ServerFunctionError: function {0}  must have only one parameter.".format(func))
            exit()
        
        if str(return_type) == "str":
            print("ServerFunctionError: function {0} must have a str return type specified.".format(func))
            exit()
        return True







