import sys
from io import BytesIO

import telegram
from flask import Flask, request, send_file

from fsm import TocMachine


API_TOKEN = '225070736:AAGWVF4fw_3L2R7RYQM-AXFCoqL4IyiuUnk'
WEBHOOK_URL = 'https://196c8b75.ngrok.io/hook'

app = Flask(__name__)
bot = telegram.Bot(token=API_TOKEN)
machine = TocMachine(
    states=[
        'initial',
        'byNum',
        'byName',
        'deck',
        'deckwhich',
        'deckrecommend',
        'deckall',
        'deckrace',
        'decknorace',
        'help',
        'limit',
        'image',
        'imageresult'
    ],
    transitions=[
        {
            'trigger': 'advance',
            'source': 'initial',
            'dest': 'byNum',
            'conditions': 'is_going_to_byNum'
        },
        {
            'trigger': 'advance',
            'source': 'initial',
            'dest': 'byName',
            'conditions': 'is_going_to_byName'
        },
        {
            'trigger': 'go_back_initial',
            'source': [
                'byNum',
                'byName',
                'deckrecommend',
                'deckall',
                'deckrace',
                'decknorace',
                'help',
                'limit',
                'image',
                'imageresult'
            ],
            'dest': 'initial'
        },
        {
            'trigger': 'advance',
            'source': 'initial',
            'dest': 'deck',
            'conditions': 'is_going_to_deck'
        },
        {
            'trigger': 'advance',
            'source': 'deck',
            'dest': 'deckwhich',
            'conditions': 'is_going_to_deckwhich'
        },
        {
            'trigger': 'advance',
            'source': 'deck',
            'dest': 'deckrecommend',
            'conditions': 'is_going_to_deckrecommend'
        },
        {
            'trigger': 'advance',
            'source': 'deckwhich',
            'dest': 'deckall',
            'conditions': 'is_going_to_deckall'
        },
        {
            'trigger': 'advance',
            'source': 'deckwhich',
            'dest': 'deckrace',
            'conditions': 'is_going_to_deckrace'
        },
        {
            'trigger': 'advance',
            'source': 'deckwhich',
            'dest': 'decknorace',
            'conditions': 'is_going_to_decknorace'
        },
        {
            'trigger': 'advance',
            'source': 'initial',
            'dest': 'help',
            'conditions': 'is_going_to_help'
        },
        {
            'trigger': 'advance',
            'source': 'initial',
            'dest': 'limit',
            'conditions': 'is_going_to_limit'
        },
        {
            'trigger': 'advance',
            'source': 'initial',
            'dest': 'image',
            'conditions': 'is_going_to_image'
        },
        {
            'trigger': 'advance',
            'source': 'image',
            'dest': 'imageresult',
            'conditions': 'is_going_to_imageresult'
        }
    ],
    initial='initial',
    auto_transitions=False,
    show_conditions=True,
)


def _set_webhook():
    status = bot.set_webhook(WEBHOOK_URL)
    if not status:
        print('Webhook setup failed')
        sys.exit(1)
    else:
        print('Your webhook URL has been set to "{}"'.format(WEBHOOK_URL))


@app.route('/hook', methods=['POST'])
def webhook_handler():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    machine.advance(update)
    return 'ok'


@app.route('/show-fsm', methods=['GET'])
def show_fsm():
    byte_io = BytesIO()
    machine.graph.draw(byte_io, prog='dot', format='png')
    byte_io.seek(0)
    return send_file(byte_io, attachment_filename='fsm.png', mimetype='image/png')


if __name__ == "__main__":
    _set_webhook()
    app.run()
