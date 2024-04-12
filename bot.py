import asyncio
from loader import bot
from handlers import start, admin_funcs
from aiogram import Dispatcher
from utils.set_bot_commands import set_default_commands


async def main() -> None:
    """
        The main entry point for the bot's execution.

        This function initializes the dispatcher with memory storage, sets default commands,
        includes routers for different functionalities, deletes any pending webhook updates,
        and starts polling for updates from the bot.

        Returns:
            None
    """

    dp = Dispatcher()
    await set_default_commands()

    dp.include_router(start.router)
    dp.include_router(admin_funcs.router)



    # Delete any pending updates from the webhook
    await bot.delete_webhook(drop_pending_updates=True)

    # Start polling for updates using the dispatcher
    await dp.start_polling(bot)


if __name__ == "__main__":
    # Run the main function using the asyncio event loop
    asyncio.run(main())
