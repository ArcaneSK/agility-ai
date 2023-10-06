from enum import Enum

class MemoryScheme(Enum):
    NONE = 1
    FULL = 2
    BUFFER = 3
    SUMMARY = 4

def format_memory(messages: list, format: MemoryScheme, buffer_length=5) -> list:
    match format:
        case MemoryScheme.NONE:
            return messages[-1]

        case MemoryScheme.FULL:
            return messages
        
        case MemoryScheme.BUFFER:
            return messages[-buffer_length:]

        case MemoryScheme.SUMMARY:
            # TODO: Write memory summarization
            pass
