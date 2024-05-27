import requests  
from bs4 import BeautifulSoup  
from IPython.display import display, HTML  
  
# Obtener y analizar el contenido HTML  
url = 'https://becat.online/faq-sobre-los-titulos-propios-de-la-unir/'  
response = requests.get(url)  
soup = BeautifulSoup(response.content, 'html.parser')  
  
# Procesar y mostrar el contenido de cada acordeón  
for accordion in soup.find_all('div', class_='et_pb_toggle'):  # Asegurarse de seleccionar el div correcto del acordeón  
    title = accordion.find('h3', class_='et_pb_toggle_title').get_text(strip=True)  # Extraer el título  
    content_div = accordion.find('div', class_='et_pb_toggle_content')  # Extraer el div que contiene el contenido  
  
    if content_div:  
        # Extracción del contenido textual, manteniendo etiquetas internas para formato  
        content = str(content_div)  
    else:  
        content = "No content available"  
  
    display(HTML(f"<h2>{title}</h2><div>{content}</div>"))  