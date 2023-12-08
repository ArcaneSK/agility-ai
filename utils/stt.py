import speech_recognition as sr

def do_stt(audio_stream, whipser_model='small.en', whipser_language='english'):
    transcription = ""
    r = sr.Recognizer()

    with sr.AudioFile(audio_stream) as source:
        audio_data = r.record(source)

        try:
            transcription = r.recognize_whisper(audio_data, language=whipser_language, model=whipser_model)
        except sr.UnknownValueError:
            print("Whisper could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Whisper", e)

    return transcription