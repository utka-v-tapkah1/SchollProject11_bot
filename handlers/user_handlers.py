import logging

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from services.food import get_food_breakfast, get_food_obed
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon.lexicon import LEXICON_RU
from keyboards.main_kb import create_menu_kb, create_back_to_menu_kb
from datetime import datetime

router = Router()

logger = logging.getLogger(__name__)


@router.message(Command(commands=["start"]))
async def process_start_command(message: Message):
    await message.answer(text=LEXICON_RU['/start'],
                         reply_markup=create_menu_kb())


@router.callback_query(F.data == '/start')
async def process_start_command(callback: CallbackQuery):
    await callback.message.answer(text=LEXICON_RU['/start'],
                                  reply_markup=create_menu_kb())
    await callback.answer()


@router.message(Command(commands=['official_site']))
async def process_site(message: Message):
    await message.answer(text=LEXICON_RU['official_site'])


@router.callback_query(F.data == 'official_site')
async def process_site(callback: CallbackQuery):
    await callback.message.answer(text=LEXICON_RU['official_site'])
    await callback.answer()


@router.message(Command(commands=['breakfast']))
async def process_breakfast(message: Message):
    mess = await message.answer(LEXICON_RU['wait'])
    brk = datetime.now().strftime("%d.%m.%Y") + '\n' + await get_food_breakfast()

    await mess.edit_text(brk,
                         reply_markup=create_back_to_menu_kb())


@router.callback_query(F.data == 'breakfast')
async def process_breakfast(callback: CallbackQuery):
    mess = await callback.message.answer(LEXICON_RU['wait'])
    brk = datetime.now().strftime("%d.%m.%Y") + '\n' + await get_food_breakfast()

    await mess.edit_text(brk,
                         reply_markup=create_back_to_menu_kb())
    await callback.answer()


@router.message(Command(commands=['obed']))
async def process_breakfast(message: Message):
    mess = await message.answer(LEXICON_RU['wait'])
    obed = datetime.now().strftime("%d.%m.%Y") + '\n' + await get_food_obed()

    await mess.edit_text(obed,
                         reply_markup=create_back_to_menu_kb())


@router.callback_query(F.data == 'obed')
async def process_obed(callback: CallbackQuery):
    mess = await callback.message.answer(LEXICON_RU['wait'])
    obed = datetime.now().strftime("%d.%m.%Y") + '\n' + await get_food_obed()

    await mess.edit_text(obed,
                         reply_markup=create_back_to_menu_kb())
    await callback.answer()
