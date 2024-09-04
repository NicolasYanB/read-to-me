from typing import Callable, Any, Union
from pathlib import Path
from io import BytesIO
import contextlib
import warnings
import os

from langdetect import detect
from scipy.io import wavfile
from TTS.api import TTS
import numpy as np
import torch

warnings.filterwarnings('ignore')

def disable_print(caller: Callable, *args, **kwargs) -> Any:
  with open(os.devnull, 'w') as f, contextlib.redirect_stdout(f):
    return caller(*args, **kwargs)

class TextToSpeech:
  model = disable_print(TTS, 'tts_models/multilingual/multi-dataset/xtts_v2', gpu=torch.cuda.is_available())

  def __init__(self):
    self.output_sample_rate: int = TextToSpeech.model.synthesizer.output_sample_rate
    self.languages: list[str] = TextToSpeech.model.languages

  def detect_language(self, text: str) -> str:
    lang = detect(text)
    return lang

  def generate_speech(self, text: str, language: str = 'en', speaker_path: Union[Path, None] = None) -> list[float]:
    speaker_arg = {}
    if speaker_path is None:
      speaker_arg['speaker'] = 'Claribel Dervla'
    else:
      speaker_arg['speaker_wav'] = str(speaker_path)

    wav = disable_print(
      TextToSpeech.model.tts,
      text,
      language=language,
      **speaker_arg
    )

    return wav
  
  def serialize_wav(self, wav: list[float], sample_rate: int = 44100) -> BytesIO:
    MAX_AMP = 32767

    wav_norm = np.array(wav) * (MAX_AMP / max(0.01, np.max(np.abs(wav))))
    wav_norm = wav_norm.astype(np.int16)
    wav_buffer = BytesIO()
    wavfile.write(wav_buffer, sample_rate, wav_norm)
    wav_buffer.seek(0)
    return wav_buffer
