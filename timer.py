import logging
from typing import Dict
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, PicklePersistence
import requests
import datetime
from dotenv import load_dotenv
import os

load_dotenv()

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
# Best practice would be to replace context with an underscore,
# since context is an unused local variable.
# This being an example and not having context present confusing beginners,
# we decided to have it present as context.
def facts_to_str(user_data: Dict[str, str]) -> str:
    """Helper function for formatting the gathered user info."""
    print(user_data)
    facts = [f'{key} - {value}' for key, value in user_data.items()]
    return "\n".join(facts).join(['\n', '\n'])


def start(update: Update, context: CallbackContext) -> None:
    """Sends explanation on how to use the bot."""
    print(context.args[0])
    context.user_data["pincode"] = context.args[0]
    context.user_data["chat_id"] = update.message.chat_id
    print(facts_to_str(context.user_data))
    # context.user_data["pincode"] = text.lower()
    update.message.reply_text('Hi! Use /set <seconds> to set a timer')


def alarm(context: CallbackContext) -> None:
    """Send the alarm message."""
    # try:
    job = context.job
    print("alarm", job.context)
    checkTime = datetime.datetime.now()
    checkTime = checkTime.replace(hour=5, minute=30, second=00)
    today = datetime.datetime.now()
    if checkTime < datetime.datetime.now():
        today = today + datetime.timedelta(days=1)
    today = today.strftime("%d/%m/%Y")
    print(today)
    r = requests.get('https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin', params={'pincode':job.context["pincode"], 'date':today }, headers={'Accept-Language':'hi_IN', 'accept':'application/json'})
    # data = {'sessions': [{'center_id': 716554, 'name': 'Oscar Hospital WP Other', 'address': 'Opposite Ganesh Nagar  Near Hindustan Naka Kandivali West', 'state_name': 'Maharashtra', 'district_name': 'Mumbai', 'block_name': 'Ward R South Corporation - MH', 'pincode': 400067, 'from': '11:00:00', 'to': '17:00:00', 'lat': 19, 'long': 72, 'fee_type': 'Paid', 'session_id': '97ced0eb-6899-4ab9-97a1-8361a51a6a7a', 'date': '11-09-2021', 'available_capacity': 0, 'available_capacity_dose1': 0, 'available_capacity_dose2': 0, 'fee': '0', 'min_age_limit': 45, 'allow_all_age': False, 'vaccine': 'SPUTNIK V', 'slots': ['11:00AM-12:00PM', '12:00PM-01:00PM', '01:00PM-02:00PM', '02:00PM-05:00PM']}, {'center_id': 716554, 'name': 'Oscar Hospital WP Other', 'address': 'Opposite Ganesh Nagar  Near Hindustan Naka Kandivali West', 'state_name': 'Maharashtra', 'district_name': 'Mumbai', 'block_name': 'Ward R South Corporation - MH', 'pincode': 400067, 'from': '10:00:00', 'to': '17:00:00', 'lat': 19, 'long': 72, 'fee_type': 'Free', 'session_id': 'a42f0904-037c-4d12-a68d-8503e082199c', 'date': '11-09-2021', 'available_capacity': 0, 'available_capacity_dose1': 0, 'available_capacity_dose2': 0, 'fee': '0', 'min_age_limit': 18, 'allow_all_age': False, 'vaccine': 'COVISHIELD', 'slots': ['10:00AM-12:00PM', '12:00PM-02:00PM', '02:00PM-04:00PM', '04:00PM-05:00PM']}, {'center_id': 716554, 'name': 'Oscar Hospital WP Other', 'address': 'Opposite Ganesh Nagar  Near Hindustan Naka Kandivali West', 'state_name': 'Maharashtra', 'district_name': 'Mumbai', 'block_name': 'Ward R South Corporation - MH', 'pincode': 400067, 'from': '11:00:00', 'to': '17:00:00', 'lat': 19, 'long': 72, 'fee_type': 'Paid', 'session_id': '681df80c-e54b-4c03-8f60-a78958660889', 'date': '11-09-2021', 'available_capacity': 0, 'available_capacity_dose1': 0, 'available_capacity_dose2': 0, 'fee': '0', 'min_age_limit': 18, 'max_age_limit': 44, 'allow_all_age': False, 'vaccine': 'SPUTNIK V', 'slots': ['11:00AM-12:00PM', '12:00PM-01:00PM', '01:00PM-02:00PM', '02:00PM-05:00PM']}, {'center_id': 716554, 'name': 'Oscar Hospital WP Other', 'address': 'Opposite Ganesh Nagar  Near Hindustan Naka Kandivali West', 'state_name': 'Maharashtra', 'district_name': 'Mumbai', 'block_name': 'Ward R South Corporation - MH', 'pincode': 400067, 'from': '10:00:00', 'to': '17:00:00', 'lat': 19, 'long': 72, 'fee_type': 'Paid', 'session_id': 'ea7abd6e-8af5-48dc-a906-86a5bcb7dabb', 'date': '11-09-2021', 'available_capacity': 0, 'available_capacity_dose1': 0, 'available_capacity_dose2': 0, 'fee': '0', 'min_age_limit': 18, 'max_age_limit': 44, 'allow_all_age': False, 'vaccine': 'COVISHIELD', 'slots': ['10:00AM-12:00PM', '12:00PM-02:00PM', '02:00PM-04:00PM', '04:00PM-05:00PM']}]}
    # print(r.json())
    data = r.json()
    print(data)
    
    for session in data["sessions"]:
        if session["fee_type"] == "Free" and session["min_age_limit"] >= 18:
            print("True")
            text_html = "<b>" + str(session["name"]) + "</b>" + " \n<b>Slot Available Dose 1 " + str(session["available_capacity_dose1"]) + "</b>"
            print(text_html)
            context.bot.send_message(job.context["chat_id"], parse_mode='HTML', text=text_html)
        else:
            print("false")
    # except err:
    #     print("error found")
    # context.bot.send_message(job.context, text='Beep!')


def remove_job_if_exists(name: str, context: CallbackContext) -> bool:
    """Remove job with given name. Returns whether job was removed."""
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True


def set_timer(update: Update, context: CallbackContext) -> None:
    """Add a job to the queue."""
    chat_id = update.message.chat_id
    try:
        # args[0] should contain the time for the timer in seconds
        due = int(context.args[0])
        if due < 0:
            update.message.reply_text('Sorry we can not go back to future!')
            return

        job_removed = remove_job_if_exists(str(chat_id), context)
        context.job_queue.run_repeating(alarm, due, context=context.user_data, name=str(chat_id))

        text = 'Timer successfully set!'
        if job_removed:
            text += ' Old one was removed.'
        update.message.reply_text(text)

    except (IndexError, ValueError):
        update.message.reply_text('Usage: /set <seconds>')


def unset(update: Update, context: CallbackContext) -> None:
    """Remove the job if the user changed their mind."""
    chat_id = update.message.chat_id
    job_removed = remove_job_if_exists(str(chat_id), context)
    text = 'Timer successfully cancelled!' if job_removed else 'You have no active timer.'
    update.message.reply_text(text)


def main() -> None:
    """Run bot."""
    # Create the Updater and pass it your bot's token.
    token = os.getenv('bottoken')
    persistence = PicklePersistence(filename='conversationbot')
    updater = Updater(token, persistence=persistence)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", start))
    dispatcher.add_handler(CommandHandler("set", set_timer))
    dispatcher.add_handler(CommandHandler("unset", unset))

    # Start the Bot
    updater.start_polling()

    # Block until you press Ctrl-C or the process receives SIGINT, SIGTERM or
    # SIGABRT. This should be used most of the time, since start_polling() is
    # non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()