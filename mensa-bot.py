import random
import requests
from datetime import datetime

# ü: "+u"\u00FC"+"
# ä: "+u"\u00E4"+"
# ö: "+u"\u00F6"+"

greeting_text_snippets = [
	"Ahoi ihr Landratten! Heute gibt's mal wieder leckerschmecker Essen f"+u"\u00FC"+"r euch, und zwar Folgendes:",
	"Wetter is mal wieder nich so? Vorlesung auch langweilig? Immerhin - Essen gibt's:",
	"Rumort's in der Magengegend aber dein Crush ist gar nicht in der N"+u"\u00E4"+"he? Dann hilft vielleicht eine dieser Leckereien:",
	"B"+u"\u00E4"+"ndernde haben Hunger, bitte um Sachspende:",
	"Dieses leckere Essen kannst du heute wahlweise mit Gabel oder mit Spoun essen:",
	"Na, schon hungrig? Dann snack dir doch eines der folgenden Gerichte:",
	"Ihr findet die Witze hier bl"+u"\u00F6"+"d? Ist wohl Geschmackssache. So wie das hier:",
	"G"+u"\u00F6"+"nnt euch die Mensung für heute:"
]

vegan_emojis = [
	u"\U0001F331",
	u"\U0001F959",
	u"\U0001F9C6",
	u"\U0001F957",
	u"\U0001F383"
]
vegetarian_emojis = [
	u"\U0001F373",
	u"\U0001F30C",
	u"\U0001F95A",
	u"\U0001F9C0"
]
meat_emojis = [
	u"\U0001F644",
	u"\U0001F9A7", # makaber
	u"\U0001F434",
	u"\U0001F437",
	u"\U0001F987",
	u"\U0001F998",
	u"\U0001F321", # Thermometer
	u"\U0001F9F8" # Teddy
]

def roll_emoji(emoji_list):
	emojicode = ""
	rand = random.randint(0, len(emoji_list) - 1)
	emojicode += emoji_list[rand]

	return emojicode

def telegram_bot_sendtext(bot_message):
	bot_token = ''
	bot_chatID = '@lg_bester_mensabot'
	send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
	response = requests.get(send_text)

	# send_animation = 'https://api.telegram.org/bot' + bot_token + '/sendAnimation?chat_id=' + bot_chatID + '&animation=https://media.giphy.com/media/l4KibK3JwaVo0CjDO/giphy.gif'
	# response2 = requests.get(send_animation)
	print(response.json())
	return response.json()

# Get that sweet meal data
mensa_id = "140" # 101 = Braunschweig; 140 = Lueneburg
tomorrow_as_iso_string = (datetime.today()).strftime('%Y-%m-%d') # + timedelta(days=1)
meals = requests.get(
	"https://sls.api.stw-on.de/v1/locations/" + mensa_id + "/menu/" + tomorrow_as_iso_string).json()['meals']

# Split by meal type
vegan_meals = list(filter(lambda current_meal: current_meal['tags']['categories'][0]['name'] == "Vegan", meals))
vegetarian_meals = list(filter(lambda current_meal: current_meal['tags']['categories'][0]['name'] == "Vegetarisch", meals))
asi_meals = list(filter(lambda current_meal: current_meal['tags']['categories'][0]['name'] != "Vegetarisch" and
											 current_meal['tags']['categories'][0]['name'] != "Vegan", meals))
meal_message = ""

# Add a random greeting
random_greeting_text = greeting_text_snippets[random.randint(0, len(greeting_text_snippets)-1)]
meal_message += random_greeting_text + "\n"

def add_meal_strings(meal_list):
	string = ""
	if len(meal_list) == 0:
		string += "\nHm, hier gibt's heute n"+u"\u00FC"+"scht.."
	else:
		previousPrice = 0.0
		for current_meal in meal_list:
			current_prices = current_meal['price']
			current_student_price = (current_prices['student'] + u"\u20AC").replace(".", ",")
			current_meal_name = current_meal['name']
			current_price_as_float = float(current_prices['student'])
			if(current_price_as_float < 2 ): # Check if it's just a sidedish
				current_meal_name = "_" + current_meal_name + "_" # Make italic
				if previousPrice > 2: # Add divider if category is not only side-dishes
					string += "\n--------"
			previousPrice = current_price_as_float
			current_meal_prices_string = "(" + current_student_price + ")"

			string = string + "\n" + current_meal_name + " " + current_meal_prices_string
	return string + "\n"

meal_message += "\n" + roll_emoji(vegan_emojis) + " *VEGAN*:"
meal_message += add_meal_strings(vegan_meals)

meal_message += "\n" + roll_emoji(vegetarian_emojis) + " *VEGETARISCH*:"
meal_message += add_meal_strings(vegetarian_meals)

meal_message += "\n" + roll_emoji(meat_emojis) + " *Totes Tier*:"
meal_message += add_meal_strings(asi_meals)

meal_message += "\nLasst's euch schmecken!" + u"\U0001F49A" + "\nEuer Leuphana Mensabot" + u"\U0001f916"
# print(meal_message)
telegram_bot_sendtext(meal_message)