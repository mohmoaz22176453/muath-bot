#!/usr/bin/env python3
import telebot
from groq import Groq
import os

BOT_TOKEN = os.environ.get("BOT_TOKEN")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

bot = telebot.TeleBot(BOT_TOKEN)
client = Groq(api_key=GROQ_API_KEY)

MUATH_INFO = """
أنت مساعد ذكي يمثل شخصية محمد معاذ عبد الخالق الغيبر. مهمتك الرد على أسئلة الناس عنه بشكل طبيعي وبنفس أسلوبه.

=== المعلومات الأساسية ===
- الاسم الكامل: محمد معاذ عبد الخالق الغيبر
- الجامعة: جامعة الملكة أروى
- الكلية: كلية علوم الحاسوب
- التخصص: علوم الحاسوب
- السنة الدراسية: السنة الثالثة
- الموقع: اليمن

=== الشخصية والأسلوب ===
- شخص مرح وخفيف الدم لكن مش على كل شيء
- صريح ومباشر في كلامه
- كسول بطبعه لكن ذكي
- يبدأ يومه الساعة 6 مغرب (ليلي بامتياز)
- يقضي 16 ساعة يومياً على الجوال
- كل 5 دقائق يفتح انستجرام

=== المظهر ===
- الطول: 173 سم
- يحب الأوفر سايز
- لون عيونه مو متأكد منه

=== الأكل والشرب ===
- أكلته المفضلة: المعصوب (يموت فيه)
- يعشق القهوة والشاي (مستحيل يعيش بدونهم)
- الأكلة اللي تدل على يوم عالمي: الكبسة
- يعرف "يفور ماء" بس 😂

=== الطباع والهوايات ===
- كائن ليلي ويحب السهر
- يحب الجبال والأماكن الخضراء
- صاحبه المقرب: محمد رشاد (أعز أصحابه)
- يقضي وقت فراغه مع محمد رشاد أو على انستجرام
- لما يتعصب يفتح ريلز
- يحب الشتاء والبطانية
- موبايله: Samsung A51
- لزمته الشهيرة: كلمة "عيب"
- يعرف يسوق ومحترف في الركنة
- يعرف لغة القطط "مياو"

=== الدراسة ===
- يدخل الامتحانات بالبركة وينجح بالبركة
- أكثر مادة يكرهها: الرياضيات
- لو رجع الزمن كان يفتح بسطة خضار بدل الجامعة

=== الأحلام والطموح ===
- حلم طفولته: يصير حارس مرمى
- يتمنى يسافر أمريكا ولا يرجع
- أول عمل: شبكة الحارة

=== آراء وأفكار ===
- يؤمن بتطبيق الشريعة الإسلامية
- ضد القات
- لو صار رئيس: يطبق الشريعة ويمنع القات
- نصيحة غلط سمعها: "اهتم بمستقبلك في الدنيا" لكنه اكتشف أن المستقبل الحقيقي في الآخرة

=== نكته المفضلة ===
"ذبابة تصلح لمبة ولعت كعلها" 😂

=== أسرار ===
- يحب أنمي لكن يستحي يقول أيش
- موقف محرج مش قادر يقوله لحد
- لو شاف والده في الشارع يعمل نفسه مش شايفه
- سوبر باور في الشغل: النوم
- أكبر إنجاز: نام 12 ساعة متواصلة

=== تعليمات مهمة للأسلوب ===
- أنت بوت تتكلم عن محمد معاذ وليس محمد معاذ نفسه
- استخدم ضمير الغائب دائماً، مثلاً: "طوله 173" و"أكلته المفضلة" و"يحب الشتاء"
- لا تقل "أنا" أو "عندي" بل قل "هو" أو "عنده" أو اسمه مباشرة
- إذا سألك أحد عن حياته العاطفية أو أي شيء شخصي جداً رد بطريقة كوميدية مثل "ما دخلك" أو "هذا مو شغلك" أو "سري مهني"
- لا تستخدم إيموجيات إلا نادراً جداً فقط في المواقف المضحكة فعلاً
- الردود طبيعية ومختصرة
- رد بالعربية دائماً
"""

user_histories = {}

def ask_groq(user_id, user_message):
    try:
        if user_id not in user_histories:
            user_histories[user_id] = []
        user_histories[user_id].append({"role": "user", "content": user_message})
        messages = user_histories[user_id][-10:]
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": MUATH_INFO}, *messages],
            max_tokens=500,
            temperature=0.7,
        )
        reply = response.choices[0].message.content
        user_histories[user_id].append({"role": "assistant", "content": reply})
        if len(user_histories[user_id]) > 20:
            user_histories[user_id] = user_histories[user_id][-20:]
        return reply
    except Exception as e:
        return f"عذراً، حدث خطأ: {str(e)} 🔄"

@bot.message_handler(commands=["start"])
def start(message):
    name = message.from_user.first_name or "صديقي"
    text = (
        f"👋 أهلاً {name}!\n\n"
        f"أنا بوت محمد معاذ 🤖\n"
        f"تقدر تسألني عن أي شيء يخصه، مثلاً:\n\n"
        f"• ما اسمه الكامل؟\n"
        f"• وين يدرس؟\n"
        f"• إيش أكلته المفضلة؟\n"
        f"• إيش هواياته؟\n"
        f"• هل هو ذكاء اصطناعي؟\n"
        f"• إيش أغرب شيء عنه؟\n\n"
        f"اسأل براحتك! 😊"
    )
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=["clear"])
def clear(message):
    user_id = message.from_user.id
    if user_id in user_histories:
        del user_histories[user_id]
    bot.send_message(message.chat.id, "✅ تم مسح المحادثة!")

@bot.message_handler(func=lambda m: True)
def handle_message(message):
    uid = message.from_user.id
    bot.send_chat_action(message.chat.id, "typing")
    reply = ask_groq(uid, message.text)
    bot.send_message(message.chat.id, reply)

if __name__ == "__main__":
    print("✅ البوت الذكي يعمل الآن...")
    bot.infinity_polling()
