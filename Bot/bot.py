"""Base Bot with minimal error handling

Raises:
    exception: None
"""
import logging as log

import hikari
import lightbulb
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pytz import timezone, utc
from config import Config#pylint: disable=E0401


def app() -> None:
    """Function to Setup and Run the Bot

    Raises:
        exception: NotOwner, CommandNotFound, NotEnoughArguments
    """

    bot = lightbulb.BotApp(token=Config.TOKEN,
                           prefix='-',
                           case_insensitive_prefix_commands=True
                           )

    scheduler = AsyncIOScheduler()

    @bot.listen(lightbulb.CommandErrorEvent)
    async def on_error(event: lightbulb.CommandErrorEvent) -> None:

        exception = event.exception

        if isinstance(exception, lightbulb.NotOwner):
            await event.context.respond("You are not the owner of this bot.")
        elif isinstance(exception, lightbulb.CommandNotFound):
            await event.context.respond("I'm sorry, but I cannot find that command.")
        elif isinstance(exception, lightbulb.NotEnoughArguments):
            await event.context.respond("You have not input all the required arguments.")
        else:
            raise exception

    @bot.listen(hikari.StartingEvent)
    async def on_starting(event: hikari.StartingEvent) -> None:
        bot.load_extensions_from("extensions")

    @bot.listen(hikari.StartedEvent)
    async def on_started(event: hikari.StartedEvent) -> None:
        scheduler.configure(timezone(utc))
        scheduler.start()
        log.info('BOT READY!')

    @bot.listen(hikari.StoppingEvent)
    async def on_stopping(event: hikari.StoppingEvent) -> None:
        scheduler.shutdown()
        log.info('BOT IS DEAD!')

    bot.run(activity=hikari.Activity(
            name=f"-help|Version={Config.VERSION}",
            type=hikari.ActivityType.WATCHING,
            )
            )
