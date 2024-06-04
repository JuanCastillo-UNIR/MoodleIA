import requests  
from bs4 import BeautifulSoup, Tag  
from IPython.display import display, HTML  
  
def obtener_faqs():
    faqs = ''
    # Obtener y analizar el contenido HTML  
    soup = BeautifulSoup(requests.get('https://becat.online/FAQ/').content, 'html.parser') 
    # Procesar y mostrar el contenido de cada acordeón  
    for accordion in soup.select('#accordion h3'):  
        title = accordion.get_text(strip=True)  
        content_div = accordion.find_next_sibling('div')  
        content = ""  
        # Función para asegurar que todas las URLs sean absolutas  
        def ensure_absolute_url(url):  
            return url if url.startswith('http') else f"https://becat.online/FAQ/{url}"  
        # Procesar todos los elementos dentro del div de contenido  
        for element in content_div.children:  
            if isinstance(element, Tag):  # Asegura que el elemento es un Tag antes de usar find_all  
                imgs = element.find_all('img')  
                for img in imgs:  
                    img['src'] = ensure_absolute_url(img['src'])  
    
                links = element.find_all('a')  
                for link in links:  
                    if 'href' in link.attrs:  
                        link['href'] = ensure_absolute_url(link['href'])  
                content += str(element)  
        faqs += f"<h2>{title}</h2><div>{content}</div>"
    return faqs