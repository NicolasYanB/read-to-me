from pathlib import Path
from io import BytesIO
import contextlib
import wave
from typing import Union

from django.test import TestCase
import numpy as np

from ..services.text_to_speech import TextToSpeech

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

class TextToSpeechTestCase(TestCase):
  @classmethod
  def setUpClass(cls):
    super(TextToSpeechTestCase, cls).setUpClass()
    cls.tts = TextToSpeech()

  def test_wav_generation(self):
    text = 'Hello World!'
    raw_wav = TextToSpeechTestCase.tts.generate_speech(text)
    self.assertIsInstance(raw_wav, list)

  def test_audio_serialization(self):
    """
    Test the wav generation by comparing the duration of buffer generated from
    a numpy array saved on a .npy file with a .wav file. They must be the same,
    once the array was generated with the .wav file itself
    """
    path = Path(__file__).parent.parent.joinpath('static')
    wav_array = np.load(path / 'test.npy')
    wav_buffer = TextToSpeechTestCase.tts.serialize_wav(wav_array)
    self.assertIsInstance(wav_buffer, BytesIO)
    
    wav_duration = get_wave_duration(wav_buffer)
    test_duration = get_wave_duration(str(path / 'test.wav'))
    self.assertEqual(wav_duration, test_duration)
