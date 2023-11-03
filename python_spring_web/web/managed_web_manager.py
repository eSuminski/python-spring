from codecs import StreamReader, StreamWriter
import asyncio
import inspect

from python_spring_core.core.manager import ApplicationContext, manage
from python_spring_web.web.managed_route_mapper import RouteMapper

@manage
class WebManager:

    def start(self, host: str = "127.0.0.1", port: int = 8000):
        self.populate_route_mapper_mappings()
        try:
            # Start the server on the specified host and port
            asyncio.run(self.start_server(host, port))
        except KeyboardInterrupt:
            print("Shutting down server")

    async def start_server(self, host: str = "127.0.0.1", port: int = 8000):
        # Start a server and bind it to the specified host and port
        server = await asyncio.start_server(self.handle_request, host, port)
        
        # Print a message indicating where the server is listening
        print(f"Listening at: http://{host}:{port}") 

        # Start serving requests forever until cancelled
        await server.serve_forever()


    async def handle_request(self, reader:StreamReader, writer:StreamWriter):
        # Read the request from the reader and decode it into a string
        request:str = (await reader.read(1024)).decode()

        # Extract the HTTP request method, URI, and version from the request
        method, uri, http_version = self.get_http_request_data(request)

        # Print the method, URI, and version for debugging purposes
        print(method, uri, http_version)

        if method == "GET" and uri == "/hello":
            response = f'{http_version} 200 OK\n\n\f{RouteMapper.mappings["GET"]["/hello"]()}'
        else:
            # Get the index HTML content from the WebManager class and construct the response
            index_content = WebManager.get_index()
            response = f'{http_version} 200 OK\n\n\f{index_content}'

        # Write the response to the writer and encode it into bytes
        writer.write(response.encode())

        # Flush the writer buffer and send the response
        await writer.drain()

        # Close the writer
        writer.close()

    @staticmethod
    def get_index():
        with open("python_spring_web\\web\\resources\\index.html") as index_:
            content = index_.read()
            return content

    @staticmethod
    def get_http_request_data(request: str):
        headers = request.split("\n")
        method, uri, version = headers[0].split()
        return (method, uri, version)
    
    def find_controllers(self):
        for object in ApplicationContext.managed_objects.values():
            if hasattr(object, "__is_controller__") and object.__is_controller__:
                yield object

    def find_route_methods(self):
        controler: object
        for controler in self.find_controllers():
            for name, func in inspect.getmembers(controler, inspect.ismethod):
                if hasattr(func, "__route__") and hasattr(func, "__verb__"):
                    yield controler, name

    def populate_route_mapper_mappings(self):
        for controler, name in self.find_route_methods():
            route = getattr(controler, name).__route__
            verb = getattr(controler, name).__verb__
            function = getattr(controler, name)
            RouteMapper.mappings[verb][route] = function
    