from io import BytesIO

from django.test import TestCase
import numpy as np

from ..services.utils import STATIC_PATH, get_wave_duration
from ..services.text_to_speech import TextToSpeech

class TextToSpeechTestCase(TestCase):
  @classmethod
  def setUpClass(cls):
    super(TextToSpeechTestCase, cls).setUpClass()
    cls.tts = TextToSpeech()

  def test_wav_generation(self):
    text = 'Hello World!'
    raw_wav = TextToSpeechTestCase.tts.generate_speech(text)
    self.assertIsInstance(raw_wav, list)

  def test_wav_generation_with_speaker(self):
    test_speaker_path = STATIC_PATH / 'test/speaker.wav'
    text = 'Hello World!'
    raw_wav = TextToSpeechTestCase.tts.generate_speech(text, speaker_path=test_speaker_path)
    self.assertIsInstance(raw_wav, list)

  def test_audio_serialization(self):
    """
    Test the wav generation by comparing the duration of buffer generated from
    a numpy array saved on a .npy file with a .wav file. They must be the same,
    once the array was generated with the .wav file itself
    """
    path = STATIC_PATH.joinpath('test')
    wav_array = np.load(path / 'test.npy')
    wav_buffer = TextToSpeechTestCase.tts.serialize_wav(wav_array)
    self.assertIsInstance(wav_buffer, BytesIO)
    
    wav_duration = get_wave_duration(wav_buffer)
    test_duration = get_wave_duration(str(path / 'test.wav'))
    self.assertEqual(wav_duration, test_duration)

  def test_language_detection(self):
    text1 = 'this is an english text'
    text2 = 'esse é um texto em português'

    lang1 = TextToSpeechTestCase.tts.detect_language(text1)
    lang2 = TextToSpeechTestCase.tts.detect_language(text2)

    self.assertEqual(lang1, 'en')
    self.assertEqual(lang2, 'pt')
