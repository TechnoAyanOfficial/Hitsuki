import asyncio
import base64
import glob
import io
import os
import random
import re
import urllib.request
from io import BytesIO
from pathlib import Path
from typing import List

import nltk  # shitty lib, but it does work
from PIL import Image
from spongemock import spongemock
from telegram import Message, Update, Bot
from telegram.error import BadRequest
from telegram.ext import CommandHandler, run_async
from zalgo_text import zalgo

from deeppyer import deepfry
from hitsuki import DEEPFRY_TOKEN
from hitsuki import dispatcher
from hitsuki.modules.disable import DisableAbleCommandHandler

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

MAXNUMURL = 'https://raw.githubusercontent.com/atanet90/expression-pack/master/meta'
WIDE_MAP = dict((i, i + 0xFEE0) for i in range(0x21, 0x7F))
WIDE_MAP[0x20] = 0x3000


# D A N K modules by @deletescape vvv


@run_async
def owo(bot: Bot, update: Update):
    message = update.effective_message
    if not message.reply_to_message:
        message.reply_text("I need a message to meme.")
    else:
        faces = ['(・`ω´・)', ';;w;;', 'owo', 'UwU', '>w<', '^w^', '\(^o\) (/o^)/', '( ^ _ ^)∠☆', '(ô_ô)', '~:o',
                 ';____;', '(*^*)', '(>_', '(♥_♥)', '*(^O^)*', '((+_+))']
        reply_text = re.sub(r'[rl]', "w", message.reply_to_message.text)
        reply_text = re.sub(r'[ｒｌ]', "ｗ", message.reply_to_message.text)
        reply_text = re.sub(r'[RL]', 'W', reply_text)
        reply_text = re.sub(r'[ＲＬ]', 'Ｗ', reply_text)
        reply_text = re.sub(r'n([aeiouａｅｉｏｕ])', r'ny\1', reply_text)
        reply_text = re.sub(r'ｎ([ａｅｉｏｕ])', r'ｎｙ\1', reply_text)
        reply_text = re.sub(r'N([aeiouAEIOU])', r'Ny\1', reply_text)
        reply_text = re.sub(r'Ｎ([ａｅｉｏｕＡＥＩＯＵ])', r'Ｎｙ\1', reply_text)
        reply_text = re.sub(r'\!+', ' ' + random.choice(faces), reply_text)
        reply_text = re.sub(r'！+', ' ' + random.choice(faces), reply_text)
        reply_text = reply_text.replace("ove", "uv")
        reply_text = reply_text.replace("ｏｖｅ", "ｕｖ")
        reply_text += ' ' + random.choice(faces)
        message.reply_to_message.reply_text(reply_text)


@run_async
def stretch(bot: Bot, update: Update):
    message = update.effective_message
    if not message.reply_to_message:
        message.reply_text("I need a message to meme.")
    else:
        count = random.randint(3, 10)
        reply_text = re.sub(r'([aeiouAEIOUａｅｉｏｕＡＥＩＯＵ])', (r'\1' * count), message.reply_to_message.text)
        message.reply_to_message.reply_text(reply_text)


@run_async
def vapor(bot: Bot, update: Update, args: List[str]):
    message = update.effective_message
    if not message.reply_to_message:
        if not args:
            message.reply_text("I need a message to convert to vaporwave text.")
        else:
            noreply = True
            data = message.text.split(None, 1)[1]
    elif message.reply_to_message:
        noreply = False
        data = message.reply_to_message.text
    else:
        data = ''

    reply_text = str(data).translate(WIDE_MAP)
    if noreply:
        message.reply_text(reply_text)
    else:
        message.reply_to_message.reply_text(reply_text)


# D A N K modules by @deletescape ^^^
# Less D A N K modules by @skittles9823 # holi fugg I did some maymays vvv


# based on https://github.com/wrxck/mattata/blob/master/plugins/copypasta.mattata
@run_async
def copypasta(bot: Bot, update: Update):
    message = update.effective_message
    if not message.reply_to_message:
        message.reply_text("I need a message to meme.")
    else:
        emojis = ["😂", "😂", "👌", "✌", "💞", "👍", "👌", "💯", "🎶", "👀", "😂", "👓", "👏", "👐", "🍕", "💥", "🍴",
                  "💦", "💦", "🍑", "🍆", "😩", "😏", "👉👌", "👀", "👅", "😩", "🚰"]
        reply_text = random.choice(emojis)
        b_char = random.choice(
            message.reply_to_message.text).lower()  # choose a random character in the message to be substituted with 🅱️
        for c in message.reply_to_message.text:
            if c == " ":
                reply_text += random.choice(emojis)
            elif c in emojis:
                reply_text += c
                reply_text += random.choice(emojis)
            elif c.lower() == b_char:
                reply_text += "🅱️"
            else:
                if bool(random.getrandbits(1)):
                    reply_text += c.upper()
                else:
                    reply_text += c.lower()
        reply_text += random.choice(emojis)
        message.reply_to_message.reply_text(reply_text)


@run_async
def bmoji(bot: Bot, update: Update):
    message = update.effective_message
    if not message.reply_to_message:
        message.reply_text("I need a message to meme.")
    else:
        b_char = random.choice(
            message.reply_to_message.text).lower()  # choose a random character in the message to be substituted with 🅱️
        reply_text = message.reply_to_message.text.replace(b_char, "🅱️").replace(b_char.upper(), "🅱️")
        message.reply_to_message.reply_text(reply_text)


@run_async
def clapmoji(bot: Bot, update: Update):
    message = update.effective_message
    if not message.reply_to_message:
        message.reply_text("I need a message to meme.")
    else:
        reply_text = "👏 "
        reply_text += message.reply_to_message.text.replace(" ", " 👏 ")
        reply_text += " 👏"
        message.reply_to_message.reply_text(reply_text)


@run_async
def zalgotext(bot: Bot, update: Update):
    message = update.effective_message
    if message.reply_to_message:
        data = message.reply_to_message.text
    else:
        data = str('Insolant human, you must reply to something to zalgofy it!')

    reply_text = zalgo.zalgo().zalgofy(data)
    message.reply_text(reply_text)


# Less D A N K modules by @skittles9823 # holi fugg I did some maymays ^^^
# shitty maymay modules made by @divadsn vvv


@run_async
def chinesememes(bot: Bot, update: Update, args: List[str]):
    message = update.effective_message
    maxnum = urllib.request.urlopen(MAXNUMURL)
    maxnum = maxnum.read().decode("utf8")
    if args:
        num = message.text.split(None, 1)[1]
    else:
        num = random.randint(0, int(maxnum))
    try:
        IMG = "https://raw.githubusercontent.com/atanet90/expression-pack/master/img/{}.jpg".format(num)
        maxnum = int(maxnum)
        maxnum -= 1
        bot.send_photo(chat_id=message.chat_id, photo=IMG, caption='Image: {} - (0-{})'.format(num, maxnum),
                       reply_to_message_id=message.message_id)
    except BadRequest as e:
        message.reply_text("Image not found!")
        print(e)


@run_async
def deepfryer(bot: Bot, update: Update):
    message = update.effective_message
    if message.reply_to_message:
        data = message.reply_to_message.photo
        data2 = message.reply_to_message.sticker
    else:
        data = []
        data2 = []

    # check if message does contain media and cancel when not
    if not data and not data2:
        message.reply_text("What am I supposed to do with this?!")
        return

    # download last photo (highres) as byte array
    if data:
        photodata = data[len(data) - 1].get_file().download_as_bytearray()
        image = Image.open(io.BytesIO(photodata))
    elif data2:
        sticker = bot.get_file(data2.file_id)
        sticker.download('sticker.png')
        image = Image.open("sticker.png")

    # the following needs to be executed async (because dumb lib)
    loop = asyncio.new_event_loop()
    loop.run_until_complete(process_deepfry(image, message.reply_to_message, bot))
    loop.close()


async def process_deepfry(image: Image, reply: Message, bot: Bot):
    # DEEPFRY IT
    image = await deepfry(
        img=image,
        token=DEEPFRY_TOKEN,
        url_base='westeurope'
    )

    bio = BytesIO()
    bio.name = 'image.jpeg'
    image.save(bio, 'JPEG')

    # send it back
    bio.seek(0)
    reply.reply_photo(bio)
    if Path("sticker.png").is_file():
        os.remove("sticker.png")


# shitty maymay modules made by @divadsn ^^^


@run_async
def shout(bot: Bot, update: Update, args):
    if len(args) == 0:
        update.effective_message.reply_text("Where is text?")
        return

    msg = "```"
    text = " ".join(args)
    result = []
    result.append(' '.join([s for s in text]))
    for pos, symbol in enumerate(text[1:]):
        result.append(symbol + ' ' + '  ' * pos + symbol)
    result = list("\n".join(result))
    result[0] = text[0]
    result = "".join(result)
    msg = "```\n" + result + "```"
    return update.effective_message.reply_text(msg, parse_mode="MARKDOWN")


# no help string
__help__ = """
*Sabrina Exclusive Commands*
-/weebify <text> : turns simple text into weebify fonts
- /owo: OWO de text
- /stretch: STRETCH de text
- /vapor: owo vapor dis
- /hitler: Quote a message and type this command to make a caption of hitler
- /mock: Does the same as /hitler but spongemock instead
- /kim: Does the same as /hitler but with Kim Jong Un instead (O no plox dont bomb my house)
- /pidor: 4pda memes
- /zalgofy: Reply to a message to g̫̞l̼̦i̎͡tͫ͢c̘ͭh̛̗ it out!
- /deepfry: For when you're hungry for memes
- /shout <keyword>: Write anything you want to give loud shout
- /dllm: Some chinese memes
- /thonkify <reply>/<args>: turns text into thonk text (only supports letters and none symbols for now).

*Emojis:*
- /clapmoji
- /bmoji
- /copypasta
"""

__mod_name__ = "🔥Sabrina Exclusive🔥"

COPYPASTA_HANDLER = CommandHandler("copypasta", copypasta)
CLAPMOJI_HANDLER = CommandHandler("clapmoji", clapmoji)
BMOJI_HANDLER = CommandHandler("bmoji", bmoji)
OWO_HANDLER = DisableAbleCommandHandler("owo", owo, admin_ok=True)
STRETCH_HANDLER = DisableAbleCommandHandler("stretch", stretch)
VAPOR_HANDLER = DisableAbleCommandHandler("vapor", vapor, pass_args=True, admin_ok=True)
ZALGO_HANDLER = DisableAbleCommandHandler("zalgofy", zalgotext)
DEEPFRY_HANDLER = DisableAbleCommandHandler("deepfry", deepfryer, admin_ok=True)
SHOUT_HANDLER = DisableAbleCommandHandler("shout", shout, pass_args=True)
DEEPFRY_HANDLER = CommandHandler("deepfry", deepfryer)
CHINESEMEMES_HANDLER = CommandHandler("dllm", chinesememes, pass_args=True)

dispatcher.add_handler(SHOUT_HANDLER)
dispatcher.add_handler(OWO_HANDLER)
dispatcher.add_handler(STRETCH_HANDLER)
dispatcher.add_handler(VAPOR_HANDLER)
dispatcher.add_handler(ZALGO_HANDLER)
dispatcher.add_handler(DEEPFRY_HANDLER)
dispatcher.add_handler(COPYPASTA_HANDLER)
dispatcher.add_handler(CLAPMOJI_HANDLER)
dispatcher.add_handler(BMOJI_HANDLER)
dispatcher.add_handler(CHINESEMEMES_HANDLER)
