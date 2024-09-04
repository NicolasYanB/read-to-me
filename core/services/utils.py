from typing import Union
from pathlib import Path
from uuid import uuid1
from io import BytesIO
import contextlib
import wave
import os

STATIC_PATH = Path(__file__).parent.parent.joinpath('static')

class UnsupportedFileException(Exception): pass

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
  
class SpeakerHandler:
  def __init__(self, data: bytes, name: str):
    self.file_path: Path = STATIC_PATH / 'speakers' / self._save_speaker_file(data, name)

  def _save_speaker_file(self, data: bytes, name: str) -> str:
    if not self._is_wav(data):
      raise UnsupportedFileException('Parameter does not correspond to a .wav binary data')
    
    path = STATIC_PATH.joinpath('speakers')
    file_id = str(uuid1())
    filename = f'{file_id}_{name}.wav'
    file_path = path / filename
    with open(file_path, 'wb') as f:
      f.write(data)
    return filename

  def _is_wav(self, data: bytes) -> bool:
    wab_bin = BytesIO(data)
    wab_bin.seek(8)
    signature = wab_bin.read(4).decode(encoding='utf-8')
    return signature == 'WAVE'
  
  def remove_speaker(self):
    os.remove(self.file_path)
