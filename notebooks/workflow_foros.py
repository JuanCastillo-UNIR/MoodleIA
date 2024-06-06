from src.api.common.services.openai_service import OpenAIService
from src.api.common.services.prompt_service import PromptService
from src.api.workflows.Foros.request_content import SchemaRequest
from src.api.workflows.Foros.gpt_content import GptContent

import requests
from bs4 import BeautifulSoup
from IPython.core.display import HTML
import sys
import os
import PyPDF2
from src.api.common.dependency_container import DependencyContainer


class ForosWorkflow:
    _openai_service: GptContent
    
    def __init__(self,
        openai_service: OpenAIService, 
        prompt_service: PromptService
    ) -> None:
        self._openai_service = GptContent(openai_service, prompt_service)

    # función que recibe los valores de entrada
    def entrada_token_discussionid():
        wstoken = input("Ingrese el valor del token: ")
        discussionid = input("Ingrese el valor del id del post (discusión): ")
        return wstoken, discussionid
    
    wstoken, discussionid = entrada_token_discussionid()
    
    # lectura del documento
    def lectura_documento(wstoken, discussionid):
        url = "https://sandbox.moodledemo.net/webservice/rest/server.php"

        params = {
        'wstoken': wstoken,
        'wsfunction': 'mod_forum_get_discussion_posts',
        'moodlewsrestformat': 'json',
        'discussionid': discussionid
        }

        # realiza la llamada a la api
        response = requests.get(url, params=params)

        # imprime la respuesta general (todo el foro) en formato JSON
        response.json()['posts']

        # ordena de manera descendente el diccionario de posts
        respuestas_posts = response.json()['posts'][::-1]

        return respuestas_posts
    
    # convierte la salida html a string
    def html_to_str(texto):
        html_object = HTML(texto)
        html_content = html_object.data
        soup = BeautifulSoup(html_content, 'html.parser')
        text = soup.get_text()
        return text
    
    respuestas_posts = lectura_documento(wstoken, discussionid)

    # Esta función devuelve una lista de diccionarios donde cada llave es un estudiante ysu valor es la respuesta del estudiante.
    def obtener_lista_diccionarios(respuestas_posts):

        # convierte la salida html a string
        def html_to_str(texto):
            html_object = HTML(texto)
            html_content = html_object.data
            soup = BeautifulSoup(html_content, 'html.parser')
            text = soup.get_text()
            return text

        # Código para almacenar respuestas
        lista_respuestas = []

        for respuesta in respuestas_posts[1:]:
            dicc_base = dict()
            dicc_base["Estudiante"] = respuesta["author"]["fullname"]
            dicc_base["Respuesta"] = html_to_str(respuesta["message"])
            lista_respuestas.append(dicc_base)

        return lista_respuestas
    
    lista_respuestas = obtener_lista_diccionarios(respuestas_posts)
    

    def ejecutar_modelo(lista_respuestas):
        # Obtener la ruta del directorio actual del notebook
        current_dir = os.getcwd()

        # Añadir la ruta al directorio raíz del proyecto al PYTHONPATH
        project_root = os.path.abspath(os.path.join(current_dir, '..'))
        if project_root not in sys.path:
            sys.path.append(project_root)

        # Abrir y leer el archivo PDF
        with open('docs/Eclesiologia.pdf', 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            
            all_text = ""
            
            # Leer las primeras 15 páginas o menos si el PDF tiene menos de 15 páginas
            for page_number in range(min(15, len(pdf_reader.pages))):
                page = pdf_reader.pages[page_number]
                text = page.extract_text()
                if text:
                    all_text += text

        # Inicializar el contenedor de dependencias
        DC = DependencyContainer()
        DC.initialize()

        # Lista de feedbacks
        lista_feedbacks = []

        # Asumiendo que lista_respuestas y pregunta están definidos
        for estudiante_respuesta in lista_respuestas:
            request = {
                'Pregunta': f'Vas a analizar cada párrafo del texto que te voy a pasar. Según el texto anterior, vas a contestar lo siguiente: {pregunta}', 
                'Texto': all_text,
                'Respuesta': estudiante_respuesta["Respuesta"]
            }
        response = DC.get_foros_content().execute(request)
        feedback = f"Retroalimentación para {estudiante_respuesta['Estudiante']}: {response['Respuesta']}"
        lista_feedbacks.append(feedback)
        feedback_message = "<br><br>".join(lista_feedbacks)
        
        return feedback_message
    
    feedback_message = ejecutar_modelo(lista_respuestas)
    
    def subir_plataforma(wstoken, discussionid, feedback_message):
        # Define the URL and token
        url = 'https://sandbox.moodledemo.net/webservice/rest/server.php'
        function = 'mod_forum_add_discussion_post'
        format = 'json'
        
        # Define the data
        data = {
            'wstoken': wstoken,
            'wsfunction': function,
            'moodlewsrestformat': format,
            'postid': discussionid, # esta en el json
            'subject': 'Re: Retroalimentaciones', #la ienes en el jaosn
            'message': feedback_message #Feedback
        }
        
        # Send the POST request
        response = requests.post(url, data=data)
        
        # Print the response
        print(response.json())
    
    subir_plataforma(wstoken, discussionid, feedback_message)


    def execute(self, request: SchemaRequest) -> dict: # type: ignore
        return self._openai_service.get_foros_content(str(request))