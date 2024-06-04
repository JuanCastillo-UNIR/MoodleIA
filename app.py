from dash import Dash, html, dcc, Input, Output, State  
import dash_bootstrap_components as dbc  
  
from src.api.workflows.FAQs.extract_FAQs import obtener_faqs, obtener_faqs_unir  
from src.api.common.dependency_container import DependencyContainer  
  
# Inicialización del contenedor de dependencias  
DC = DependencyContainer()  
DC.initialize()  
  
app = Dash(__name__, external_stylesheets=[dbc.themes.MATERIA])  
  
app.layout = dbc.Container([  
    dbc.Row([dbc.Col([html.H1("ChatBot Becat - FAQs", className="text-center mb-4", style={'font-size': '2.5em', 'font-family': 'Comic Sans MS', 'color': '#0056b3'})])]),  
    dbc.Row([  
        dbc.Col([  
            dcc.Loading(  
                id="loading",  
                type="default",  
                children=html.Div(id='chat_area', style={'height': '520px', 'overflow': 'auto', 'padding': '10px', 'border': '1px solid #ccc', 'border-radius': '5px', 'font-family': 'Comic Sans MS', 'color': '#333'})  
            ),  
            dcc.Input(id='user_input', type='text', placeholder='Escribe tu pregunta...', style={'width': '100%', 'height': '50px', 'font-size': '1.2em', 'margin-top': '20px', 'border-radius': '5px', 'font-family': 'Comic Sans MS'}),  
            dbc.Button('Enviar', id='send_button', n_clicks=0, className="btn btn-primary mt-2", style={'width': '100%', 'background-color': '#0056b3', 'border-color': '#0056b3', 'font-family': 'Comic Sans MS'})  
        ], width=12)  
    ])  
], fluid=True, style={'max-width': '1200px', 'padding': '20px'})  
  
@app.callback(  
    Output('chat_area', 'children'),  
    Input('send_button', 'n_clicks'),  
    State('user_input', 'value'),  
    prevent_initial_call=True  
)  
def update_chat(n_clicks, user_input):  
    if user_input is None or n_clicks == 0:  
        return ""  
    request = {'Pregunta': user_input, 'FAQs': obtener_faqs() + obtener_faqs_unir()}  
    response = DC.get_schema_generator_workflow().execute(request)  
    content = response['Contenido']  
    if isinstance(content, bytes):  
        content = content.decode('utf-8')  
    src = f"data:text/html;charset=utf-8,{content}"  
    return html.Iframe(src=src, style={'width': '100%', 'height': '100%', 'border': 'none', 'font-family': 'Comic Sans MS'}, id='chat_iframe')  
  
if __name__ == '__main__':  
    app.run_server(debug=True)  