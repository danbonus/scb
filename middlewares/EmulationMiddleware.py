from vkbottle.tools.dev_tools.mini_types.bot.message import MessageMin

from vkbottle_overrides.dispatch.middlewares.abc import BaseMiddleware


class EmulationMiddleware(BaseMiddleware):
    async def pre(self, message: MessageMin, scb):
        if scb.user.is_writer:
            if "emulation_date" in scb.storage:
                await message.answer(f"🌀 | Вы находитесь в эмуляции! Дата: {scb.storage['emulation_date']}.")
