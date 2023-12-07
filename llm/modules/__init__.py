
class ChatModuleInterface:
    def load_model(self):
        raise NotImplementedError

    def get_response(self, messages, max_tokens):
        raise NotImplementedError