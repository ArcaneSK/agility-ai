from modules import ChatModuleInterface
import openai

class OpenAIModule(ChatModuleInterface):
    def __init__(self, api_key):
        openai.api_key = api_key

    def get_response(self, messages):
        resp = openai.ChatCompletion.create(
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
            messages = formatted_messages+self.shadow_messages
        )

        self.shadow_messages = [] # clear shadow messages

        return resp['choices'][0]['message']['content']