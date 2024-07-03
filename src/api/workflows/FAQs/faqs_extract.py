from datetime import datetime, timedelta  
import requests, bs4  


class FAQsExtract:  
    FAQs: str  
    last_time_extracted: str = None  
  
    def __init__(self):
        self.FAQs = self.faqs_scraping()  
        self.last_time_extracted = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  

    def get_faqs(self):
        if self.last_time_extracted is None or self.needs_update():  
            self.FAQs = self.faqs_scraping()  
            self.last_time_extracted = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
        return self.FAQs
    
    def faqs_scraping(self): 
        faqs = ''  
        soup = bs4.BeautifulSoup(requests.get('https://becat.online/FAQ/').content, 'html.parser')  
        for accordion in soup.select('#accordion h3'):  
            title = accordion.get_text(strip=True)  
            content_div = accordion.find_next_sibling('div')  
            content = ""  
            for element in content_div.children:  
                if isinstance(element, bs4.Tag):  
                    imgs = element.find_all('img')  
                    for img in imgs:  
                        img['src'] = self.ensure_absolute_url(img['src'])  
                    links = element.find_all('a')  
                    for link in links:  
                        if 'href' in link.attrs:  
                            link['href'] = self.ensure_absolute_url(link['href'])  
                    content += str(element)  
            faqs += f"<h2>{title}</h2><div>{content}</div>"  
        return faqs  
  
    def ensure_absolute_url(self, url):  
        return url if url.startswith('http') else f"https://becat.online/FAQ/{url}"  
  
    def needs_update(self):  
        last_date = datetime.strptime(self.last_time_extracted, '%Y-%m-%d %H:%M:%S') 
        return datetime.now() >= last_date + timedelta(days=5)  