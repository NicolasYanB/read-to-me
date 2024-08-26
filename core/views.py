from django.views.decorators.http import require_http_methods
from django.http import JsonResponse

from .services.content_extractor import get_main_content

@require_http_methods(['GET'])
def extract(request):
  url = request.GET.get('url')
  if url is None:
    return JsonResponse({'message': 'URL not defined'}, status=400)
  try:
    content = get_main_content(url)
    return JsonResponse({"content": content})
  except Exception:
    return JsonResponse({'message': f'There is something wrong with the URL {url}'}, status=400)
