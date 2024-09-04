from typing import Callable
import re

from django.http import JsonResponse, FileResponse, HttpResponse, HttpRequest
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

from .services.speaker_handler import SpeakerHandler, UnsupportedFileException
from .services.content_extractor import get_main_content, UrlException
from .services.text_to_speech import TextToSpeech

def catch_error(view: Callable) -> Callable:
  def catch(request: HttpRequest):
    try:
      return view(request)
    except Exception as e:
      print(str(e))
      return HttpResponse(status=500)
  return catch

@require_http_methods(['GET'])
@catch_error
def extract(request: HttpRequest):
  url = request.GET.get('url')
  if url is None:
    return JsonResponse({'message': 'URL not defined'}, status=400)
  try:
    content = get_main_content(url)
    return JsonResponse({"content": content})
  except UrlException:
    return JsonResponse({'message': f'There is something wrong with the URL {url}'}, status=400)
  
@require_http_methods(['POST'])
@csrf_exempt
@catch_error
def generate(request: HttpRequest):
  content = request.POST.get('content')
  if content is None or content == '':
    return JsonResponse({'message': 'Text content not found'}, status=400)
  
  speaker_file = request.FILES.get('speaker')
  speaker_handler = None
  if speaker_file is not None:
    speaker_audio = speaker_file.read()
    speaker_name = re.sub(r'.wav$', '', speaker_file.name)

    try:
      speaker_handler = SpeakerHandler(speaker_audio, speaker_name)
    except UnsupportedFileException:
      return JsonResponse({'message': "The audio file must be a '.wav' file"}, status=400)
  
  text_to_speech = TextToSpeech()
  language = text_to_speech.detect_language(content)
  language = language if language in text_to_speech.languages else 'en'

  if speaker_handler is None:
    raw_wav = text_to_speech.generate_speech(content, language=language)
  else:
    raw_wav = text_to_speech.generate_speech(content, language=language, speaker_path=speaker_handler.file_path)
    speaker_handler.remove_speaker()

  audio_rate = text_to_speech.output_sample_rate
  wav_buffer = text_to_speech.serialize_wav(raw_wav, sample_rate=audio_rate)
  wav_buffer.seek(0)
  
  return FileResponse(wav_buffer)
