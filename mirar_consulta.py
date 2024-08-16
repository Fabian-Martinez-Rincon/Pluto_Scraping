from bs4 import BeautifulSoup

headers = {
    "User-Agent": "python-requests/2.32.3"
}

def fetch_html(session, url):
    with session.get(url) as response:
        if response.status == 200:
            return response.text()
        else:
            return None
    

soup = BeautifulSoup(html_content, 'html.parser')
    
    
    
    
    
    
    
    
    
    
    
    
    
    