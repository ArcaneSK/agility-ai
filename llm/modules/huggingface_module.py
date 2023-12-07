from llm.modules import ChatModuleInterface

from config import Config

class HuggingFaceModule(ChatModuleInterface):

    def __init__(self):
        self.cfg = Config()

    def load_model():
        pass # TODO: add model loader

    def get_response(self, messages, max_tokens=800):
        pass # TODO: add completion 