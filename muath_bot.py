#!/usr/bin/env python3
import telebot
from openai import OpenAI
import os

BOT_TOKEN = os.environ.get("BOT_TOKEN")
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")

bot = telebot.TeleBot(BOT_TOKEN)
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY
)

MUATH_INFO = """
تعريف البوت
هذا بوت يعرف محمد معاذ ويجاوب على الأسئلة عنه.
البوت يتكلم عن محمد معاذ بضمير الغائب، وكأنه شخص يعرفه ويصفه للناس.

معلومات عن محمد معاذ
محمد معاذ شاب يمني من صنعاء تقريباً. يدرس في كلية علوم الحاسوب، وقريب من عالم البرمجة أكثر من أي شيء ثاني. أكثر لغة اشتغل عليها هي C++، ويحب يفهم الكود سطر سطر، خصوصاً الشروط والحلقات والدوال. إذا شاف كود ما يفهمه يجلس يحلله لين يفهمه بالكامل.
هو يبرمج باستخدام Visual Studio Code ومركب MinGW عشان يشغل برامج C++.
وعنده مواد في الجامعة مثل هياكل البيانات والتصميم المنطقي الرقمي.
الرياضيات ما هي أكثر شيء يحبه في الدراسة، وأحياناً يشوفها معقدة شوي، لكن يتعامل معها لأنها جزء من تخصصه.

اهتماماته
محمد معاذ فضولي بطبيعته. يحب يسأل عن أشياء كثيرة:
تقنية، سياسة، تاريخ، وحتى أسئلة غريبة أحياناً بس بدافع الفضول.
يتابع الأخبار السياسية أحياناً، ويتصفح الإنترنت كثير يبحث عن معلومات أو نقاشات.
وأحياناً يشاهد الأنمي، خصوصاً الأعمال الرومانسية أو الكوميدية.

شخصيته
محمد معاذ يحب النقاش والجدال الفكري.
ما يحب المجاملات الزائدة، ويفضل الكلام المباشر والصريح.
أحياناً يمزح في كلامه، وأحياناً يكون جاد حسب الموضوع.
لو دخل نقاش غالباً يحاول يفهم الفكرة كاملة قبل ما يقتنع فيها.

أسلوب الرد
البوت يتكلم باللهجة اليمنية العامية.
الردود تكون طبيعية ومختصرة، مثل كلام الناس.
مثال كلمات يستخدمها:
ايش - اشتي - ماشي - والله - ياخي.

الأسئلة الشخصية
إذا أحد سأل عن حياة محمد معاذ العاطفية أو أشياء شخصية جداً، البوت يرد بطريقة ساخرة مثل:
"ياخي مالك دخل 😂"
"هذا سري مهني."
"ركز في حياتك واترك محمد معاذ بحاله."
"""

user_histories = {}

def ask_ai(user_id, user_message):
    try:
        if user_id not in user_histories:
            user_histories[user_id] = []

        user_histories[user_id].append({
            "role": "user",
            "content": user_message
        })

        messages = user_histories[user_id][-10:]

        response = client.chat.completions.create(
            model="mistralai/mistral-small-3.1-24b-instruct:free",
            messages=[
                {"role": "system", "content": MUATH_INFO},
                *messages
            ],
            max_tokens=1024,
            temperature=0.9,
        )

        reply = response.choices[0].message.content

        user_histories[user_id].append({
            "role": "assistant",
            "content": reply
        })

        if len(user_histories[user_id]) > 20:
            user_histories[user_id] = user_histories[user_id][-20:]

        return reply

    except Exception as e:
        return f"عذراً، حدث خطأ: {str(e)} 🔄"

@bot.message_handler(commands=["start"])
def start(message):
    name = message.from_user.first_name or "صديقي"
    text = (
        f"أهلاً {name}!\n\n"
        f"أنا بوت محمد معاذ 🤖\n"
        f"تقدر تسألني عن أي شيء يخصه، مثلاً:\n\n"
        f"• مين هو محمد معاذ؟\n"
        f"• ايش يدرس؟\n"
        f"• ايش اهتماماته؟\n"
        f"• ايش شخصيته؟\n\n"
        f"اسأل براحتك!"
    )
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=["clear"])
def clear(message):
    user_id = message.from_user.id
    if user_id in user_histories:
        del user_histories[user_id]
    bot.send_message(message.chat.id, "تم مسح المحادثة! ابدأ من جديد 😊")

@bot.message_handler(func=lambda m: True)
def handle_message(message):
    uid = message.from_user.id
    name = message.from_user.first_name or "مجهول"
    print(f"[{name}]: {message.text}")
    bot.send_chat_action(message.chat.id, "typing")
    reply = ask_ai(uid, message.text)
    print(f"[البوت]: {reply}")
    bot.send_message(message.chat.id, reply)

if __name__ == "__main__":
    print("✅ البوت يعمل الآن...")
    bot.infinity_polling(timeout=60, long_polling_timeout=60)