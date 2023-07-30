from aiogram import Bot, Dispatcher, types, utils
from aiogram.types import (Message,
                           ReplyKeyboardMarkup,
                           KeyboardButton,
                           )
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from botconfig import TOKEN_API, HELP_RESPONSE, DB_CONFIG
from api_yad2 import get_yad2_data
from dbmanager import DBconnect

# initialize DB
db = DBconnect(**DB_CONFIG)

# initalize bot
bot = Bot(token=TOKEN_API)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer("Hi! I'm a bot. I can search yad2 around you and "
                         "show you some flats you may intrested in. "
                         "Please type /help to see the command list.")


@dp.message_handler(commands=['help'])
async def help_msg(message: types.Message):
    await message.answer(HELP_RESPONSE)


# this two functions work with requested location
# locatiion only send can be send as ReplyKeyboardMarkup
async def request_location(message: Message):
    button = KeyboardButton(text="Send location", request_location=True)
    markup = ReplyKeyboardMarkup(resize_keyboard=True).add(button)
    await message.answer("Please share your location:", reply_markup=markup)


# parse location to coordinates
# write it to database with user ID
async def get_location(message: Message):
    location = message.location
    latitude = location.latitude
    longitude = location.longitude
    # write to db user_id and his GPS coordinates
    await db.add_user(message.from_user.id)
    await db.db_change_coordinates(latitude, longitude, message.from_user.id)
    print(latitude, longitude,  message.from_user.id)
    await message.answer("Now, select radius to search. /radius")


@dp.message_handler(commands=['location'])
async def location(message: types.Message):
    await request_location(message)


@dp.message_handler(commands=['radius'])
async def radius(message: types.Message):
    ib = []
    for i in range(100, 2001, 100):
        ib.append(InlineKeyboardButton(text=f'{i}',
                                       callback_data=i))

    ikb = InlineKeyboardMarkup(row_width=5)
    ikb.add(*ib)
    await bot.send_message(chat_id=message.from_user.id,
                           text='Select radius around you to search',
                           reply_markup=ikb,
                           )


@dp.message_handler(commands=['maxarea'])
async def maxarea(message: types.Message):
    ib = []
    for i in range(100, 300, 10):
        ib.append(InlineKeyboardButton(text=f'{i}',
                  callback_data=i),
                  )

    ikb = InlineKeyboardMarkup(row_width=5)
    ikb.add(*ib)
    await bot.send_message(chat_id=message.from_user.id,
                           text='Select maximum area of the flat',
                           reply_markup=ikb)


@dp.message_handler(commands=['minarea'])
async def minarea(message: types.Message):
    ib = []
    for i in range(10, 201, 10):
        ib.append(InlineKeyboardButton(text=f'{i}',
                  callback_data=i))

    ikb = InlineKeyboardMarkup(row_width=5)
    ikb.add(*ib)
    await bot.send_message(chat_id=message.from_user.id,
                           text='Select minimum area of the flat',
                           reply_markup=ikb)


@dp.message_handler(commands=['balcony'])
async def balcony(message: types.Message):
    ib = []
    ib.append(InlineKeyboardButton(text='YES',
                                   callback_data=f'{1}'))
    ib.append(InlineKeyboardButton(text='NO',
                                   callback_data=f'{0}'))

    ikb = InlineKeyboardMarkup(row_width=5)
    ikb.add(*ib)
    await bot.send_message(chat_id=message.from_user.id,
                           text='Do you wanna a balcony',
                           reply_markup=ikb)


@dp.callback_query_handler()
async def callback_handler(callback: types.CallbackQuery):

    if 'minimum' in callback.message.text:
        query = ('min_square', callback.data)
        await db.change_properties(query, callback.from_user.id)

    if 'maximum' in callback.message.text:
        query = ('max_square', callback.data)
        await db.change_properties(query, callback.from_user.id)

    if 'radius' in callback.message.text:
        query = ('radius', callback.data)
        await db.change_properties(query, callback.from_user.id)

    if 'balcony' in callback.message.text:
        if callback.data == '0':
            balc = False
        else:
            balc = True
        query = ('balcony', balc)  # can be a bug check
        await db.change_properties(query, callback.from_user.id)

    await bot.send_message(chat_id=callback.from_user.id,
                           text=("Continue configuration or get you flats"
                                 "\n/minarea\n/maxarea "
                                 "\n/balcony \n/radius \n/get  "),
                           )


@dp.message_handler(content_types=['location'])
async def handle_location(message: types.Message):
    await get_location(message)


@dp.message_handler(commands=['get'])
async def get(message: types.Message):

    """this function call get_request_data to get data from DB to pass it
    to search in yad2
    it get back searches   from yad and returns you nicel frmatted results """

    request_config = await db.get_request_data(str(message.from_user.id))
    resp_dict = await get_yad2_data(request_config)
    ind = 0
    while ind < 6 and ind < len(resp_dict['feed']["feed_items"]):
        # FIXME get 6 flats, probably good idea to add this control to
        # configuration as it user preference
        try:
            url = f"https://www.yad2.co.il/item/{resp_dict['feed']['feed_items'][ind]['link_token']}"
            rooms = f"{resp_dict['feed']['feed_items'][ind]['row_4'][0]['value']} rooms'"
            area = f"{resp_dict['feed']['feed_items'][ind]['row_4'][2]['value']} sq. meters"
            price = resp_dict['feed']['feed_items'][ind]['price']
            images = resp_dict['feed']['feed_items'][ind]['images_urls']
            msg = f"{rooms}.\n{area} \n{price}\n{url}"
            images = resp_dict['feed']['feed_items'][ind]['images_urls']
            if len(images) > 1:
                m = []
                try:
                    for _ in images:
                        m.append(types.InputMediaPhoto(_))

                    await bot.send_media_group(chat_id=message.from_user.id,
                                               media=m,
                                               )
                except utils.exceptions.ValidationError as error:
                    print("Not ehough photo, check link on yad2 site\n", error)
            await message.answer(msg)

        except KeyError:
            print('Key error. Missed info in yad2')
        except IndexError:
            print('Index error. Missed info in yad2')

        ind += 1
    await message.answer('Whould you like to make another search?')
    await message.answer(HELP_RESPONSE)


@dp.message_handler(commands=['print'])
async def print_msg(message: types.Message):
    res = await db.get_request_data(str(message.from_user.id))
    await message.answer(res)


if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dispatcher=dp, skip_updates=True)
