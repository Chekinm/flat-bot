Corrected English:

# Flat-bot

This is a Telegram bot designed to fetch available flats for rent around your geographical position. Unfortunately, it is not working properly at the moment because yad2, the platform it relies on, is blocking automatic requests. However, I am actively working on finding a workaround.

## To run:

1. You need to have Python installed.
2. Create a virtual environment and run the following command to install the required packages from the supplied requirements.txt file:
   ```
   pip install -r requirements.txt
   ```
3. You must have a Telegram account to run this bot.
4. Create a simple bot on Telegram and obtain a token for it. Refer to the documentation at https://core.telegram.org/bots/tutorial#obtain-your-bot-token.
5. Add your token to the botconfig1 file and then rename it to botconfig.
6. Run PostgreSQL and create a database. Specify the database environment in the botconfig file.
7. Run bot_handler.py.

## Why is it not working properly?

Unfortunately, yad2 is a very restrictive company and does not provide an open API for public access. Some people claim that you can request API access from them, but I have already tried doing so and received no response.

Without an API token, you are only allowed to make one request to yad2 per day from a specified IP address.

For demo purposes, I have added a workaround. If you receive a bad response from yad2, the application will fetch information from a previously saved file (json.data).
