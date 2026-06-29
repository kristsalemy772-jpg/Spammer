import asyncio
import os
from aiohttp import web
from telegram import Bot, LinkPreviewOptions

BOT_TOKEN = "8929884157:AAH2_l-iYqOOTUmMayvrSIIPGmEQba64sOk"
CHANNEL_ID = "@KAZELIDERMODS"

bot = Bot(token=BOT_TOKEN)

# 1. TEMPLATE PARA SA MLBB UPDATE
# 1. TEMPLATE PARA SA MLBB UPDATE (Naka-Collapsible Quote na)
MLBB_MESSAGE = """<blockquote expandable="true"><i><a href="https://t.me/KAZELIDERMODS/6270">𝘓𝘢𝘵𝘦𝘴𝘵 𝘜𝘥𝘱𝘢𝘵𝘦:
𝘔𝘰𝘣𝘪𝘭𝘦 𝘓𝘦𝘨𝘦𝘯𝘥𝘴: 𝘉𝘢𝘯𝘨 𝘉𝘢𝘯𝘨
𝘷2.1.88.12027 || 𝘔𝘰𝘥 𝘷3.1.3</a>

𝘕𝘌𝘌𝘋 𝘒𝘌𝘠 𝘓𝘖𝘎𝘐𝘕 ??? :
𝘍𝘰𝘳 𝘪𝘯𝘲𝘶𝘪𝘳𝘪𝘦𝘴 𝘢𝘯𝘥 𝘢𝘷𝘢𝘪𝘭𝘮𝘦𝘯𝘵, 𝘴𝘦𝘯𝘥 𝘢 𝘥𝘪𝘳𝘦𝘤𝘵 𝘮𝘦𝘴𝘴𝘢𝘨𝘦 ~ <a href="https://t.me/phia_maganda">𝘗𝘩𝘪𝘢 𝘍𝘦𝘭𝘪𝘤𝘪𝘢</a>

𝘕𝘰 𝘍𝘳𝘦𝘦 🫪 𝘎𝘌𝘛𝘚!?</i></blockquote>"""


# 2. TEMPLATE PARA SA CODM
CODM_MESSAGE = """<a href="https://t.me/KAZELIDERMODS/380">𝘊𝘖𝘋𝘔 𝘐𝘕𝘑𝘌𝘊𝘛𝘖𝘙 𝘛𝘙𝘐𝘈𝘓 𝘊𝘓𝘖𝘚𝘌!!!...</a>"""

# 3. TEMPLATE PARA SA PROMO (Naka-Quote + Malinis na Italic Fonts)
PROMO_MESSAGE = """<blockquote>𝘗𝘙𝘖𝘔𝘖 &lt; 30𝘋𝘈𝘠𝘚 &gt; (𝘔𝘓𝘉𝘉 𝘝𝘪𝘗)
  
   𝘍𝘜𝘓𝘓 𝘝𝘌𝘙𝘚𝘐𝘖𝘕 𝘞𝘐𝘛𝘏 𝘉𝘠𝘗𝘈𝘚𝘚!!

₱599 || $10.16 &gt; 30𝘋𝘈𝘠𝘚 &lt; 

𝘋𝘔: <a href="https://t.me/phia_maganda">@phia_maganda</a>/<a href="https://t.me/TADOOOHULOL"></a>
💥 𝘸𝘢𝘯𝘵 𝘵𝘰 𝘣𝘦 𝘳𝘦𝘴𝘦𝘭𝘭𝘦𝘳?</blockquote>"""

# Tatlong templates na magsalitan sa 2-minute loop
ALL_MESSAGES = [MLBB_MESSAGE, CODM_MESSAGE, PROMO_MESSAGE]

async def loop_spam():
    print("Spammer bot started (Alternating MLBB, CODM, and PROMO + 2 mins delay)...")
    index = 0
    
    while True:
        try:
            current_message = ALL_MESSAGES[index % len(ALL_MESSAGES)]
            
            # 1. IPAPALAPAG ANG CURRENT MESSAGE
            sent_message = await bot.send_message(
                chat_id=CHANNEL_ID,
                text=current_message,
                parse_mode="HTML",
                disable_notification=False,
                link_preview_options=LinkPreviewOptions(is_disabled=True)
            )
            print(f"Message sent! (Index: {index} | ID: {sent_message.message_id})")

            # 2. BIBILANG NG 2 MINUTO (120 SECONDS) BAGO BURAHIN
            await asyncio.sleep(600)

            # 3. BURAHIN PAGKATAPOS NG 2 MINUTO
            await bot.delete_message(
                chat_id=CHANNEL_ID,
                message_id=sent_message.message_id
            )
            print(f"Deleted Message ID: {sent_message.message_id}")

            # 4. AGWAT BAGO MAG-SEND ULIT NG KASUNOD NA MESSAGE (3 seconds)
            await asyncio.sleep(3)
            
            index += 1

        except Exception as e:
            print("Error sa loop:", e)
            await asyncio.sleep(10)

# --- RENDER WEB SERVER CONFIGURATION ---
async def handle_index(request):
    return web.Response(text="Bot is running smoothly on Render!")

async def main():
    app = web.Application()
    app.router.add_get('/', handle_index)
    
    port = int(os.environ.get("PORT", 8080))
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", port)
    
    print(f"Starting dummy web server on port {port} for Render...")
    await site.start()
    
    await loop_spam()

if __name__ == "__main__":
    asyncio.run(main())
   
