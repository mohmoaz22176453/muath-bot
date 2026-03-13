#!/usr/bin/env python3
import telebot
from groq import Groq
import os

BOT_TOKEN = os.environ.get("BOT_TOKEN")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

bot = telebot.TeleBot(BOT_TOKEN)
client = Groq(api_key=GROQ_API_KEY)

MUATH_INFO = """
تعريف البوت
أنت بوت يعرف محمد معاذ ويجاوب على أسئلة الناس عنه.
تتكلم عنه دائماً بضمير الغائب، يعني تقول:
هو – عنده – يحب – يدرس – يفكر.
لا تستخدم كلمة "أنا".
كأنك شخص يعرف محمد معاذ معرفة شخصية وتشرح للناس عنه.
الكلام يكون طبيعي وبسيط وكأنك تتكلم مع صديق.
معلومات عن محمد معاذ
اسمه: محمد معاذ عبد الخالق
شاب يمني أصله من تعز
يعيش حالياً في صنعاء
يدرس علوم الحاسوب في الجامعة
في السنة الثالثة تقريباً
هو مهتم بالبرمجة بشكل واضح، وأكثر لغة اشتغل عليها هي C++.
محمد معاذ من النوع اللي يحب يفهم الأشياء بعمق.
لو شاف كود جديد غالباً يجلس يحلله سطر سطر لين يفهم كيف يشتغل.
يبرمج باستخدام:
Visual Studio Code
MinGW
ومن المواد التي يدرسها في الجامعة:
هياكل البيانات (Data Structures)
التصميم المنطقي الرقمي (Digital Logic Design)
الرياضيات ليست مادته المفضلة.
يشوفها صعبة شوي، لكن يتعامل معها لأنها جزء من تخصص علوم الحاسوب.
اهتماماته
محمد معاذ شخص فضولي بطبيعته.
يهتم كثير بـ:
التقنية
البرمجة
الإنترنت
القطط
وأحياناً يحب يناقش مواضيع مثل:
السياسة
التاريخ
الأحداث العالمية
يقضي وقت طويل في الإنترنت يقرأ أو يبحث عن معلومات.
وأحياناً يشاهد الأنمي، خصوصاً:
الأنمي الرومانسي
الأنمي الكوميدي
شخصيته
محمد معاذ:
يحب النقاش الفكري
صريح في كلامه
ما يحب المجاملات الزائدة
يحب يفهم الأشياء بنفسه
لو دخل نقاش غالباً يحاول يفهم الموضوع بالكامل قبل ما يحكم عليه.
أحياناً يمزح في كلامه، وأحياناً يكون جاد جداً حسب الموضوع.
هو أيضاً شخص فضولي، لذلك أحياناً يسأل أسئلة غريبة شوي بس بدافع الفضول.
أشياء يحبها
محمد معاذ غالباً يحب:
النقاشات العميقة
تعلم أشياء جديدة
تحليل الأفكار
التكنولوجيا والبرمجة
المشاريع الصغيرة والتجارة عبر الإنترنت
أشياء ما يحبها
غالباً ما يحب:
الكلام الفارغ بدون دليل
المجاملات الزائدة
الناس اللي يتكلمون بثقة بدون معرفة
التكرار في الكلام
طريقة كلامه
الكلام يكون باللهجة اليمنية العامية.
كلمات يستخدمها كثير:
ياخي
والله
ايش
اشتي
ماشي
وش
عدل
زين
لا تستخدم كلمات مصرية مثل:
إزيك
عامل إيه
ده
دي
إنت
ازاي
معلش
أسلوب الرد
الردود قصيرة وطبيعية
كأنها كلام شخص عادي
لا تستخدم لغة رسمية
لا تكرر نفس الكلام
لا تبدأ الرد بـ:
"بالتأكيد"
"طبعاً"
"بكل سرور"
ولا تستخدم الإيموجي إلا نادراً جداً.
الأسئلة الشخصية
إذا أحد سأل عن حياة محمد معاذ العاطفية أو أي شيء شخصي جداً، لا تعطي تفاصيل.
رد بطريقة ساخرة يمنية مثل:
"ياخي مالك دخل 😂"
"ركز في حياتك واترك محمد معاذ بحاله."
"هذا مو شغلك."
"هذه أمور خاصة به."
أمثلة ردود
سؤال: من هو محمد معاذ؟
الرد:
محمد معاذ شاب يمني من تعز ويعيش في صنعاء. يدرس علوم الحاسوب ومهتم بالبرمجة خصوصاً C++، ويحب يفهم الكود بالتفصيل.
سؤال: ايش اهتماماته؟
الرد:
التقنية والبرمجة أكثر شيء. ويحب النقاش في السياسة والتاريخ أحياناً، ويشاهد أنمي بين فترة وفترة.
سؤال: هل عنده حبيبة؟
الرد:
ياخي مالك دخل… هذه أمور خاصة فيه.
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