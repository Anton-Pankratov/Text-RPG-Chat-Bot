from aiogram import Bot


class ChatBot(Bot):

    def __init__(self, token):
        super().__init__(token)
        self._is_closed = False

    async def close(self, request_timeout=None):
        if not self._is_closed:
            await super().close(request_timeout=request_timeout)
            self._is_closed = True

    @property
    def is_closed(self):
        return self._is_closed
