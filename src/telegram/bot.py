import sys
sys.path.append('..')

from util.Rextester import Rextester, RextesterException

import telebot

bot = telebot.TeleBot('')
rextester = Rextester()


@bot.message_handler(func=lambda message: message.text.startswith('/exec'))
def handle_exec(message):
    message_text = message.text

    if len(message_text.split(" ")) < 3:
        return

    stdin = ''
    if "/stdin" in message_text:
        stdin = ' '.join(message_text.split('/stdin ')[1:])
        message_text = message_text.replace('/stdin ' + stdin, '')

    language = message_text.split(' ')[1]
    code = ' '.join(message_text.split(' ')[2:])

    try:
        response = rextester.execute(language=language, code=code, stdin=stdin)
    except RextesterException:
        bot.send_message(message.chat.id, 'error @ rextester or unknown language')
        return

    extra = ''
    if response['Warnings']:
        extra = extra + '\nWarning: ' + response['Warnings']
    if response['Errors']:
        extra = extra + '\nErrors: ' + response['Errors']

    stats = ''
    if response['Stats']:
        stats = '\nStats: ' + response['Stats']

    output = ' no output '
    if response['Result']:
        output = response['Result']

    if len(extra) < 4070:  # prevent message_too_long
        bot.send_message(message.chat.id, 'Output: ' + output[:(4080 - len(extra) - len(stats))] + extra + stats)
    else:
        bot.send_message(message.chat.id, 'too much long errors/warnings to show output')


while True:
    try:
        bot.polling(none_stop=True)
    except KeyboardInterrupt:
        exit(0)
    except Exception as e:
        continue
