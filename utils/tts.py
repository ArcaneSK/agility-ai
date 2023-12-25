try:
    from TTS.api import TTS
    from TTS.utils.synthesizer import Synthesizer
except ModuleNotFoundError:
    print("Could not find the TTS module.")
    raise

class TextToSpeech:

    def __init__(self):
        self.model = TTS('tts_models/multilingual/multi-dataset/xtts_v2').to('cuda')

    def do_tts(self, text, speaker):
        return self.model.tts(
        text=text,
        speaker_wav=[f'voices\{speaker}.wav'],
        language='en'
        )