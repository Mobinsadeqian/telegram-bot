import requests
from bs4 import BeautifulSoup
from telegram import Update
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

token = "YOUR TOKEN"

KNOWN_BRANDS = ["Apple", "Samsung", "Google"]

async def start(update : Update, context : ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("""
سلام به ربات قیمت گوشی‌ها خوش آمدید

برای دریافت منوی برندها روی گزینه /brand  برندها کلیک کنید
                                    """)


async def brand(update : Update, context : ContextTypes.DEFAULT_TYPE):
    brands = [KNOWN_BRANDS]
    reply_markup = ReplyKeyboardMarkup(brands, resize_keyboard=True, one_time_keyboard=True)
    await update.message.reply_text("یکی از برندها را انتخاب کنید: ", reply_markup= reply_markup)

def get_price_apple():
    url = "https://www.mobile.ir/phones/prices-brand-7-apple.aspx"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    price = soup.find_all("td", attrs= {"class" : ["price"]})
    all_prices = []

    for i in price:
        all_prices.append(i.text.strip())

    models = soup.find_all("a", attrs= {"class" : ["phone"]})

    all_models = []

    for i in models:
        all_models.append(i.text.strip())
    return all_models, all_prices

def get_price_samsung():
    url = "https://www.mobile.ir/phones/prices-brand-2-samsung.aspx?terms=&brandid=2&provinceid=&duration=14&price_from=-1&price_to=-1&shopid=&pagesize=200&sort=date&dir=desc&submit=%D8%AC%D8%B3%D8%AA%D8%AC%D9%88"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    price = soup.find_all("td", attrs= {"class" : ["price"]})
    all_prices = []

    for i in price:
        all_prices.append(i.text.strip())

    models = soup.find_all("a", attrs= {"class" : ["phone"]})

    all_models = []

    for i in models:
        all_models.append(i.text.strip())
    return all_models, all_prices

def get_price_google():
    url = "https://www.mobile.ir/phones/prices-brand-118-google.aspx"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    price = soup.find_all("td", attrs= {"class" : ["price"]})
    all_prices = []

    for i in price:
        all_prices.append(i.text.strip())

    models = soup.find_all("a", attrs= {"class" : ["phone"]})

    all_models = []

    for i in models:
        all_models.append(i.text.strip())
    return all_models, all_prices

apple_models = [ 
    ["Apple iPhone 13"], ["Apple iPhone 14"], ["Apple iPhone 16", "Apple iPhone 16 Pro", "Apple iPhone 16 Pro Max", "Apple iPhone 16e"], 
    ["Apple iPhone 17", "Apple iPhone 17 Pro", "Apple iPhone 17 Pro Max"]
]

samsung_models = [
    ["Samsung Galaxy A17 4G", "Samsung Galaxy A56", "Samsung Galaxy A07 4G", "Samsung Galaxy A26", "Samsung Galaxy A16", "Samsung Galaxy A55"], 
    ["Samsung Galaxy A36", "Samsung Galaxy A06", "Samsung Galaxy A05s", "Samsung Galaxy A05", "Samsung Galaxy A35", "Samsung Galaxy A15"
    ],
    [
      "Samsung Galaxy S24 FE", "Samsung Galaxy S24 Ultra", "Samsung Galaxy S24+"
    ],
    [
      "Samsung Galaxy S25 Edge", "Samsung Galaxy S25 Ultra", "Samsung Galaxy S25+", "Samsung Galaxy S25"  
    ],
    [
        "Samsung Galaxy Z Flip7", "Samsung Galaxy Z Fold7", "Samsung Galaxy Z Flip6", "Samsung Galaxy Z Fold6", "Samsung Galaxy Z Fold5"
    ]

]

google_models = [
    ["Google Pixel 7 Pro"],
    ["Google Pixel 8 Pro", "Google Pixel 8a", "Google Pixel 8"],
    ["Google Pixel 9 Pro", "Google Pixel 9a", "Google Pixel 9 Pro XL", "Google Pixel 9"]
]





async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    if user_message in KNOWN_BRANDS:
        context.user_data["brand"] = user_message

        if user_message == "Apple":
            keyboard = apple_models
        elif user_message == "Samsung":
            keyboard = samsung_models
        elif user_message == "Google":
            keyboard = google_models    
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
        await update.message.reply_text("عالی! حالا یکی از مدل‌ها را انتخاب کنید:", reply_markup=reply_markup)
        return

    selected_brand = context.user_data.get("brand")
    selected_model = user_message

    if not selected_brand:
        await update.message.reply_text("لطفاً ابتدا با دستور /brand یک برند را انتخاب کنید.")
        return

    models =[]
    prices =[]

    if selected_brand == "Apple":
        models, prices = get_price_apple()
    elif selected_brand == "Samsung":
        models, prices = get_price_samsung()
    elif selected_brand == "Google":
        models, prices = get_price_google()    


    if selected_model in models:
        index = models.index(selected_model)
        price = prices[index]
        # بعد از نمایش قیمت، کیبورد را حذف می‌کنیم
        await update.message.reply_text(f"""قیمت مدل {selected_model}:\n\n {price} 💰    

برای انتخاب مدل دیگر از دستور  /brand  استفاده کنید""", reply_markup=ReplyKeyboardRemove())
    else:
        # اگر مدل پیدا نشد
        await update.message.reply_text("متاسفانه این مدل پیدا نشد. لطفاً دوباره از منوی /brand شروع کنید.")    

        

def main():
    app = Application.builder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("brand", brand))

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("✅ ربات روشن شد و آماده دریافت پیام‌هاست...")
    app.run_polling()

if __name__ == "__main__":
    main()
