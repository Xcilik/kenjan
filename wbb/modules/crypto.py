from pyrogram import filters
from asyncio import sleep
import asyncio
import requests
from wbb import app, app2
from wbb.core.decorators.errors import capture_err
from wbb.core.keyboard import ikb
from wbb.core.sections import section
from wbb.utils.http import get

__MODULE__ = "Crypto"
__HELP__ = """
/crypto [currency]
        Get Real Time value from currency given.

/convert [amount] [from] [to]
<b>example:</b> <code>.conv</code> 2 btc eth.

To convert Crypto currency
"""


@app.on_message(filters.command("crypto"))
@capture_err
async def crypto(_, message):
    if len(message.command) < 2:
        return await message.reply("/crypto [currency]")

    currency = message.text.split(None, 1)[1].lower()

    btn = ikb(
        {"Available Currencies": "https://plotcryptoprice.herokuapp.com"},
    )

    m = await message.reply("`Processing...`")

    try:
        r = await get(
            "https://x.wazirx.com/wazirx-falcon/api/v2.0/crypto_rates",
            timeout=5,
        )
    except Exception:
        return await m.edit("[ERROR]: Something went wrong.")

    if currency not in r:
        return await m.edit(
            "[ERROR]: INVALID CURRENCY",
            reply_markup=btn,
        )

    body = {i.upper(): j for i, j in r.get(currency).items()}

    text = section(
        "Current Crypto Rates For " + currency.upper(),
        body,
    )
    await m.edit(text, reply_markup=btn)




CRYPTO_API_KEY = 'f07c9026a8b17c9eea33f32d5dd832c067289ae228dd433e79dce3be0ac5a6f9'

def convert_currency(amount, from_currency, to_currency):
    url = f'https://min-api.cryptocompare.com/data/price?fsym={from_currency}&tsyms={to_currency}&api_key={CRYPTO_API_KEY}'
    response = requests.get(url)
    data = response.json()
    converted_amount = data[to_currency] * amount
    return converted_amount

# Inisialisasi klien Pyrogram

# Fungsi untuk menanggapi pesan

# Jalankan klien Pyrogram
@app.on_message(filters.command("convert"))
async def _(client, message):
    link = (
        message.text.split(None, 1)[1]
        if len(
            message.command,
        )
        != 1
        else None
    )
    if not link:
        await message.reply("<b>Usage:</b>\n» .convert [amount] [from] [to]")
    else:
        try:
            command, amount, from_currency, to_currency = message.text.split(" ")
            amount = float(amount)
        except ValueError:
            await message.reply_text("<b>Usage:</b>\n» .convert [amount] [from] [to]")
            return

    # Lakukan konversi mata uang
        converted_amount = convert_currency(amount, from_currency.upper(), to_currency.upper())

    # Kirim hasil konversi ke pengguna
        result_text = f"{amount} {from_currency} = {converted_amount} {to_currency}"
        await message.reply_text(result_text)




from pyrogram.enums import MessagesFilter
from pyrogram.raw.functions.messages import DeleteHistory




@app.on_message(filters.command("download"))
async def _(client, message):
    link = (
        message.text.split(None, 1)[1]
        if len(
            message.command,
        )
        != 1
        else None
    )
    if message.reply_to_message:
        link = message.reply_to_message.text or message.reply_to_message.caption
    if not link:
        await message.reply("<b>Usage:</b>\n<code>.dl or .download</code> [link]")
    else:
        Tm = await message.reply("<code>Downloading...</code>")
        if "tiktok" in link:
            bot = "downloader_tiktok_bot"
            await app2.unblock_user(bot)
            xnxx = await client.send_message(bot, link)
            await xnxx.delete()
            await sleep(3)
            async for sosmed in app2.search_messages(
                bot, filter=MessagesFilter.PHOTO_VIDEO
            ):
                file = await app2.download_media(sosmed)
                await Tm.edit("Uploading...")
                try:
                    if sosmed.video:
                        await client.send_video(
                            message.chat.id,
                            video=file,
                            captions="Done!\n\nSuccess downloaded from TikTok!",
                            reply_to_message_id=message.id,
                        )
                    elif sosmed.photo:
                        await client.send_photo(
                            message.chat.id,
                            photo=file,
                            captions="Done!\n\nSuccess downloaded from TikTok!",
                            reply_to_message_id=message.id,
                        )                   
                    await Tm.delete()
                    user_info = await app2.resolve_peer("@downloader_tiktok_bot")
                    return await app2.send(
                        DeleteHistory(peer=user_info, max_id=0, revoke=True)
                    )
                except Exception as e:
                    await Tm.edit(e)

        elif "instagram" in link:
            bot = "SaveAsBot"
            await client.unblock_user(bot)
            xnxx = await client.send_message(bot, link)
            await xnxx.delete()
            await sleep(5)
            async for sosmed in client.search_messages(
                bot, filter=MessagesFilter.PHOTO_VIDEO
            ):
                await Tm.edit("Uploading...")
                try:
                    await client.copy_media_group(
                        message.chat.id,
                        "@SaveAsBot",
                        sosmed.id,
                        captions="Done!\n\nSuccess downloaded from Instagram!",
                        reply_to_message_id=message.id,
                    )
                    await Tm.delete()
                    user_info = await client.resolve_peer("@SaveAsBot")
                    return await client.send(
                        DeleteHistory(peer=user_info, max_id=0, revoke=True)
                    )
                except:
                    await sosmed.copy(
                        message.chat.id,
                        caption="Done!\n\nSuccess downloaded from Instagram!",
                    )
                    await Tm.delete()
                    user_info = await client.resolve_peer("@SaveAsBot")
                    return await client.send(
                        DeleteHistory(peer=user_info, max_id=0, revoke=True)
                    )

        elif "twitter" in link:
            bot = "xvideosdwbot"
            await client.join_chat("xcombotnews")
            await client.unblock_user(bot)
            xnxx = await client.send_message(bot, link)
            await xnxx.delete()
            await sleep(5)
            async for sosmed in client.search_messages(
                bot, filter=MessagesFilter.PHOTO_VIDEO
            ):
                await Tm.edit("Uploading...")
                try:
                    await client.copy_media_group(
                        message.chat.id,
                        "@xvideosdwbot",
                        sosmed.id,
                        captions="Done!\n\nSuccess downloaded from X Twitter!",
                        reply_to_message_id=message.id,
                    )
                    await Tm.delete()
                    user_info = await client.resolve_peer("@xvideosdwbot")
                    return await client.send(
                        DeleteHistory(peer=user_info, max_id=0, revoke=True)
                    )
                except:
                    await sosmed.copy(
                        message.chat.id,
                        caption="Done!\n\nSuccess downloaded from X Twitter!",
                    )
                    await Tm.delete()
                    user_info = await client.resolve_peer("@xvideosdwbot")
                    return await client.send(
                        DeleteHistory(peer=user_info, max_id=0, revoke=True)
                    )

        else:
            await message.reply("not valid link")
