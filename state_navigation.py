from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from dataclasses import make_dataclass
from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    KeyboardButton
)


class Form(StatesGroup):
    state_full_name = State()
    state_phone_number = State()
    state_email = State()
    state_room_type = State()
    state_guests = State()
    state_arrival_date = State()
    state_departure_date = State()
    state_confirmation = State()


StateData = make_dataclass(  # dataclass that holds information that are included in each state
    "StateData",
    ["state_name",  # state's variable name example: state1, state2 ... state8
     "state_memory_name",
     "state_question",
     "state_reply_buttons"]  # list[list[KeyboardButton]] # state's keyboard reply buttons
)

# Individual bot buttons

button_go_back = KeyboardButton(text="Go Back")
button_cancel = KeyboardButton(text="Cancel")
button_yes_book = InlineKeyboardButton(text="Yes", callback_data="yes")
button_no_book = InlineKeyboardButton(text="No", callback_data="no")
button_standard_room = KeyboardButton(text="Standard Room")
button_family_room = KeyboardButton(text="Family Room")
button_private_room = KeyboardButton(text="Private Room")
button_female_room = KeyboardButton(text="Female Room")
button_male_room = KeyboardButton(text="Male Room")
button_confirm = KeyboardButton(text="Confirm")

buttons_book = [[  # buttons to help the user's interest of booking a room.
    button_no_book, button_yes_book
]]
buttons_full_name = [[
    button_cancel
]]
buttons_phone_number = [[  # reply keyboard buttons that go with phone number state
    button_go_back, button_cancel
]]
buttons_email = [[
    button_go_back, button_cancel
]]
buttons_room_type = [  # inline buttons that go into room_type state
    [button_standard_room, button_family_room, button_private_room, button_female_room, button_male_room],
    [button_cancel, button_go_back]
]
buttons_guests = [[
    button_cancel, button_go_back
]]
buttons_arrival_date = [[
    button_cancel, button_go_back
]]
buttons_departure_date = [[
    button_cancel, button_go_back
]]
buttons_confirmation = [[
    button_cancel, button_confirm
]]

statedata_full_name = StateData("Form.state_full_name", "full_name", "write your full name?", buttons_full_name)
statedata_phone_number = StateData("Form.state_phone_number", "phone_number", "please write your phone number. Phone numbers should follow the standard +000-000-0000 format.",
                                   buttons_phone_number)
statedata_email = StateData("Form.state_email", "email", "write your email.", buttons_email)
statedata_room_type = StateData("Form.state_room_type", "room_type", "Select the type of room you want?",
                                buttons_room_type)
statedata_guests = StateData("Form.state_guests", "guests", "Please tell me the number of guests.",
                             buttons_guests)
statedata_arrival_date = StateData("Form.state_arrival_date", "arrival_date", "please let let me know your date of arrival. date format should be DD-MM-YYYY",
                                   buttons_arrival_date)
statedata_departure_date = StateData("Form.state_departure_date", "departure_date", "please write your departure date. date format should be DD-MM-YYYY",
                                     buttons_departure_date)
statedata_confirmation = StateData("Form.state_full_name", "confirm", "Confirm?",
                                   buttons_confirmation)

async def previous_state(current_state: State):
    states_list = [(statedata_full_name,Form.state_full_name),
                   (statedata_phone_number,Form.state_phone_number),
                   (statedata_email,Form.state_email),
                   (statedata_room_type,Form.state_room_type),
                   (statedata_guests,Form.state_guests),
                   (statedata_arrival_date,Form.state_arrival_date),
                   (statedata_departure_date,Form.state_departure_date),
                   (statedata_confirmation,Form.state_confirmation)
                   ]

    match_statelist_element = [(d,s) for d,s in states_list if s==current_state] #current statedata and state
    state_data, state =match_statelist_element[0][0] , match_statelist_element[0][1]
    current_state_index = states_list.index((state_data,state))
    previous_state_index = current_state_index-1
    previous_state_data,previous_state=states_list[previous_state_index]
    return (previous_state_data,previous_state)
