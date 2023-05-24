import os
import json

from config import Config
from llm.chat import Chat
from utils import slugify, clean_input
from utils.spinner import Spinner

from database import session
from database.models import *

cfg = Config()

def load_system_prompt() -> str:
    """
    Load the stored prompt from the database
    """
    with session:
        stored_prompts = Prompt.select(role="system")

        if stored_prompts:
            while(True):
                print("Please, select a stored system prompt or enter nothing to specific your own:")

                for prompt in Prompt.select(role="system"):
                    print(f"    {prompt.id}. {prompt.name}")

                prompt_selection = clean_input("Select: ")

                if prompt_selection.isnumeric():
                    selected_prompt = Prompt[prompt_selection]
                    if not selected_prompt:
                        continue
                    else:
                        return selected_prompt.text
                else:
                    break
    
    print("Please, enter your own system prompt.")
    sys_prompt = clean_input("System Prompt: ")

    to_save = clean_input("Would you like to save this prompt? [y/N]: ")

    if to_save == "y":
        new_prompt_name = clean_input("What would you like to name this prompt?: ")

        with session:
            Prompt(name=new_prompt_name, text=sys_prompt, role="system")

    return sys_prompt

def save_conversation_to_file(chat: object) -> None:
    """
    Save messages to a file. Filename is based on what GPT decides.
    """
    output_dir = os.path.join(os.getcwd(), 'saved_conversations')

    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    # Ask GPT for the best filename for this conversation
    chat.add_shadow_message("user", cfg.filename_prompt)

    try:
        with Spinner("Saving... "):
            resp = chat.complete(max_tokens=10)

            # Sanitize filename response from GPT
            filename = slugify(resp[:32]) + '.json'
            output_path = os.path.join(output_dir, filename)

            # Save conversation messages as JSON
            with open(output_path, "w") as output_file:
                json.dump(chat.messages, output_file, indent=4)

        print("Filed saved: ", filename)
    except Exception as e:
        print("Unable to save conversation. Error: ", e)

def load_conversation_from_file() -> dict:
    """
    Load message from a file in the saved conversations directory
    """
    # TODO: Load conversations from file
    pass

def main() -> None:
    """
    Main function for CLI execution
    """
    end = False
    try_again = False

    chat = Chat()
    chat.add_message("system", load_system_prompt())

    while end == False:
        if try_again == False:
            user_prompt = clean_input("Prompt: ")

            match user_prompt:
                case 'quit' | '':
                    print("Quitting...")
                    quit(0)
                case 'save':
                    save_conversation_to_file(chat)
                    continue
                case 'load':
                    continue

            chat.add_message("user", user_prompt)

        try:
            with Spinner("Thinking... "):
                resp = chat.complete(model=cfg.dumb_cli_model)

            chat.add_message("assistant", resp)

            print("Response: " + resp)

            try_again = False
        except Exception as e:
            print("The following error occured: ", e)
            desc = clean_input("Whould you like to try again? [Y/n]: ")

            if desc == "n":
                quit()
            else:
                try_again = True


if __name__ == "__main__":
    main()    