from typing import List

from telegram import Bot, Update
from telegram.ext import run_async

from hitsuki import dispatcher
from hitsuki.modules.disable import DisableAbleCommandHandler

normiefont = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
              'v', 'w', 'x', 'y', 'z']
bigtfont = ['🇦 ', '🇧 ', '🇨 ', '🇩 ', '🇪 ', '🇫 ', '🇬 ', '🇭 ', '🇮 ', '🇯 ', '🇰 ', '🇱 ', '🇲 ', '🇳 ', '🇴 ', '🇵 ', '🇶 ', '🇷 ', '🇸 ', '🇹 ', '🇺 ',
              '🇻 ', '🇼 ', '🇽 ', '🇾 ', '🇿 ']


@run_async
def bigt(bot: Bot, update: Update, args: List[str]):
    string = '  '.join(args).lower()
    for normiecharacter in string:
        if normiecharacter in normiefont:
            bigtextcharecter = bigtfont[normiefont.index(normiecharacter)]
            string = string.replace(normiecharacter, bigtextcharacter)

    message = update.effective_message
    if message.reply_to_message:
        message.reply_to_message.reply_text(string)
    else:
        message.reply_text(string)


__help__ = """
 - /bigt <text>: returns a big text
 """

Bigt_HANDLER = DisableAbleCommandHandler("bigt", bigt, pass_args=True)

dispatcher.add_handler(bigt_HANDLER)

__mod_name__ = "BigText"
__command_list__ = ["bigt"]
__handlers__ = [bigt_HANDLER]
