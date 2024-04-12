from typing import Union
from aiogram.filters import BaseFilter
from aiogram.types import Message


class ChatTypeFilter(BaseFilter):
    def __init__(self, chat_type: Union[str, list]):
        self.chat_type = chat_type

    async def __call__(self, message: Message) -> bool:
        """
            Check if the chat type of the message matches the specified chat type(s).

            Args:
                message (Message): The incoming message.

            Returns:
                bool: True if the chat type matches, False otherwise.
        """
        if isinstance(self.chat_type, str):
            return message.chat.type == self.chat_type
        else:
            return message.chat.type in self.chat_type