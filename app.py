import requests
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler
#from telegram.ext import Application
import os

PORT = int(os.environ.get("PORT", "8443"))
TOKEN = "5906044284:AAFvXhElWvNLFBbnLgn8NfRc95dB0g5jzjU"

class area:
    location = 0
    name = 'Ang Mo Kio'
    status = 'weather'

Locations = {
    '0':'Ang Mo Kio',
    '1':'Bedok',
    '2':'Bishan',
    '3':'Boon Lay',
    '4':'Bukit Batok',
    '5':'Bukit Merah',
    '6':'Bukit Panjang',
    '7':'Bukit Timah',
    '8':'Central Water Catchment',
    '9':'Changi',
    '10':'Choa Chu Kang',
    '11':'Clementi',
    '12':'City',
    '13':'Geylang',
    '14':'Hougang',
    '15':'Jalan Bahar',
    '16':'Jurong East',
    '17':'Jurong Island',
    '18':'Jurong West',
    '19':'Kallang',
    '20':'Lim Chu Kang',
    '21':'Mandai',
    '22':'Marine Parade',
    '23':'Novena',
    '24':'Pasir Ris',
    '25':'Paya Lebar',
    '26':'Pioneer',
    '27':'Pulau Tekong',
    '28':'Pulau Ubin',
    '29':'Punggol',
    '30':'Queenstown',
    '31':'Seletar',
    '32':'Sembawang',
    '33':'Sengkang',
    '34':'Sentosa',
    '35':'Serangoon',
    '36':'Southern Islands',
    '37':'Sungei Kadut',
    '38':'Tampines',
    '39':'Tanglin',
    '40':'Tengah',
    '41':'Toa Payoh',
    '42':'Tuas',
    '43':'Western Islands',
    '44':'Western Water Catchment',
    '45':'Woodlands',
    '46':'Yishun'
}

async def start(update: Update, context:CallbackContext ) -> None:
    await update.message.reply_text("Choose the region you want to keep track of and I'll notify you when the weather forecast changes!")


async def set_command(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton('Ang Mo Kio', callback_data='0'),InlineKeyboardButton('Bedok', callback_data='1'),InlineKeyboardButton('Bishan', callback_data='2')],
        [InlineKeyboardButton('Boon Lay', callback_data='3'),InlineKeyboardButton('Bukit Batok', callback_data='4'),InlineKeyboardButton('Bukit Merah', callback_data='5')],
        [InlineKeyboardButton('Bukit Panjang', callback_data='6'),InlineKeyboardButton('Bukit Timah', callback_data='7'),InlineKeyboardButton('Central Water Catchment', callback_data='8')],
        [InlineKeyboardButton('Changi', callback_data='9'),InlineKeyboardButton('Choa Chu Kang', callback_data='10'),InlineKeyboardButton('Clementi', callback_data='11')],
        [InlineKeyboardButton('City', callback_data='12'),InlineKeyboardButton('Geylang', callback_data='13'),InlineKeyboardButton('Hougang', callback_data='14')],
        [InlineKeyboardButton('Jalan Bahar', callback_data='15'),InlineKeyboardButton('Jurong East', callback_data='16'),InlineKeyboardButton('Jurong Island', callback_data='17')],
        [InlineKeyboardButton('Jurong West', callback_data='18'),InlineKeyboardButton('Kallang', callback_data='19'),InlineKeyboardButton('Lim Chu Kang', callback_data='20')],
        [InlineKeyboardButton('Mandai', callback_data='21'),InlineKeyboardButton('Marine Parade', callback_data='22'),InlineKeyboardButton('Novena', callback_data='23')],
        [InlineKeyboardButton('Pasir Ris', callback_data='24'),InlineKeyboardButton('Paya Lebar', callback_data='25'),InlineKeyboardButton('Pioneer', callback_data='26')],
        [InlineKeyboardButton('Pulau Tekong', callback_data='27'),InlineKeyboardButton('Pulau Ubin', callback_data='28'),InlineKeyboardButton('Punggol', callback_data='29')],
        [InlineKeyboardButton('Queenstown', callback_data='30'),InlineKeyboardButton('Seletar', callback_data='31'),InlineKeyboardButton('Sembawang', callback_data='32')],
        [InlineKeyboardButton('Sengkang', callback_data='33'),InlineKeyboardButton('Sentosa', callback_data='34'),InlineKeyboardButton('Serangoon', callback_data='35')],
        [InlineKeyboardButton('Southern Islands', callback_data='36'),InlineKeyboardButton('Sungei Kadut', callback_data='37'),InlineKeyboardButton('Tampines', callback_data='38')],
        [InlineKeyboardButton('Tanglin', callback_data='39'),InlineKeyboardButton('Tengah', callback_data='40'),InlineKeyboardButton('Toa Payoh', callback_data='41')],
        [InlineKeyboardButton('Tuas', callback_data='42'),InlineKeyboardButton('Western Islands', callback_data='43'),InlineKeyboardButton('Western Water Catchment', callback_data='44')],
        [InlineKeyboardButton('Woodlands', callback_data='45'),InlineKeyboardButton('Yishun', callback_data='46')]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Please choose:", reply_markup=reply_markup)

    current_jobs = context.job_queue.get_jobs_by_name(str(update.effective_message.chat_id))
    if current_jobs:
        for job in current_jobs:
            job.schedule_removal()



async def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()
    area.location = int(query.data)
    area.name = Locations[query.data]
    await query.edit_message_text(text=f"Selected option: {area.name}")

    chat_id = update.effective_message.chat_id
    due = 0
    context.job_queue.run_once(alert, due, chat_id=chat_id, name=str(chat_id), data=due)

    chat_id = update.effective_message.chat_id
    due = 900 #15 minutes
    context.job_queue.run_repeating(alert, due, chat_id=chat_id, name=str(chat_id), data=due)


async def alert(context: CallbackContext) -> None:
    job = context.job
    response = requests.get("https://api.data.gov.sg/v1/environment/2-hour-weather-forecast").json()
    start = (response["items"][0]["valid_period"]["start"])[11:16]
    end = (response["items"][0]["valid_period"]["end"])[11:16]
    forecast = (response["items"][0]["forecasts"][area.location]["forecast"])
    text = f"The forecast for {area.name} is {forecast} from {start} to {end}"
    if area.status != text:
        await context.bot.send_message(job.chat_id, text=text)
    area.status = text


async def end(update: Update, context: CallbackContext) -> None:
    current_jobs = context.job_queue.get_jobs_by_name(str(update.effective_message.chat_id))
    if current_jobs:
        for job in current_jobs:
            job.schedule_removal()
    await update.message.reply_text("Removed Alerts")


def main() -> None:
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("set", set_command))
    dispatcher.add_handler(CommandHandler("end", end))
    dispatcher.add_handler(CallbackQueryHandler(button))

    updater.start_webhook(listen="0.0.0.0",
                        port=int(PORT),
                        url_path=TOKEN,
                        webhook_url="https://weather-forecast-sg.herokuapp.com/" + TOKEN)
    updater.idle()

if __name__ == "__main__":
    main()


#@app.route("/", methods=["GET", "POST"])
#def home():
#    if request.method == "POST":
#        application = Application.builder().token("5906044284:AAFvXhElWvNLFBbnLgn8NfRc95dB0g5jzjU").build()
#        application.add_handler(CommandHandler("start", start))
#        application.add_handler(CommandHandler("set", set_command))
#        application.add_handler(CommandHandler("end", end))
#        application.add_handler(CallbackQueryHandler(button))
#        application.run_polling()
