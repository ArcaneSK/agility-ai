import os
from dotenv import load_dotenv

load_dotenv()

class Config():
    """
    Configuration class that store and organizes all script options
    """

    def __init__(self) -> None:
        """ 
        Initialize the Config class
        """
        self.database_engine = os.getenv("DATABASE_ENGINE", "sqlite")
        self.database_name = os.getenv("DATABASE_NAME", "database")

        self.open_api_key = os.getenv("OPENAI_API_KEY")
        self.smart_cli_model = "gpt-4"
        self.dumb_cli_model = "gpt-3.5-turbo"
        self.filename_prompt = "What's a good filename for this conversation, based on user " \
            "messages only? Exclude file extension and system messages. Filename < 32 characters."
        self.command_prompt = "If there is something "
