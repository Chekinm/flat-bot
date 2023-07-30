# DB CONFIG
DB_CONFIG = {'host': 'localhost',
             'user': 'psyco_user',
             'password': 'psyco_user_password',
             'dbname': 'hackaton_db',
             }

HELP_RESPONSE = """
/start - start working with the bot
/help - this text
/location - tell the bots where you are 
/radius - select the radius of the area around
you to search flats (in meter, default is 500)
/minarea - select mix flat area (50 sq.m. by default)
/maxarea - select max flat area (200 sq.m. by default)
/balcony  - tell me, if you wanna balcony (yes by default)
/get - show you the results based on your creteria
"""

DESCRIPTION = """
This is a bot which helps you to 
finds a flat to rent. 
It search yad2 relevant flats  around your current postions.
"""

# TELEGRAM BOT CONFIG

TOKEN_API = "----------get you own ------------------"  # telegram token