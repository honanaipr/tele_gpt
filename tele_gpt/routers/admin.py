from aiogram import Router
from aiogram.enums import InlineQueryResultType
from aiogram.filters import Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.methods import EditMessageText
from aiogram.types import (
    ChosenInlineResult,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InlineQuery,
    InlineQueryResultArticle,
    InputTextMessageContent,
    Message,
)
from aiogram_dialog import DialogManager, StartMode
from loguru import logger

from tele_gpt import utils
from tele_gpt.exceptions import DBError
from tele_gpt.loader import bot
from tele_gpt.states import AdminSG

admin_router = Router()


@admin_router.message(Command("get_users"))
async def command_start_handler(message: Message, command: CommandObject):
    if not message.from_user:
        return
    if not await utils.is_admin(message.from_user.id):
        logger.warning("Someone non admin try to use " + (message.text or ""))
        return
    try:
        users = await utils.get_users()
    except DBError as e:
        logger.exception(e)
    if not command.args:
        answer = (
            "\n".join(
                [
                    "Name: " + str(user.name) + "\n"
                    "Id: " + str(user.id) + "\n"
                    "Is admin: " + str(user.is_admin) + "\n\n"
                    for user in users
                ]
            )
            or "No users yet"
        )
        await message.answer(answer)
    else:
        await message.answer("Not realized for " + command.args)


@admin_router.message(Command("add_admin"))
async def command_add_admin_handler(
    message: Message,
    command: CommandObject,
    dialog_manager: DialogManager,
    state: FSMContext,
):
    if not message.from_user:
        return
    if not await utils.is_admin(message.from_user.id):
        logger.warning("Someone non admin try to user ", message.text)
        return
    await dialog_manager.start(AdminSG.add_admin)
