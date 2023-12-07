from llm.modules import ChatModuleInterface
import openai

class OpenAIModule(ChatModuleInterface):
    MODE_SMART = 1
    MODE_DUMB  = 2

    def __init__(self, cfg):
        if not cfg.open_api_key:
            raise ValueError("OpenAI API Key enviroment variable (OPENAI_API_KEY) is not set.")
        
        openai.api_key = cfg.open_api_key

        self.smart_model_name = cfg.smart_cli_model
        self.dumb_model_name = cfg.dumb_cli_model

    def load_model(self):
        pass

    def get_response(self, messages, max_tokens=800, mode=MODE_SMART):
        resp = openai.ChatCompletion.create(
            model=self.smart_model_name if mode == self.MODE_SMART else self.dumb_model_name,
            max_tokens=max_tokens,
            temperature=1.2,
            messages = messages
        )

        return resp['choices'][0]['message']['content']