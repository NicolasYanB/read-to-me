from pathlib import Path
import os

from django.test import TestCase

from ..services.utils import SpeakerHandler, get_wave_duration, UnsupportedFileException, STATIC_PATH

TEST_PATH = STATIC_PATH / 'test'

class SaveSpeakerFileTest(TestCase):
  def get_binary(self, path: Path) -> bytes:
    with open(path, 'rb') as f:
      return f.read()
    
  def test_save_speaker_file(self):
    speaker_name = 'test'
    test_wav_path = TEST_PATH / 'test.wav'
    test_wav = self.get_binary(test_wav_path)
    handler = SpeakerHandler(test_wav, speaker_name)
    self.assertTrue(handler.file_path.exists())
    test_duration = get_wave_duration(str(test_wav_path))
    speaker_duration = get_wave_duration(str(handler.file_path))
    self.assertEqual(test_duration, speaker_duration)
    os.remove(handler.file_path)

  def test_not_wav_binary(self):
    test_bin = self.get_binary(TEST_PATH / 'test.npy')
    self.assertRaises(UnsupportedFileException, lambda: SpeakerHandler(test_bin, 'test.wav'))

  def test_remove_file(self):
    test_wav_path = TEST_PATH / 'test.wav'
    test_wav = self.get_binary(test_wav_path)
    handler = SpeakerHandler(test_wav, 'test')
    self.assertTrue(handler.file_path.exists())
    handler.remove_speaker()
    self.assertFalse(handler.file_path.exists())

    