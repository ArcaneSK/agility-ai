from enum import Enum

class MemoryScheme(Enum):
    NONE = 1
    FULL = 2
    SUMMARY = 3

def format_memory(messages: list, format: MemoryScheme) -> list:
    match format:
        case MemoryScheme.NONE:
            return messages[-1]

        case MemoryScheme.FULL:
            return messages

        case MemoryScheme.SUMMARY:
            # TODO: Write memory summarization
            pass
