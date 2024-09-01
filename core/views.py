from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, FileResponse

from .services.content_extractor import get_main_content
from .services.text_to_speech import TextToSpeech

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
  
@require_http_methods(['POST'])
@csrf_exempt
def generate(request):
  content = request.POST.get('content')
  if content is None or content == '':
    return JsonResponse({'message': 'Text content not found'}, status=400)
  
  text_to_speech = TextToSpeech()
  language = text_to_speech.detect_language(content)
  language = language if language in text_to_speech.languages else 'en'
  raw_wav = text_to_speech.generate_speech(content, language=language)
  audio_rate = text_to_speech.output_sample_rate
  wav_buffer = text_to_speech.serialize_wav(raw_wav, sample_rate=audio_rate)
  wav_buffer.seek(0)
  
  return FileResponse(wav_buffer)
