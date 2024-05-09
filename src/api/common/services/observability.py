import phoenix as px
from phoenix.trace.langchain import LangChainInstrumentor
import socket, os

class Observability:
    def __init__(self, port: int):
        self.port = port

    def __check_port_occupied(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            return s.connect_ex(('localhost', self.port)) == 0
        
    def launch_app(self):
        px.launch_app()

    def set_observability(self):
        if self.__check_port_occupied():
            print(f"Port {self.port} is already in use. Server is already started.")
            try:
                LangChainInstrumentor().instrument()
                print("Instrument succesfull")
            except Exception as e:
                print(f"An error has ocurred while instrumenting: {e}")
        else:
            try:
                self.launch_app()
            except Exception as e:
                print(f"An exception starting server has occurred: {e}")
            try:
                LangChainInstrumentor().instrument()
                print("Instrument succesful")
            except Exception as e:
                print(f"An exception has ocurred while instrumenting: {e}")