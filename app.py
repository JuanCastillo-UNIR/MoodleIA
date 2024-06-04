from src.api.workflows.FAQs.extract_FAQs import obtener_faqs  
from dash import Dash, html, dcc, Input, Output  
import dash_bootstrap_components as dbc  
from src.api.common.dependency_container import DependencyContainer  
import base64  
  
DC = DependencyContainer()  
DC.initialize()  
  
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])  
  
app.layout = dbc.Container([  
    dbc.Row([dbc.Col([html.H1("ChatBot Becat - FAQs", className="text-center mb-4")])]),  
    dbc.Row([  
        dbc.Col([  
            dcc.Loading(  
                id="loading",  
                type="default",  
                children=html.Div(id='chat_area')  
            ),  
            dcc.Input(id='user_input', type='text', placeholder='Escribe tu pregunta...', style={'width': '100%'}, debounce=True),  
            dbc.Button('Enviar', id='send_button', n_clicks=0, className="btn btn-primary")  
        ], width=12)  
    ])  
], fluid=True)  
  
@app.callback(  
    Output('chat_area', 'children'),  
    Input('send_button', 'n_clicks'),  
    Input('user_input', 'value'),  
    prevent_initial_call=True  
)  
def update_chat(n_clicks, user_input):  
    if user_input is None:  
        return ""  
    request = {'Pregunta': user_input, 'FAQs': obtener_faqs()}  
    response = DependencyContainer.get_schema_generator_workflow().execute(request)  
      
    # Asegúrate de que la respuesta está en UTF-8  
    if isinstance(response['Contenido'], bytes):  
        content = response['Contenido'].decode('utf-8')  
    else:  
        content = response['Contenido']  
      
    encoded_content = base64.b64encode(content.encode('utf-8')).decode('utf-8')  
    src = f"data:text/html;base64,{encoded_content}"  
    return html.Iframe(src=src, style={'width': '100%', 'height': '500px', 'border': 'none'}, id='chat_iframe')  
  
if __name__ == '__main__':  
    app.run_server(debug=True)  