"""
MIT License

Copyright (c) 2023 TheHamkerCat

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import re

from pyrogram import filters

from wbb import app
import requests
import openai as anuan
import g4f
from bing_image_downloader import downloader
from wbb.core.decorators.errors import capture_err
from wbb.core.decorators.permissions import adminsOnly
from wbb.core.sections import section
from wbb.utils.dbfunctions import (
    alpha_to_int,
    get_karma,
    get_karmas,
    int_to_alpha,
    is_karma_on,
    karma_off,
    karma_on,
    update_karma,
)
from sample_config import OPENAI_APIKEY
from wbb.utils.filter_groups import karma_negative_group, karma_positive_group
from wbb.utils.functions import get_user_id_and_usernames

__MODULE__ = "OpenAI"
__HELP__ = """
/ai [question] - Generated text / ChatGpt
/dalle [text] - Generated Image
"""

regex_upvote = r"^(\++|\+1|thx|tnx|tq|ty|thankyou|thank you|thanx|thanks|pro|cool|good|agree|👍|\++ .+)$"
regex_downvote = r"^(-+|-1|not cool|disagree|worst|bad|👎|-+ .+)$"


async def ChatGPT(question):
    try:
        response = await g4f.ChatCompletion.create_async(
            model=g4f.models.default,
            provider=g4f.Provider.GeekGpt,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": question},
            ],
            timeout=60,
        )
        return response if response else "lagi error coba lagi nanti"
    except Exception as error:
        return str(error)

def get_text(message):
    reply_text = (
        message.reply_to_message.text or message.reply_to_message.caption
        if message.reply_to_message
        else ""
    )
    user_text = message.text.split(None, 1)[1] if len(message.text.split()) >= 2 else ""
    return (
        f"{user_text}\n\n{reply_text}"
        if reply_text and user_text
        else reply_text + user_text
    )

@app.on_message(
    filters.command("ai")
)
async def openai(_, message):
    args = get_text(message)
    if not args:
        return await message.reply("<b>What???</b>")    
    Tm = await message.reply("<code>Generated Text...</code>")        
    try:
        response = await ChatGPT(args)
        if len(response) > 4096:
            with io.BytesIO(response.encode()) as out_file:
                out_file.name = "openAi.txt"
                await message.reply_document(document=out_file)
        else:
            msg = message.reply_to_message or message
            await app.send_message(
                message.chat.id, response, reply_to_message_id=msg.id
            )
    except Exception as error:
        await message.reply(str(error))
    await Tm.delete()


@app.on_message(
    filters.command("image")
)
async def iamges(_, message):
    msg = (
        message.text.split(None, 1)[1]
        if len(
            message.command,
        )
        != 1
        else None
    )
    if not msg:
        await message.reply("<b>What image to seacrh?</b>")
    else:
        cilik = await message.reply("<code>Searching image...</code>")
        try:            
            downloader.download(query, limit=5, output_dir='downloads', adult_filter_off=True, force_replace=False)
            for i in range(1, 6):
                image_path = f"downloads/{query}/{query}{i}.jpg"
                await app.send_photo(message.chat.id, photo=open(image_path, 'rb'))
            await cilik.delete()
        except Exception as e:
            await cilik.edit(f"{e}")
            
@app.on_message(
    filters.command("dalle")
)
async def curie(_, message):
    msg = (
        message.text.split(None, 1)[1]
        if len(
            message.command,
        )
        != 1
        else None
    )
    if not msg:
        await message.reply("<b>What image to manipulated?</b>")
    else:
        cilik = await message.reply("<code>Manipulated image...</code>")
        try:            
            anuan.api_key = OPENAI_APIKEY
            response = anuan.Image.create(
            prompt=msg,
            n=1,
            size="1024x1024"
            )
            image_url = response['data'][0]['url']
            await app.send_photo(message.chat.id, photo=image_url)
            await cilik.delete()
        except Exception as e:
            await cilik.edit(f"{e}")
            
@app.on_message(
    filters.text
    & filters.group
    & filters.incoming
    & filters.reply
    & filters.regex(regex_upvote, re.IGNORECASE)
    & ~filters.via_bot
    & ~filters.bot,
    group=karma_positive_group,
)
@capture_err
async def upvote(_, message):
    if not await is_karma_on(message.chat.id):
        return
    if not message.reply_to_message.from_user:
        return
    if not message.from_user:
        return
    if message.reply_to_message.from_user.id == message.from_user.id:
        return
    chat_id = message.chat.id
    user_id = message.reply_to_message.from_user.id
    user_mention = message.reply_to_message.from_user.mention
    current_karma = await get_karma(chat_id, await int_to_alpha(user_id))
    if current_karma:
        current_karma = current_karma["karma"]
        karma = current_karma + 1
        new_karma = {"karma": karma}
        await update_karma(chat_id, await int_to_alpha(user_id), new_karma)
    else:
        karma = 1
        new_karma = {"karma": karma}
        await update_karma(chat_id, await int_to_alpha(user_id), new_karma)
    await message.reply_text(
        f"Incremented Karma of {user_mention} By 1 \nTotal Points: {karma}"
    )


@app.on_message(
    filters.text
    & filters.group
    & filters.incoming
    & filters.reply
    & filters.regex(regex_downvote, re.IGNORECASE)
    & ~filters.via_bot
    & ~filters.bot,
    group=karma_negative_group,
)
@capture_err
async def downvote(_, message):
    if not await is_karma_on(message.chat.id):
        return
    if not message.reply_to_message.from_user:
        return
    if not message.from_user:
        return
    if message.reply_to_message.from_user.id == message.from_user.id:
        return

    chat_id = message.chat.id
    user_id = message.from_user.id
    current_karma = await get_karma(chat_id, await int_to_alpha(user_id))
    if current_karma:
        current_karma = current_karma["karma"]
        karma = current_karma - 1
        new_karma = {"karma": karma}
        await update_karma(chat_id, await int_to_alpha(user_id), new_karma)
    else:
        karma = 1
        new_karma = {"karma": karma}
        await update_karma(chat_id, await int_to_alpha(user_id), new_karma)

    user_id = message.reply_to_message.from_user.id
    user_mention = message.reply_to_message.from_user.mention
    current_karma = await get_karma(chat_id, await int_to_alpha(user_id))
    if current_karma:
        current_karma = current_karma["karma"]
        karma = current_karma - 1
        new_karma = {"karma": karma}
        await update_karma(chat_id, await int_to_alpha(user_id), new_karma)
    else:
        karma = 1
        new_karma = {"karma": karma}
        await update_karma(chat_id, await int_to_alpha(user_id), new_karma)
    await message.reply_text(
        f"Decremented Karma of {user_mention} By 1 \nTotal Points: {karma}"
    )


@app.on_message(filters.command("karma") & filters.group)
@capture_err
async def command_karma(_, message):
    chat_id = message.chat.id
    if not message.reply_to_message:
        m = await message.reply_text("Analyzing Karma...")
        karma = await get_karmas(chat_id)
        if not karma:
            return await m.edit("No karma in DB for this chat.")
        msg = f"Karma list of {message.chat.title}"
        limit = 0
        karma_dicc = {}
        for i in karma:
            user_id = await alpha_to_int(i)
            user_karma = karma[i]["karma"]
            karma_dicc[str(user_id)] = user_karma
            karma_arranged = dict(
                sorted(
                    karma_dicc.items(),
                    key=lambda item: item[1],
                    reverse=True,
                )
            )
        if not karma_dicc:
            return await m.edit("No karma in DB for this chat.")
        userdb = await get_user_id_and_usernames(app)
        karma = {}
        for user_idd, karma_count in karma_arranged.items():
            if limit > 15:
                break
            if int(user_idd) not in list(userdb.keys()):
                continue
            username = userdb[int(user_idd)]
            karma["@" + username] = ["**" + str(karma_count) + "**"]
            limit += 1
        await m.edit(section(msg, karma))
    else:
        if not message.reply_to_message.from_user:
            return await message.reply("Anon user has no karma.")

        user_id = message.reply_to_message.from_user.id
        karma = await get_karma(chat_id, await int_to_alpha(user_id))
        if karma:
            karma = karma["karma"]
            await message.reply_text(f"**Total Points**: __{karma}__")
        else:
            karma = 0
            await message.reply_text(f"**Total Points**: __{karma}__")


@app.on_message(filters.command("karma_toggle") & ~filters.private)
@adminsOnly("can_change_info")
async def captcha_state(_, message):
    usage = "**Usage:**\n/karma_toggle [ENABLE|DISABLE]"
    if len(message.command) != 2:
        return await message.reply_text(usage)
    chat_id = message.chat.id
    state = message.text.split(None, 1)[1].strip()
    state = state.lower()
    if state == "enable":
        await karma_on(chat_id)
        await message.reply_text("Enabled Karma System for this chat.")
    elif state == "disable":
        await karma_off(chat_id)
        await message.reply_text("Disabled Karma System for this chat.")
    else:
        await message.reply_text(usage)
