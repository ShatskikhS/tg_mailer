from typing import List
from config_data import MESSAGE_MAX_LENGTH

def split_message(text: str, max_length: int = MESSAGE_MAX_LENGTH) -> List[str]:
    return [text[i:i + max_length] for i in range(0, len(text), max_length)]