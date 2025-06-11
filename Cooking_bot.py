from openai import OpenAI
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

bot = telebot.TeleBot("7553369898:AAGCyBP7BQ6Oyfo7mWVCpbnWzEbR06IFw-0")
client = OpenAI(
    base_url= "https://openrouter.ai/api/v1",
    api_key= "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",
)
user_id_chanels = [-1002267991061]
user_has_joined = {}
name_chanel = ["studio_code_313"]
user_id = ""
# بررسی عضویت کاربر در کانال
def check_all_channels(user_id):
    for ch in user_id_chanels:
            try:
                status = bot.get_chat_member(ch, user_id).status
                print(f"[DEBUG] وضعیت عضویت کاربر {user_id} در {ch}: {status}")
                if status not in ("member", "administrator", "creator"):
                    return False
            except Exception as e:
                print(f"[ERROR] بررسی عضویت در {ch} برای کاربر {user_id} شکست خورد: {e}")
                return False
            return True


def is_admin(user_id):
    # لیست ID ادمین ها را در اینجا وارد کنید
    admin_ids = [5163330529]
    return user_id in admin_ids
# response = client.chat.completions.create(
#     model="deepseek/deepseek-r1-0528:free",
#     messages=[{"role": "user", "content": user_input}],
#     temperature= 0.5
# )

# print(response.choices[0].message.content)


@bot.message_handler(commands=["admin_panel"])
def adminpanel(message):
    if is_admin(user_id=message.from_user.id):
        markup = InlineKeyboardMarkup()
        btn2 = InlineKeyboardButton("اضافه کردن چنل تبلیغاتی.", callback_data="ad_chanel")
        btn3 = InlineKeyboardButton("حذف چنل تبلیغاتی.", callback_data="remove_adchanel")
        markup.add(btn2)
        markup.add(btn3)
        bot.send_message(message.chat.id, "به پنل ادمین خوش اومدی.", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "شما دسترسی به این ویژگی را ندارید.")


@bot.message_handler(commands=["start"])
def start_chef (message):
    print(user_id)
    text = """
🍽️ به ربات شِف کوچولو خوش اومدی!

👨‍🍳 اینجا جاییه که با چند تا ماده‌ی ساده، می‌تونی کلی غذای خوشمزه کشف کنی!

سه تا کار می‌تونم برات انجام بدم:

1️⃣ مواد غذایی داری؟ بگو چی داری، من بهت می‌گم چی می‌تونی باهاش درست کنی.
2️⃣ یه غذا تو ذهنت هست؟ اسمشو بهم بگو، منم قدم به قدم طرز تهیه‌شو می‌گم.
3️⃣ اطلاعات عمومیت راجب غذا کمه؟ بهم بگو راجب هر غذا چی میخوای بدونی تا بهت بگم.
🍅🥔🍳🥦 فرقی نمی‌کنه چند تا ماده داری، مهم اینه که دست‌پختت قراره خوشمزه بشه!

حالا بگو ببینم با چی شروع می‌کنیم؟ 😋"""
    if user_has_joined.get(user_id, True):
       markup = InlineKeyboardMarkup()
       btn1 = InlineKeyboardButton(text= "پیشنهاد غذا با موادت👨‍🍳🍳", callback_data="food_offer")
       btn2 = InlineKeyboardButton(text= "دستور پخت📜🍲", callback_data="recipe")
       btn3 = InlineKeyboardButton(text="حرف زدن راجب غذا💬🍖", callback_data="talking")
       markup.add(btn1, btn2)
       markup.add(btn3)
       bot.send_message(message.chat.id, text, reply_markup=markup)
    else:
        markup = InlineKeyboardMarkup()
        for chanel in name_chanel:
            btn = InlineKeyboardButton(text=chanel.replace("@", " "), url=f"https://t.me/{chanel.replace("@", "")}")
            markup.add(btn)
        join_btn = InlineKeyboardButton(text="عضو شدم.", callback_data="join")
        markup.add(join_btn)
        bot.send_message(message.chat.id, "لطفاً برای ادامه و کار با ربات، ابتدا در کانال زیر عضو شو:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    text = """🍽️ حرف بزن با باتِ شِف کوچولو!

تو این قسمت می‌تونی هرچی دلت خواست درباره غذا بپرسی یا گپ بزنی!
از این که غذای محبوب یه کشور چیه، تا اینکه چی‌کار کنی قرمه‌سبزیت جا بیفته 😋
می‌تونی بپرسی:

– غذای معروف ترکیه چیه؟
– چجوری پاستا رو خوش‌طعم‌تر کنم؟
– بهترین ادویه برای مرغ چیه؟
– یا حتی بپرسی: باقلا قاتق از کجاست؟ 

آشپز دیجیتال همیشه آماده‌ست برای یه گفت‌و‌گوی خوشمزه! 😄
و در ضمن هر وقت خواستی چتت رو با من تموم کنی فقطط لازمه بگی (کافیه)😄👍"""
    text2 = """🍽️ دستور پخت غذا
هر غذایی که دلت می‌خواد بپز، فقط اسمشو بفرست! دستور پختش رو سریع و آسون برات می‌فرستم👨‍🍳🍱
و در ضمن هر وقت خواستی چتت رو با من تموم کنی فقطط لازمه بگی (کافیه)😄👍"""
    user_id = call.from_user.id
    print(user_id)
    if call.data == "join":
        if check_all_channels(user_id):
            bot.delete_message(call.message.chat.id, call.message.message_id)
            user_has_joined[user_id] = True
            print(f"[DEBUG] user_has_joined[{user_id}] = {user_has_joined[user_id]}")
            start_chef(call.message)
        else:
            bot.send_message(call.message.chat.id, "لطفا ابتدا در تمام چنل ها عضو بشید.")
    elif call.data == "talking":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, text)
        bot.register_next_step_handler(call.message, talking)
    elif call.data == "recipe":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, text2)
        bot.register_next_step_handler(call.message, recipe)
    elif call.data == "food_offer":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, text2)
        bot.register_next_step_handler(call.message, food_offer)

def food_offer(message):
    text = message.text
    system_text = """تو یه اشپز حرفه ای هستی که اسمت شِف کوچولو هست؛
فقط به سوالات مربوط به پیشنهاد دادن غذا جواب بده 
مثل:
با گوجه و تخم مرغ چه چبزی میتونم درست کنم و سوالای اینشکلی؛
به سوالای مربوط به دستور پخت یا سوالات عمومی راجب غذا جواب نده؛
مثال:
۱- غذا های معروف ایتالیا چی هستن؟
به این نوع سوالات جواب نده؛
۲- دستور پخت پاستا الفردو رو بهم بده.
به این نوع سوالاتم جواب نده؛
همیشه کوتاه و مختصرو مفید کواب بده با لحن صمیمانه و از در ایموجی  هم استفاده کن."""
    bot.send_chat_action(message.chat.id, 'typing')
    messagee=[
        {"role": "system", "content": system_text},
        {"role": "user", "content": text}
        ]
    if text == "کافیه":
        bot.send_message(message.chat.id, "خوشحال شدم از حرف زدن باهات😄")
    else:
        response = client.chat.completions.create(
     model="deepseek/deepseek-r1-0528:free",
     messages=messagee,
     temperature= 0.5
        )
        bot.send_message(message.chat.id, response.choices[0].message.content)
        bot.register_next_step_handler(message, food_offer)

def talking(message):
    text = message.text
    system_text = """تو یه آشپز حرفه ای هستی که اسمت شِف کوچولو هست؛
فقط به سوالات عمومی اشپزی جواب بده و به سوالات مربوغبه دستور پخت و یا پیشنهاد غذا پاسخ نده برای مثال:
۱- اولین بار چه کشوری پیتزا رو درست کرد؟
به این نوع سوال جواب بده 
۲- با تخم مرغ و گوجه چه غذاهایی میتونم درست کنم و دستور پخت اون رو بهم بده.
به این نوع سپالات جواب نده؛
همیشه کوتاه مختصر و مفید حواب بده و لحن صمیمانه ای داشته باش و از ایموجیاستفاده کن."""
    bot.send_chat_action(message.chat.id, 'typing')
    messagee=[
        {"role": "system", "content": system_text},
        {"role": "user", "content": text}
        ]
    if text == "کافیه":
        bot.send_message(message.chat.id, "خوشحال شدم از حرف زدن باهات😄")
    else:
        response = client.chat.completions.create(
     model="deepseek/deepseek-r1-0528:free",
     messages=messagee,
     temperature= 0.7
        )
        bot.send_message(message.chat.id, response.choices[0].message.content)
        bot.register_next_step_handler(message, talking)

def recipe(message):
    text = message.text
    system_text = """تو یه آشپز حرفه ای هستی که اسمت شِف کوچولو هست؛
فقط به سوالات مربوط به دستور پخت جواب بده
مثال:
۱ـ با دستور پخت پاستا الفردو رو بهم بده.
به این نوع سوالات جواب بده
۲-راجب پاستا الفردو توضیح بده و اولین بار کجا درست شد؟
به این نوع سوالات جواب نده
۳ـ با گوجه و تخم مرغ چی میتونم درست کنم؟
به این نوع سوالات جواب نده؛
همیشه کوتاه مختصر و کار امد جواب بده لحن صمیمانه ای داشته باش و از ایموجی استفاده کن."""
    bot.send_chat_action(message.chat.id, 'typing')
    messagee=[
        {"role": "system", "content": system_text},
        {"role": "user", "content": text}
        ]
    if text == "کافیه":
        bot.send_message(message.chat.id, "خوشحال شدم از حرف زدن باهات😄")
    else:
        response = client.chat.completions.create(
     model="deepseek/deepseek-r1-0528:free",
     messages=messagee,
     temperature= 0.4
        )
        bot.send_message(message.chat.id, response.choices[0].message.content)
        bot.register_next_step_handler(message, recipe)
print("bot is ready")

try:
    chat = bot.get_chat_member(user_id_chanels, 5163330529)  # اسم درست کانالت
    print("✅ get_chat موفق:", chat.status)
except Exception as e:
    print("❌ get_chat شکست خورد:", e)
bot.polling()