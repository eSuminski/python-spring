"""
    this class will be used to find the classes/methods that perform actions on the data 
    recieved and returned via the web
"""

import socket

class WebManager:
    
    @classmethod
    def start_server(cls):
        """
            to start up our server we need to give host and port information. Ideally 
            this would be customizable, but will make it static for now 
        """
        server_host = "127.0.0.1"
        server_port = 8000

        """
            now we can create our socket
        """
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((server_host, server_port))
        server_socket.listen(1)
        print(f"Listening at {server_host}:{server_port}")
        try:
            while True:
                # wait for a connection from end user
                client_connection, client_address = server_socket.accept()

                # get the request
                request = client_connection.recv(1024).decode()
                # print(request) # debugging

                request_data = WebManager.get_http_request_data(request)
                # print(request_data) # debugging

                # return response
                response = f"HTTP/1.0 200 OK\n\n{WebManager.get_index()}"
                client_connection.sendall(response.encode())

                client_connection.close()
        except KeyboardInterrupt:
            server_socket.close()
            print("Goodbye!")

    @classmethod
    def get_index(cls):
        index_ = open("python_spring_web\\web\\resources\\index.html")
        content = index_.read()
        index_.close()
        return content

    @classmethod
    def get_http_request_data(cls, request: str):
        headers = request.split("\n")
        method, uri, version = headers[0].split()
        return (method, uri, version)


