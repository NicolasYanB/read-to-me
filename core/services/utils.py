from typing import Union
from pathlib import Path
from io import BytesIO
import contextlib
import wave

STATIC_PATH = Path(__file__).parent.parent.joinpath('static')

def get_wave_duration(wav_file: Union[str, BytesIO]) -> float:
  wav = None
  if isinstance(wav_file, BytesIO):
    wav = wave.Wave_read(wav_file)
  elif type(wav_file) is str:
    wav = wave.open(wav_file, 'r')
  else:
    raise Exception('Unsupported parameter type')

  with contextlib.closing(wav) as f:
    frames = f.getnframes()
    rate = f.getframerate()
    duration = frames / float(rate)
    return duration
