import unicodedata
import re

from rich.console import Console
from rich.text import Text

def slugify(value, allow_unicode=False):
    """
    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value)
    return re.sub(r'[-\s]+', '-', value)

def clean_input(prompt: str='', style=None):
    console = Console()

    try:
        prompt_text = Text(text=prompt, style=style)
        return console.input(prompt_text)
    except KeyboardInterrupt:
        console.print("\nKeyboard interrupt issued", style="orange3")
        print("Quitting...")
        exit(0)