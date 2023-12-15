try:
    from TTS.api import TTS
    from TTS.utils.synthesizer import Synthesizer
except ModuleNotFoundError:
    print("Could not find the TTS module.")
    raise

def do_tts(text):
    model = TTS('tts_models/multilingual/multi-dataset/xtts_v2').to('cuda')

    #model.tts_to_file(
    #    text=text,
    #    file_path=output_file,
    #    speaker_wav=['path/to/wave/file'],
    #    language='English'
    #    )

    #audio_data = model.tts(
    #    text=text,
    #    speaker_wav=['path/to/wave/file'],
    #    language='English'
    #    )

    pass