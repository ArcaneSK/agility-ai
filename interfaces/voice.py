import speech_recognition as sr
# from TTS.api import TTS

from config import Config

cfg = Config()

def run():
    pass
    # model_name = TTS.list_models()[0]
    # tts = TTS(model_name)
    # tts.tts_to_file(text="Hello world!", speaker=tts.speakers[0], language=tts.languages[0], file_path="output.wav")



    # r = sr.Recognizer()
    # with sr.Microphone() as source:
    #     print("Say something!")
    #     r.adjust_for_ambient_noise(source, duration=0.2)
    #     audio = r.listen(source)
    #     print("Sending... ")

    #     # recognize speech using Sphinx
    #     try:
    #         print("Sphinx thinks you said " + r.recognize_sphinx(audio))
    #     except sr.UnknownValueError:
    #         print("Sphinx could not understand audio")
    #     except sr.RequestError as e:
    #         print("Sphinx error; {0}".format(e))

    #     # recognize speech using Google Speech Recognition
    #     try:
    #         # for testing purposes, we're just using the default API key
    #         # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
    #         # instead of `r.recognize_google(audio)`
    #         print("Google Speech Recognition thinks you said " + r.recognize_google(audio))
    #     except sr.UnknownValueError:
    #         print("Google Speech Recognition could not understand audio")
    #     except sr.RequestError as e:
    #         print("Could not request results from Google Speech Recognition service; {0}".format(e))

    #     # recognize speech using Whisper API
    #     try:
    #         print(f"Whisper API thinks you said {r.recognize_whisper_api(audio, api_key=cfg.open_api_key)}")
    #     except sr.RequestError as e:
    #         print("Could not request results from Whisper API")