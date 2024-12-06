import asyncio
import subprocess

from components import chat_bot, dispatcher_chat_bot
from commands.commands import set_commands
from db import db

async def shutdown(bot, db_connection):
    if not bot.is_closed:
        await bot.session.close()
    if db_connection:
        await db_connection.close_db()

async def main():
    await db.init_db()
    await set_commands(chat_bot)

    try:
        await dispatcher_chat_bot.start_polling(chat_bot)
        subprocess.run(['python', 'components.py'])
    except (KeyboardInterrupt, SystemExit):
        pass
    finally:
        await shutdown(chat_bot, db)

if __name__ == '__main__':
    asyncio.run(main())


#async def main_telethon():
#    await client_telethon.start()
#    await fetch_messages_telethon(chat_id=, topic_id=)

# with client_telethon:
#    client_telethon.loop.run_until_complete(main_telethon())