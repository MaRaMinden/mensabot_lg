import random
import requests
from datetime import datetime

greeting_text_snippets = [
	"Ahoi ihr Landratten! Heute gibt's mal wieder leckerschmecker Essen für euch, und zwar Folgendes:",
	"Wetter is mal wieder nich so? Vorlesung auch langweilig? Immerhin - Essen gibt's:",
	"Rumort's in der Magengegend aber dein Crush ist gar nicht in der Nähe? Dann hilft vielleicht eine dieser Leckereien:",
	"Bänderer:innen haben Hunger, bitte um Sachspende:",
	"Dieses leckere Essen kannst du heute wahlweise mit Gabel oder mit Spoun essen:",
	"Na, schon hungrig? Dann snack dir doch eines der folgenden Gerichte:"
]

vegan_emojis = [
	"\U0001F331",
	"\U0001F959",
	"\U0001F9C6",
	"\U0001F957",
	"\U0001F383"
]
vegetarian_emojis = [
	"\U0001F373",
	"\U0001F30C",
	"\U0001F95A",
	"\U0001F9C0"
]
meat_emojis = [
	"\U0001F644",
	"\U0001F9A7", # makaber
	"\U0001F434",
	"\U0001F437",
	"\U0001F987",
	"\U0001F998",
	"\U0001F321", # Thermometer
	"\U0001F9F8" # Teddy
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

	return response.json()

# Get that sweet meal data
mensa_id = "140" # 101 = Braunschweig; 140 = Lüneburg
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
		string += "\nHm, hier gibt's heute nüscht.."
	else:
		for current_meal in meal_list:
			current_meal_name = current_meal['name']
			current_prices = current_meal['price']
			current_student_price = (current_prices['student'] + "€").replace(".", ",")
			"""
			current_employee_price = (current_prices['employee'] + "€").replace(".", ",")
			current_guest_price = (current_prices['guest'] + "€").replace(".", ",")
			"""
			current_meal_prices_string = "(" + current_student_price + ")"

			string = string + "\n" + current_meal_name + " " + current_meal_prices_string
	return string + "\n"

meal_message += "\n" + roll_emoji(vegan_emojis) + " *VEGAN*:"
meal_message += add_meal_strings(vegan_meals)

meal_message += "\n" + roll_emoji(vegetarian_emojis) + " *VEGATARISCH*:"
meal_message += add_meal_strings(vegetarian_meals)

meal_message += "\n" + roll_emoji(meat_emojis) + " *FLEISCH*:"
meal_message += add_meal_strings(asi_meals)

meal_message += "\nLasst's euch schmecken! \U0001F49A\nEuer Leuphana Mensabot \U0001f916"
print(meal_message)
# telegram_bot_sendtext(meal_message)