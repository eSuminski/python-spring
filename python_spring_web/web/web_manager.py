"""
    this class will be used to find the classes/methods that perform actions on the data 
    recieved and returned via the web. It will also spin up the server and manage the
    deployment of the server
"""

from codecs import StreamReader, StreamWriter
import asyncio


class WebManager:

    @classmethod
    async def handle_request(cls, reader:StreamReader, writer:StreamWriter):
        request:str = (await reader.read(1024)).decode()
        # print(request) # for debugging
        method, uri, http_version = request.split("\n")[0].split()
        # print(method, uri, http_version) # for debugging
        response = f'{http_version} 200 OK\n\n\f{WebManager.get_index()}'
        writer.write(response.encode())
        await writer.drain()
        writer.close()

    @classmethod
    async def start(cls, host:str = "127.0.0.1", port: int = 8000):
        server = await asyncio.start_server(WebManager.handle_request, host, port)
        async with server:
            print("Listening at: http://localhost:8000")
            await server.serve_forever()


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
    