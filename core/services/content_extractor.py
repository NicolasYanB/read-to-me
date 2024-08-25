from readability import Document
from bs4 import BeautifulSoup
from requests import get

def get_main_content(url: str) -> str:
  response = get(url)
  status_code = response.status_code
  content_type = response.headers['content-type']
  if status_code != 200 or 'text/html' not in content_type:
    raise Exception(f'There was an error on the url request: {url}\nstatus code: {status_code}\n{content_type}')
  doc = Document(response.content)
  text = BeautifulSoup(doc.summary(), 'lxml').text
  return text