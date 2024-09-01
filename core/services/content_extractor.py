from readability import Document
from bs4 import BeautifulSoup
from requests import get
import requests

class UrlException(Exception): pass

def get_main_content(url: str) -> str:
  try:
    response = get(url)
  except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError) as e:
    raise UrlException(f'There was an erro on the url reqeust: {url}\n{str(e)}')
  
  status_code = response.status_code
  content_type = response.headers['content-type']
  if status_code != 200 or 'text/html' not in content_type:
    raise UrlException(f'There was an error on the url request: {url}\nstatus code: {status_code}\n{content_type}')
  doc = Document(response.content)
  text = BeautifulSoup(doc.summary(), 'lxml').text
  return text