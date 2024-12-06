import asyncio
import socket

from aiogram.client.session import aiohttp


class ChatBotTaskManager:

    def __init__(self):
        self.running_task = None
        self.task_timer = 5  # 60 * 60
        self.timeout = 5

    async def run_task(self, func, *args, **kwargs):
        while True:
            try:
                if asyncio.iscoroutinefunction(func):
                    await func(*args, **kwargs)
                else:
                    await func(*args, **kwargs)
                await asyncio.sleep(self.task_timer)
            except (aiohttp.ClientError, socket.gaierror) as e:
                print(f"Сетевая ошибка: {e}. Перезапуск через 5 секунд.")
                await asyncio.sleep(5)
            except asyncio.TimeoutError as e:
                print(f"Ошибка таймаута: {e}. Перезапуск через 5 секунд.")
                await asyncio.sleep(5)
            except asyncio.CancelledError:
                print("Задача была отменена.")
                break
            except Exception as e:
                print(f"Неизвестная ошибка: {e}. Перезапуск через 10 секунд.")
                await asyncio.sleep(10)

    async def create_task(self, func, *args, **kwargs):
        loop = asyncio.get_running_loop()
        self.running_task = loop.create_task(self.run_task(func, *args, **kwargs))

    async def cancel_task(self):
        if self.running_task:
            self.running_task.cancel()
            self.running_task = None

    def is_task_running(self) -> bool:
        return self.running_task is not None and not self.running_task.done()