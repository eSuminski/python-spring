from codecs import StreamReader, StreamWriter
import asyncio

from python_spring_core.core.manager import manage
from python_spring_web.web.web_handler import WebHandler

@manage
class WebManager:

    def __init__(self, web_handler: WebHandler = None) -> None:
        self.web_handler = web_handler


    async def handle_request(self, reader:StreamReader, writer:StreamWriter):
        request:str = (await reader.read(1024)).decode()
        # print(request) # for debugging
        method, uri, http_version = self.get_http_request_data(request)
        print(method, uri, http_version) # for debugging
        response = f'{http_version} 200 OK\n\n\f{WebManager.get_index()}'
        writer.write(response.encode())
        await writer.drain()
        writer.close()

    async def start(self, host:str="127.0.0.1", port:int=8000):
        server = await asyncio.start_server(self.handle_request, host, port)
        async with server:
            print("Listening at: http://localhost:8000")
            await server.serve_forever()

    def start_server(self, host:str = "127.0.0.1", port: int = 8000):
        """
        Starts the server with the specified host and port.

        Args:
            host (str): The host IP address to bind the server to. Defaults to "127.0.0.1".
            port (int): The port number to bind the server to. Defaults to 8000.
        """
        asyncio.run(self.start(host, port))


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
    