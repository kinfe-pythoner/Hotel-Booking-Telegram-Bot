import os
import re
from aiogram import Bot, Dispatcher, Router, F
from aiogram.types import (
    Message, CallbackQuery, InlineQuery, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove
)
from aiogram.filters import CommandStart,Command
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import State
from dataclasses import make_dataclass
from state_navigation import Form, StateData
from aiogram.enums.parse_mode import ParseMode
from dotenv import load_dotenv
import sys
import os
import asyncio
import state_navigation
import logging

load_dotenv()
bot=Bot(token=os.getenv("TOKEN")) #parse_mode=ParseMode.HTML
router=Router()
dp=Dispatcher()
dp.include_router(router)

@router.message(CommandStart())
async def command_start(message: Message, state:FSMContext) -> None:
    await message.answer(
        """
        Hello, I am a Homeland hotel's chatbot. I can help you book a room on our hotel. Do you want to book a room?"
        """,
        reply_markup = InlineKeyboardMarkup(inline_keyboard=state_navigation.buttons_book,resize_keyboard=True)
    )

@router.callback_query()
async def start_book(call: CallbackQuery, state: FSMContext) -> None:
    if call.data.lower()=="no":
        await state.clear()
        await call.message.answer(
            """
            Process Canceled.
            """,
            reply_markup=ReplyKeyboardRemove()
        )
    else:
        await state.set_state(Form.state_full_name)
        await call.message.answer(
            """
            Greate, In order to proceed with the booking process we will ask you some personal information. \nplease Provide us your full name. 
            """, reply_markup=ReplyKeyboardMarkup(keyboard=state_navigation.buttons_full_name, resize_keyboard=True)
        )

@router.message(Form.state_full_name)
async def handle_full_name(message: Message, state: FSMContext) -> None:
    if message.text.lower()=="cancel":
        await cancel_process(message,state)
    elif message.text.lower()=="go back":
        await go_back(message,state)
    else:
        await state.update_data(full_name=message.text)
        await state.set_state(Form.state_phone_number)
        await message.answer(
            """
            please write your phone number. Phone numbers should follow the standard format. (start with +)
            """,
            reply_markup=ReplyKeyboardMarkup(keyboard=state_navigation.buttons_phone_number, resize_keyboard=True)
        )
@router.message(Form.state_phone_number)
async def handle_phone_number(message: Message, state: FSMContext) -> None:
    if message.text.lower()=="cancel":
        await cancel_process(message,state)
    elif message.text.lower()=="go back":
        await go_back(message,state)
    else:
        if re.fullmatch("^(\+\d{1,3})?\s?\(?\d{1,4}\)?[\s.-]?\d{3}[\s.-]?\d{4}$",message.text):
            await state.update_data(phone_number=message.text)
            await state.set_state(Form.state_email)
            await message.answer(
                """
                Please write your email.
                """,
                reply_markup=ReplyKeyboardMarkup(keyboard=state_navigation.buttons_email, resize_keyboard=True)
            )
        else:
            await message.answer(
                """
                Please write a correct phone numbe.
                """,
                reply_markup=ReplyKeyboardMarkup(keyboard=state_navigation.buttons_phone_number, resize_keyboard=True)
            )

@router.message(Form.state_email)
async def handle_email(message: Message, state: FSMContext) -> None:
    if message.text.lower()=="cancel":
        await cancel_process(message,state)
    elif message.text.lower()=="go back":
        await go_back(message,state)
    else:
        if re.fullmatch("^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$",message.text):
            await state.update_data(email=message.text)
            await state.set_state(Form.state_room_type)
            await message.answer(
                """
                Please select the type of room you want.
                """,
                reply_markup=ReplyKeyboardMarkup(keyboard=state_navigation.buttons_room_type, resize_keyboard=True)
            )
        else:
            await message.answer(
                """
                The email you sent looks invalid. please write a correct email address.
                """,
                reply_markup=ReplyKeyboardMarkup(keyboard=state_navigation.buttons_email, resize_keyboard=True)
            )

@router.message(Form.state_room_type)
@router.message(Command(commands=["standard room","family room","private room","female room","male room","cancel"]))
async def handle_room_type(message: Message, state: FSMContext)->None:
    if message.text.lower()=="cancel":
        await cancel_process(message,state)
    elif message.text.lower()=="go back":
        await go_back(message,state)
    else:
        await state.update_data(room_type=message.text)
        await state.set_state(Form.state_guests)
        await message.answer(
            """
            How many Guests do you have?
            """,
            reply_markup=ReplyKeyboardMarkup(keyboard=state_navigation.buttons_guests, resize_keyboard=True)
        )

@router.message(Form.state_guests)
async def handle_guests(message:Message, state:FSMContext) -> None:
    if message.text.lower()=="cancel":
        await cancel_process(message,state)
    elif message.text.lower()=="go back":
        await go_back(message,state)
    else:
        await state.update_data(guests=message.text)
        await state.set_state(Form.state_arrival_date)
        await message.answer(
            """
            please let let me know your date of arrival. date format should be DD-MM-YYYY.
            """,
            reply_markup=ReplyKeyboardMarkup(keyboard=state_navigation.buttons_arrival_date, resize_keyboard=True)
        )

@router.message(Form.state_arrival_date)
async def handle_arrival_date(message: Message, state: FSMContext) ->None:
    if message.text.lower()=="cancel":
        await cancel_process(message,state)
    elif message.text.lower()=="go back":
        await go_back(message,state)
    else:
        if re.fullmatch("^[0-9]{1,2}\\/[0-9]{1,2}\\/[0-9]{4}$",message.text):
            await state.update_data(arrival_date=message.text)
            await state.set_state(Form.state_departure_date)
            await message.answer(
                """
                please let let me know your departure date.
                """,
                reply_markup=ReplyKeyboardMarkup(keyboard=state_navigation.buttons_departure_date, resize_keyboard=True)
            )
        else:
            await message.answer(
                """
                You wrote an invalid date, please write a correct date.
                """,
                reply_markup=ReplyKeyboardMarkup(keyboard=state_navigation.buttons_arrival_date, resize_keyboard=True)
            )

@router.message(Form.state_departure_date)
async def handle_departure_date(message: Message, state: FSMContext) ->None:
    if message.text.lower()=="cancel":
        await cancel_process(message,state)
    elif message.text.lower()=="go back":
        await go_back(message,state)
    else:
        if re.fullmatch("^[0-9]{1,2}\\/[0-9]{1,2}\\/[0-9]{4}$",message.text):
            await state.update_data(departure_date=message.text)
            data = await state.get_data()
            client_info = []
            for key, value in data.items():
                client_info.append(f"{key}: {value}")
            await state.set_state(Form.state_confirmation)
            client_info = "\n".join(client_info)
            await message.answer(
                f"""
                Information Collected:\n{client_info}\nConfirm room reservation?
                """,
                reply_markup=ReplyKeyboardMarkup(keyboard=state_navigation.buttons_confirmation, resize_keyboard=True)
            )
        else:
            await message.answer(
                f"""
                you provided invalid departure date.please provide a valid date. 
                """,
                reply_markup=ReplyKeyboardMarkup(keyboard=state_navigation.buttons_departure_date, resize_keyboard=True)
            )

@router.message(Form.state_confirmation)
@router.message(Command(commands=["confirm"]))
async def handle_confirmation(message: Message,state: FSMContext) -> None:
    if message.text.lower() == "cancel":
        await cancel_process(message,state)
    elif message.text.lower()=="confirm":
        await state.update_data(departure_date=message.text)
        await message.answer(
            """
            Room Reserved.
            """,
            reply_markup=ReplyKeyboardRemove()
        )

async def go_back(message:Message , state: FSMContext) -> None:
    current_state = await state.get_state()
    previous_statedata , previous_state = await state_navigation.previous_state(current_state)
    await state.set_state(previous_state)
    await message.answer(
        f"""
        {previous_statedata.state_question}
        """,
        reply_markup=ReplyKeyboardMarkup(keyboard=previous_statedata.state_reply_buttons,resize_keyboard=True)
    )

async def cancel_process(message:Message,state:FSMContext) -> None:
    await state.clear()
    await message.answer(
        """
        Process Canceled.
        """,
        reply_markup=ReplyKeyboardRemove()
    )

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    #logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    print("Telegram bot started.")
    asyncio.run(main())