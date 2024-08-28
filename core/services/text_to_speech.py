from TTS.api import TTS

class TextToSpeech:
  def __init__(self):
    self.model = None

  def init_model(self):
    self.model = TTS('tts_models/multilingual/multi-dataset/xtts_v2', gpu=False)

tts = TextToSpeech()