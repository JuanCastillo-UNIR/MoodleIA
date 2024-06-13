import sys
import requests
from bs4 import BeautifulSoup
from IPython.core.display import HTML
import os
import PyPDF2
from src.api.common.services.openai_service import OpenAIService
from src.api.common.services.prompt_service import PromptService
from src.api.workflows.Foros.gpt_content import GptContent

class ForosWorkflow:
    _openai_service: GptContent

    def __init__(self, openai_service: OpenAIService, prompt_service: PromptService) -> None:
        self._openai_service = GptContent(openai_service, prompt_service)

    def entrada_token_discussionid(self):
        wstoken = '8c4b7d7f49bc9db13536925e3e2d74ca'
        discussionid = 1
        return wstoken, discussionid

    def lectura_documento(self, wstoken, discussionid):
        url = "https://sandbox.moodledemo.net/webservice/rest/server.php"
        params = {
            'wstoken': wstoken,
            'wsfunction': 'mod_forum_get_discussion_posts',
            'moodlewsrestformat': 'json',
            'discussionid': discussionid
        }
        response = requests.get(url, params=params)
        respuestas_posts = response.json()['posts'][::-1]
        return respuestas_posts

    def html_to_str(self, texto):
        html_object = HTML(texto)
        html_content = html_object.data
        soup = BeautifulSoup(html_content, 'html.parser')
        text = soup.get_text()
        return text

    def ejecutar_modelo(self, lista_respuestas):
        with open('docs/Eclesiologia.pdf', 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            all_text = ""
            for page_number in range(min(4, len(pdf_reader.pages))):
                page = pdf_reader.pages[page_number]
                text = page.extract_text()
                if text:
                    all_text += text
        posts = []
        for estudiante_respuesta in lista_respuestas:
            posts.append({estudiante_respuesta['author']['fullname']:estudiante_respuesta['message']})
        request = {'Pregunta': lista_respuestas[0]['message'], 
                   'Texto': all_text,
                   'Posts': posts[1:]}
        response = self._openai_service.get_foros_content(str(request))
        display(response)
        return response

    # Usar esta función solo en caso de que se necesite generar los feedbacks uno a uno en ciclo
    # def ejecutar_modelo(self, lista_respuestas):
    #     with open('docs/Eclesiologia.pdf', 'rb') as file:
    #         pdf_reader = PyPDF2.PdfReader(file)
    #         all_text = ""
    #         for page_number in range(min(3, len(pdf_reader.pages))):
    #             page = pdf_reader.pages[page_number]
    #             text = page.extract_text()
    #             if text:
    #                 all_text += text

    #     posts = []
    #     for estudiante_respuesta in lista_respuestas:
    #         posts.append({estudiante_respuesta['author']['fullname']:estudiante_respuesta['message']})

    #     respuestas = []
    #     for post in posts[1:]:
    #         request = {'Pregunta': lista_respuestas[0]['message'], 'Posts': post}
    #         response = self._openai_service.get_foros_content(str(request))
    #         respuestas.append(response)

    #     display(respuestas)
    #     return respuestas

    def subir_plataforma(self, wstoken, discussionid, feedback_message):
        url = 'https://sandbox.moodledemo.net/webservice/rest/server.php'
        data = {
            'wstoken': wstoken,
            'wsfunction': 'mod_forum_add_discussion_post',
            'moodlewsrestformat': 'json',
            'postid': discussionid,
            'subject': 'Re: Retroalimentaciones',
            'message': str(feedback_message)
        }
        response = requests.post(url, data=data)
        return response
    
    
    def execute(self) -> dict: # type: ignore
        wstoken, discussionid = self.entrada_token_discussionid()
        respuestas_posts = self.lectura_documento(wstoken, discussionid)
        feedback_message = self.ejecutar_modelo(respuestas_posts)
        html = ''
        for key, value in feedback_message.items():  
            html+=f"<br>{key.split('_')[0]}: {value}<br>"
        # result = "<br><br>".join([f"{key}: {value}" for d in feedback_message for key, value in d.items()])
        self.subir_plataforma(wstoken, discussionid, html)
        return True