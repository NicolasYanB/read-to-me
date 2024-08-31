from io import BytesIO
import contextlib
import warnings
import os

from scipy.io import wavfile
from TTS.api import TTS
import numpy as np

warnings.filterwarnings('ignore')

def disable_print_wrapper(caller, *args, **kwargs):
  with open(os.devnull, 'w') as f, contextlib.redirect_stdout(f):
    return caller(*args, **kwargs)

class TextToSpeech:
  model = disable_print_wrapper(TTS, 'tts_models/multilingual/multi-dataset/xtts_v2', gpu=False)

  def __init__(self):
    self.output_sample_rate = TextToSpeech.model.synthesizer.output_sample_rate

  def generate_speech(self, text: str) -> np.ndarray:
    wav = disable_print_wrapper(
      TextToSpeech.model.tts,
      text,
      language='en',
      speaker='Claribel Dervla'
    )

    return wav
  
  def serialize_wav(self, wav: list, sample_rate: int = 44100) -> BytesIO:
    MAX_AMP = 32767

    wav_norm = np.array(wav) * (MAX_AMP / max(0.01, np.max(np.abs(wav))))
    wav_norm = wav_norm.astype(np.int16)
    wav_buffer = BytesIO()
    wavfile.write(wav_buffer, sample_rate, wav_norm)
    wav_buffer.seek(0)
    return wav_buffer
