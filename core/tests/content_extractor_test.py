from django.test import TestCase
from ..services.content_extractor import get_main_content

class ContentExtractorTestCase(TestCase):
  def test_fetch_main_body(self):
    url = 'https://en.wikipedia.org/wiki/24th_Waffen_Mountain_Division_of_the_SS_Karstj%C3%A4ger'
    content = get_main_content(url)
    self.assertIn('The 24th Waffen Mountain Division of the SS Karstjäger was a', content)

  def test_invalid_response(self):
    url = 'https://catfact.ninja/fact'
    self.assertRaises(Exception, lambda _: get_main_content(url))