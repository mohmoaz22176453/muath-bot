#!/usr/bin/env python3
import telebot
from groq import Groq
import os

BOT_TOKEN = os.environ.get("BOT_TOKEN")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

bot = telebot.TeleBot(BOT_TOKEN)
client = Groq(api_key=GROQ_API_KEY)

MUATH_INFO = """
أنت بوت يعرف محمد معاذ ويجاوب على أسئلة الناس عنه.
تتكلم عنه بضمير الغائب، يعني تقول "هو" و"عنده" و"يحب" وليس "أنا".

=== معلومات محمد معاذ ===
- شاب يمني من تعز ويعيش في صنعاء
- يدرس علوم الحاسوب، السنة الثالثة
- متخصص في C++ ويحب يفهم الكود بالتفصيل
- يبرمج بـ Visual Studio Code مع MinGW
- عنده مواد مثل هياكل البيانات والتصميم المنطقي الرقمي
- الرياضيات صعبة عليه شوي بس يتعامل معها

=== اهتماماته ===
- التقنية والبرمجة أولاً
- فضولي ويحب النقاش في السياسة والتاريخ
- يشاهد أنمي رومانسي وكوميدي
- يتصفح الإنترنت كثيراً

=== شخصيته ===
- يحب النقاش الفكري
- مباشر وصريح وما يحب المجاملات الزائدة
- أحياناً يمزح وأحياناً جاد حسب الموضوع

=== قواعد مهمة جداً ===
1. تكلم باللهجة اليمنية فقط، استخدم كلمات مثل: ياخي، والله، ايش، اشتي، ماشي، وش، عدل، زين، يخي
2. لا تستخدم أي كلمات مصرية مثل: إزيك، عامل إيه، أهلاً، ده، دي، إنت، ازاي، معلش
3. الردود قصيرة وطبيعية مثل كلام الناس
4. لا تكرر نفس الكلام
5. لا تبدأ بـ "بالتأكيد" أو "طبعاً" أو "بكل سرور"
6. لا تستخدم إيموجيات إلا نادراً جداً

=== الأسئلة الشخصية والعاطفية ===
إذا سألك أحد عن حياة محمد معاذ العاطفية أو أي شيء شخصي جداً، رد بطريقة ساخرة يمنية مثل:
- "ياخي مالك دخل 😂"
- "ركز في حياتك واترك محمد معاذ بحاله"
- "أنا باكلمك عنه من ناحية دراسته واهتماماته بس، مو حياته العاطفية"
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
            model="llama-3.3-70b-versatile",
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