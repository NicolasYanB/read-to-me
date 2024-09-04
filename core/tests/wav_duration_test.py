from django.test import TestCase
import numpy as np

from ..services.utils import get_wave_duration, STATIC_PATH
from ..services.text_to_speech import TextToSpeech

TEST_PATH = STATIC_PATH / 'test'

class WavDurationTest(TestCase):
  def test_get_duration_with_path(self):
    self.assertEqual(get_wave_duration(str(TEST_PATH / 'test.wav')), 1)

  def test_get_duration_with_binary(self):
    tts = TextToSpeech()
    wav_array = np.load(TEST_PATH / 'test.npy')
    wav_buffer = tts.serialize_wav(wav_array)
    self.assertEqual(get_wave_duration(wav_buffer), 1)