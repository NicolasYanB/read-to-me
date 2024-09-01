from django.test import TestCase
from ..services.content_extractor import get_main_content, UrlException

class ContentExtractorTestCase(TestCase):
  def test_fetch_main_body(self):
    url = 'https://en.wikipedia.org/wiki/24th_Waffen_Mountain_Division_of_the_SS_Karstj%C3%A4ger'
    content = get_main_content(url)
    self.assertIn('The 24th Waffen Mountain Division of the SS Karstjäger was a', content)

  def test_invalid_response(self):
    url = 'https://catfact.ninja/fact'
    self.assertRaises(UrlException, lambda: get_main_content(url))

  def test_invalid_url(self):
    url1 = 'qwerqwerqwer'
    url2 = 'https://uytfghgdc'
    self.assertRaises(UrlException, lambda: get_main_content(url1))
    self.assertRaises(UrlException, lambda: get_main_content(url2))
