import telebot
from telebot import types
import os
import random
import sys
import requests
import time
import config
from threading import Thread
import re
import json
from SimpleQIWI import *
bot = telebot.TeleBot(config.token)


key = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
key.row('✅Заказать','📊 Статистика')
key.row('⚠F.A.Q.','📋 Пользовательское соглашение')
#key.row('F.A.Q.')



menu = types.InlineKeyboardMarkup() #наша клавиатура
menu.add(types.InlineKeyboardButton(text='📱 VK 📱', callback_data='1'))
menu.add(types.InlineKeyboardButton(text='📷 Инста 📷', callback_data='2'))
menu.add(types.InlineKeyboardButton(text='📩 Telegram 📩', callback_data='3'),types.InlineKeyboardButton(text='🔑 Steam 🔑', callback_data='4'))
menu.add(types.InlineKeyboardButton(text='👨‍👩‍👦 Семейный 👨‍👩‍👦', callback_data='5'),types.InlineKeyboardButton(text='⭐ PREMIUM ⭐', callback_data='6'))

@bot.message_handler(commands=["start"])
def cmd_start(message):
  f = 0
  bd = [line.rstrip('\n') for line in open('f.txt', encoding='utf-8')]
  for line in bd:
    if str(message.chat.id) in line:
      f = 1
  if f == 1:
    bot.send_message(message.chat.id,config.start,reply_markup=key)
  else:
    log_file = open('f.txt', 'a', encoding="utf-8")
    log_file.write(str(message.chat.id)+'\n')
    log_file.close
    bot.send_message(message.chat.id, config.start, parse_mode="Markdown",reply_markup=key)

@bot.message_handler(commands=["balance"])
def balance(message):
    if message.chat.id in config.admins:
      try:
        api = QApi(token=config.QIWI_TOKEN, phone=config.QIWI_ACCOUNT)
        bot.send_message(message.chat.id, text=str(api.balance)+' рублей')
      except Exception as e:
        print(e)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(message):
    opl = telebot.types.InlineKeyboardMarkup()
    opl.add(telebot.types.InlineKeyboardButton(text='Проверить оплату', callback_data='check'),telebot.types.InlineKeyboardButton(text='Назад', callback_data='pay'))
    if message.data == "pay":
        bot.edit_message_text(chat_id=message.message.chat.id, message_id=message.message.message_id, text= f'''
Наши товары:
VK *{config.sum[0]}* руб.
Инста *{config.sum[1]}* руб.
Telegram *{config.sum[2]}* руб.)
Steam *{config.sum[3]}* руб.
Premium *{config.sum[4]}* руб.
Elite *{config.sum[5]}* руб.
                ''', parse_mode="Markdown",reply_markup=menu)
    elif message.data == 'check':
        a = 0
        tarif = 0
        b = 0
        f = 0
        bd = [line.rstrip('\n') for line in open('payd.txt', encoding='utf-8')]
        for line in bd:
          if str(message.message.chat.id) in line:
            f = 1
        if f != 1:
            s = requests.Session()
            s.headers['authorization'] = 'Bearer ' + config.QIWI_TOKEN
            parameters = {'rows': '2'}
            h = s.get('https://edge.qiwi.com/payment-history/v1/persons/'+ str(config.QIWI_ACCOUNT) +'/payments', params = parameters)
            req = json.loads(h.text)
            #print(req)
            random_code = str(message.message.chat.id)
            #print(random_code)
            summ = 0
            for i in range(len(req['data'])):
              if req['data'][i]['personId'] == config.QIWI_ACCOUNT:
                if req['data'][i]['comment'] == random_code and req['data'][i]['sum']['currency'] == 643:
                  if req['data'][i]['sum']['amount'] == config.sum[0]:
                    a = req['data'][i]
                    tarif = 0
                    summ = config.sum[0]
                  elif req['data'][i]['sum']['amount'] == config.sum[1]:
                    a = req['data'][i]
                    tarif = 1
                    summ = config.sum[1]
                  elif req['data'][i]['sum']['amount'] == config.sum[2]:
                    a = req['data'][i]
                    tarif = 2
                    summ = config.sum[2]
                  elif req['data'][i]['sum']['amount'] == config.sum[3]:
                    a = req['data'][i]
                    tarif = 3
                    summ = config.sum[3]
                  elif req['data'][i]['sum']['amount'] == config.sum[3]:
                    a = req['data'][i]
                    tarif = 4
                    summ = config.sum[4]
                  elif req['data'][i]['sum']['amount'] == config.sum[3]:
                    a = req['data'][i]
                    tarif = 5
                    summ = config.sum[5]

        else:
            bot.answer_callback_query(callback_query_id=message.id, show_alert=False, text="Попробуйте еще раз через пару минут")
            return
        f = 0
        tovar = 0
        if a != 0:
            bd = [line.rstrip('\n') for line in open('pay.txt', encoding='utf-8')]
            if str(a['txnId']) in bd:
                f = 1
            if f != 1:
                if tarif == 0:
                    bd = [line.rstrip('\n') for line in open('DATA/1.txt', encoding='utf-8')]
                    tovar = random.choice(bd)
                    bot.send_message(message.message.chat.id,f'''
*ОПЛАТА ПРОШЛА УСПЕШНО*

Ваш товар `{tovar}`''', parse_mode="Markdown")
                elif tarif == 1:
                    bd = [line.rstrip('\n') for line in open('DATA/2.txt', encoding='utf-8')]
                    tovar = random.choice(bd)
                    bot.send_message(message.message.chat.id,f'''
*ОПЛАТА ПРОШЛА УСПЕШНО*

Ваш товар `{tovar}`''', parse_mode="Markdown")
                elif tarif == 2:
                    bd = [line.rstrip('\n') for line in open('DATA/3.txt', encoding='utf-8')]
                    tovar = random.choice(bd)
                    bot.send_message(message.message.chat.id,f'''
*ОПЛАТА ПРОШЛА УСПЕШНО*

Ваш товар `{tovar}`''', parse_mode="Markdown")
                elif tarif == 3:
                    bd = [line.rstrip('\n') for line in open('DATA/4.txt', encoding='utf-8')]
                    tovar = random.choice(bd)
                    bot.send_message(message.message.chat.id,f'''
*ОПЛАТА ПРОШЛА УСПЕШНО*

Ваш товар `{tovar}`''', parse_mode="Markdown")
                elif tarif == 4:
                    bd = [line.rstrip('\n') for line in open('DATA/5.txt', encoding='utf-8')]
                    tovar = random.choice(bd)
                    bot.send_message(message.message.chat.id,f'''
*ОПЛАТА ПРОШЛА УСПЕШНО*

Ваш товар `{tovar}`''', parse_mode="Markdown")

                elif tarif == 5:
                    bd = [line.rstrip('\n') for line in open('DATA/6.txt', encoding='utf-8')]
                    tovar = random.choice(bd)
                    bot.send_message(message.message.chat.id,f'''
*ОПЛАТА ПРОШЛА УСПЕШНО*

 Ваш товар `{tovar}`''', parse_mode="Markdown")
                idd = bot.send_message(message.message.chat.id,f'Среднее время выполнения заказа в данный момент 12-13часов')
                bot.register_next_step_handler(idd, vvod)
                pattern = re.compile(re.escape(str(tovar)))
                with open(f'DATA/{str(tarif+1)}.txt', 'r+', encoding="utf-8") as f:
                    lines = f.readlines()
                    f.seek(0)
                    for line in lines:
                        result = pattern.search(line)
                        if result is None:
                            f.write(line)
                        f.truncate()
                zaz = Thread(target=zad, args=(message.message.chat.id,), daemon=True)
                zaz.start()
                for i in config.admins:
                    try:
                        bot.send_message(i,f'{message.message.chat.id} купил товар за {summ} рублей')
                    except:
                        pass
            else:
                log_file = open('payd.txt', 'a', encoding="utf-8")
                log_file.write(str(message.message.chat.id)+'\n')
                log_file.close
                pays = Thread(target=payw, args=(message.message.chat.id,), daemon=True)
                pays.start()
                bot.answer_callback_query(callback_query_id=message.id, show_alert=False, text="Платеж не обнаружен")
                return
            log_file = open('pay.txt', 'a', encoding="utf-8")
            log_file.write(str(a['txnId'])+'\n')
            log_file.close
        else:
            log_file = open('payd.txt', 'a', encoding="utf-8")
            log_file.write(str(message.message.chat.id)+'\n')
            log_file.close
            pays = Thread(target=payw, args=(message.message.chat.id,), daemon=True)
            pays.start()
            bot.answer_callback_query(callback_query_id=message.id, show_alert=False, text="Платеж не обнаружен")

    elif message.data == '1':
        bd = [line.rstrip('\n') for line in open('DATA/1.txt', encoding='utf-8')]
        if bd == []:
            bot.answer_callback_query(callback_query_id=message.id, show_alert=False, text="Товара нет в наличии")
        else:
            pay = types.InlineKeyboardMarkup() #наша клавиатура
            pay.add(types.InlineKeyboardButton(text='Приобрести', callback_data='p1'))
            pay.add(types.InlineKeyboardButton(text='Назад', callback_data='pay'))
            bot.edit_message_text(chat_id=message.message.chat.id, message_id=message.message.message_id, text=config.opis[0],reply_markup=pay)
    elif message.data == '2':
        bd = [line.rstrip('\n') for line in open('DATA/2.txt', encoding='utf-8')]
        if bd == []:
            bot.answer_callback_query(callback_query_id=message.id, show_alert=False, text="Товара нет в наличии")
        else:
            pay = types.InlineKeyboardMarkup() #наша клавиатура
            pay.add(types.InlineKeyboardButton(text='Приобрести', callback_data='p2'))
            pay.add(types.InlineKeyboardButton(text='Назад', callback_data='pay'))
            bot.edit_message_text(chat_id=message.message.chat.id, message_id=message.message.message_id, text=config.opis[1],reply_markup=pay)
    elif message.data == '3':
        bd = [line.rstrip('\n') for line in open('DATA/3.txt', encoding='utf-8')]
        if bd == []:
            bot.answer_callback_query(callback_query_id=message.id, show_alert=False, text="Товара нет в наличии")
        else:
            pay = types.InlineKeyboardMarkup() #наша клавиатура
            pay.add(types.InlineKeyboardButton(text='Приобрести', callback_data='p3'))
            pay.add(types.InlineKeyboardButton(text='Назад', callback_data='pay'))
            bot.edit_message_text(chat_id=message.message.chat.id, message_id=message.message.message_id, text=config.opis[2],reply_markup=pay)
    elif message.data == '4':
        bd = [line.rstrip('\n') for line in open('DATA/4.txt', encoding='utf-8')]
        if bd == []:
            bot.answer_callback_query(callback_query_id=message.id, show_alert=False, text="Товара нет в наличии")
        else:
            pay = types.InlineKeyboardMarkup() #наша клавиатура
            pay.add(types.InlineKeyboardButton(text='Приобрести', callback_data='p4'))
            pay.add(types.InlineKeyboardButton(text='Назад', callback_data='pay'))
            bot.edit_message_text(chat_id=message.message.chat.id, message_id=message.message.message_id, text=config.opis[3],reply_markup=pay)
    elif message.data == '5':
        bd = [line.rstrip('\n') for line in open('DATA/5.txt', encoding='utf-8')]
        if bd == []:
            bot.answer_callback_query(callback_query_id=message.id, show_alert=False, text="Товара нет в наличии")
        else:
            pay = types.InlineKeyboardMarkup() #наша клавиатура
            pay.add(types.InlineKeyboardButton(text='Приобрести', callback_data='p5'))
            pay.add(types.InlineKeyboardButton(text='Назад', callback_data='pay'))
            bot.edit_message_text(chat_id=message.message.chat.id, message_id=message.message.message_id, text=config.opis[4],reply_markup=pay)
    elif message.data == '6':
        bd = [line.rstrip('\n') for line in open('DATA/6.txt', encoding='utf-8')]
        if bd == []:
            bot.answer_callback_query(callback_query_id=message.id, show_alert=False, text="Товара нет в наличии")
        else:
            pay = types.InlineKeyboardMarkup() #наша клавиатура
            pay.add(types.InlineKeyboardButton(text='Приобрести', callback_data='p6'))
            pay.add(types.InlineKeyboardButton(text='Назад', callback_data='pay'))
            bot.edit_message_text(chat_id=message.message.chat.id, message_id=message.message.message_id, text=config.opis[5],reply_markup=pay)
    elif message.data == "p1":
        sum = config.sum[0]
        opl.add(telebot.types.InlineKeyboardButton('Оплатить', url=f'https://qiwi.com/payment/form/99?amountInteger={sum}\
&amountFraction=0&extra[%27account%27]={str(config.QIWI_ACCOUNT)}&extra\
[%27comment%27]={message.from_user.id}&blocked[1]=account&blocked[2]=comment&blocked[3]=sum'))
        bot.edit_message_text(chat_id=message.message.chat.id, message_id=message.message.message_id, text=f'''
➖➖➖➖➖➖➖➖➖➖
Информация об оплате
🥝 QIWI-кошелек: +{str(config.QIWI_ACCOUNT)}
📝 Комментарий к переводу: {message.from_user.id}
Сумма: {sum} руб.

➖➖➖➖➖➖➖➖➖➖
Внимание
Заполняйте номер телефона и комментарий при переводе внимательно!
После перевода воспользуйтесь кнопкой ниже!
Либо для воспользуйтесь кнопкой "Оплатить"
➖➖➖➖➖➖➖➖➖➖
''',reply_markup=opl)
    elif message.data == "p2":
        sum = config.sum[1]
        opl.add(telebot.types.InlineKeyboardButton('Оплатить', url=f'https://qiwi.com/payment/form/99?amountInteger={sum}\
&amountFraction=0&extra[%27account%27]={str(config.QIWI_ACCOUNT)}&extra\
[%27comment%27]={message.from_user.id}&blocked[1]=account&blocked[2]=comment&blocked[3]=sum'))
        bot.edit_message_text(chat_id=message.message.chat.id, message_id=message.message.message_id, text=f'''
➖➖➖➖➖➖➖➖➖➖
Информация об оплате
🥝 QIWI-кошелек: +{str(config.QIWI_ACCOUNT)}
📝 Комментарий к переводу: {message.from_user.id}
Сумма: {sum} руб.

➖➖➖➖➖➖➖➖➖➖
Внимание
Заполняйте номер телефона и комментарий при переводе внимательно!
После перевода воспользуйтесь кнопкой ниже!
Либо для воспользуйтесь кнопкой "Оплатить"
➖➖➖➖➖➖➖➖➖➖
''',reply_markup=opl)

    elif message.data == "p3":
        sum = config.sum[2]
        opl.add(telebot.types.InlineKeyboardButton('Оплатить', url=f'https://qiwi.com/payment/form/99?amountInteger={sum}\
&amountFraction=0&extra[%27account%27]={str(config.QIWI_ACCOUNT)}&extra\
[%27comment%27]={message.from_user.id}&blocked[1]=account&blocked[2]=comment&blocked[3]=sum'))
        bot.edit_message_text(chat_id=message.message.chat.id, message_id=message.message.message_id, text=f'''
➖➖➖➖➖➖➖➖➖➖
Информация об оплате
🥝 QIWI-кошелек: +{str(config.QIWI_ACCOUNT)}
📝 Комментарий к переводу: {message.from_user.id}
Сумма: {sum} руб.

➖➖➖➖➖➖➖➖➖➖
Внимание
Заполняйте номер телефона и комментарий при переводе внимательно!
После перевода воспользуйтесь кнопкой ниже!
Либо для воспользуйтесь кнопкой "Оплатить"
➖➖➖➖➖➖➖➖➖➖
''',reply_markup=opl)

    elif message.data == "p4":
        sum = config.sum[3]
        opl.add(telebot.types.InlineKeyboardButton('Оплатить', url=f'https://qiwi.com/payment/form/99?amountInteger={sum}\
&amountFraction=0&extra[%27account%27]={str(config.QIWI_ACCOUNT)}&extra\
[%27comment%27]={message.from_user.id}&blocked[1]=account&blocked[2]=comment&blocked[3]=sum'))
        bot.edit_message_text(chat_id=message.message.chat.id, message_id=message.message.message_id, text=f'''
➖➖➖➖➖➖➖➖➖➖
Информация об оплате
🥝 QIWI-кошелек: +{str(config.QIWI_ACCOUNT)}
📝 Комментарий к переводу: {message.from_user.id}
Сумма: {sum} руб.

➖➖➖➖➖➖➖➖➖➖
Внимание
Заполняйте номер телефона и комментарий при переводе внимательно!
После перевода воспользуйтесь кнопкой ниже!
Либо для воспользуйтесь кнопкой "Оплатить"
➖➖➖➖➖➖➖➖➖➖
''',reply_markup=opl)
    elif message.data == "p5":
        sum = config.sum[4]
        opl.add(telebot.types.InlineKeyboardButton('Оплатить', url=f'https://qiwi.com/payment/form/99?amountInteger={sum}\
&amountFraction=0&extra[%27account%27]={str(config.QIWI_ACCOUNT)}&extra\
[%27comment%27]={message.from_user.id}&blocked[1]=account&blocked[2]=comment&blocked[3]=sum'))
        bot.edit_message_text(chat_id=message.message.chat.id, message_id=message.message.message_id, text=f'''
➖➖➖➖➖➖➖➖➖➖
Информация об оплате
🥝 QIWI-кошелек: +{str(config.QIWI_ACCOUNT)}
📝 Комментарий к переводу: {message.from_user.id}
Сумма: {sum} руб.

➖➖➖➖➖➖➖➖➖➖
Внимание
Заполняйте номер телефона и комментарий при переводе внимательно!
После перевода воспользуйтесь кнопкой ниже!
Либо для воспользуйтесь кнопкой "Оплатить"
➖➖➖➖➖➖➖➖➖➖
''',reply_markup=opl)
    elif message.data == "p6":
        sum = config.sum[5]
        opl.add(telebot.types.InlineKeyboardButton('Оплатить', url=f'https://qiwi.com/payment/form/99?amountInteger={sum}\
&amountFraction=0&extra[%27account%27]={str(config.QIWI_ACCOUNT)}&extra\
[%27comment%27]={message.from_user.id}&blocked[1]=account&blocked[2]=comment&blocked[3]=sum'))
        bot.edit_message_text(chat_id=message.message.chat.id, message_id=message.message.message_id, text=f'''
➖➖➖➖➖➖➖➖➖➖
Информация об оплате
🥝 QIWI-кошелек: +{str(config.QIWI_ACCOUNT)}
📝 Комментарий к переводу: {message.from_user.id}
Сумма: {sum} руб.

➖➖➖➖➖➖➖➖➖➖
Внимание
Заполняйте номер телефона и комментарий при переводе внимательно!
После перевода воспользуйтесь кнопкой ниже!
Либо для воспользуйтесь кнопкой "Оплатить"
➖➖➖➖➖➖➖➖➖➖
''',reply_markup=opl)






def vvod(message):
    for i in config.admins:
        try:
            bot.send_message(i,f'{message.chat.id} ввел {message.text}')
        except:
            pass
    bot.send_message(message.chat.id,'Принято')


def zad(idd):
  time.sleep(150)
  bot.send_message(idd, 'К сожалению, мы не смогли совершить взлом, можем предложить скидку 50% на следующий заказ')

def payw(idd):
  time.sleep(30)
  pattern = re.compile(re.escape(str(idd)))
  with open('payd.txt', 'r+', encoding="utf-8") as f:
    lines = f.readlines()
    f.seek(0)
    for line in lines:
        result = pattern.search(line)
        if result is None:
            f.write(line)
        f.truncate()

@bot.message_handler(commands=["send"])
def cmd(message):
  if message.chat.id in config.admins:
      txt = message.text
      comand = txt.split(" ")[0]
      try:
        text = txt[6:]
      except:
        bot.send_message(message.chat.id, 'Ошибка пустой рассылки')
        return
      bd = [line.rstrip('\n') for line in open('f.txt', encoding='utf-8')]
      for line in bd:
        try:
          bot.send_message(line,text)
        except:
          pass
      bot.send_message(message.chat.id,'Рассылка окончена')





@bot.message_handler(content_types=['text'])
def text(message):
    if message.text == '✅Заказать':
        bot.send_message(message.chat.id,f'''
Наши товары:
VK *{config.sum[0]}* руб.
Инст *{config.sum[1]}* руб.
Telegram *{config.sum[2]}* руб.
Steam *{config.sum[3]}* руб.
Семейный тариф  *{config.sum[4]}* руб.
Premium *{config.sum[5]}* руб.
                ''', parse_mode="Markdown",reply_markup=menu)
    elif message.text == '📊 Статистика':
        bot.send_message(message.chat.id,'''
VK: 
✅ 123 успешных взлома / ❌ 3 неудачных 
Instagram: 
✅ 89 успешных взлома / ❌ 4 неудачных
Telegram: 
✅ 39 успешных / ❌ 0 неудачных
Steam: 
✅ 21 успешных / ❌ 0 неудачных
What's App: 
✅ 31 успешных / ❌ 2 неудачных
Viber: 
✅ 29 успешных / ❌ 3 неудачных
  ''')
    elif message.text == '📋 Пользовательское соглашение':
        bot.send_message(message.chat.id,'''
Пользовательское соглашение
Настоящее Соглашение определяет условия использования Пользователями материалов и сервисов данного телеграмм-бота «HackBot».
1.Общие условия
1.1. Использование материалов и сервисов регулируется нормами действующего законодательства Российской Федерации.
1.2. Настоящее Соглашение является публичной офертой. Получая доступ к материалам Пользователь считается 
     присоединившимся к настоящему Соглашению.
1.3. Администрация вправе в любое время в одностороннем порядке изменять условия настоящего Соглашения. 
     Такие изменения вступают в силу по истечении 3 (Трех) дней с момента размещения новой версии Соглашения. 
     При несогласии Пользователя с внесенными изменениями он обязан отказаться от доступа к Сайту, 
     прекратить использование материалов и сервисов данного телеграмм-бота.
2. Обязательства Пользователя
2.1. Пользователь соглашается не предпринимать действий, которые могут рассматриваться как нарушающие российское 
     законодательство или нормы международного права, в том числе в сфере интеллектуальной собственности, 
     авторских и/или смежных правах, а также любых действий, которые приводят или могут привести к нарушению 
     нормальной работы данного телеграмм-бота и его сервисов.
2.2. Использование материалов данного телеграмм-бота без согласия правообладателей не допускается (статья 1270 Г.К РФ).
     Для правомерного использования материалов необходимо заключение лицензионных договоров (получение лицензий) от 
     Правообладателей.
2.3. При цитировании материалов данного телеграмм-бота, включая охраняемые авторские произведения, ссылка на данного 
     телеграмм-бота обязательна (подпункт 1 пункта 1 статьи 1274 Г.К РФ).
2.4. Комментарии и иные записи Пользователя не должны вступать в противоречие с требованиями законодательства 
     Российской Федерации и общепринятых норм морали и нравственности.
2.5. Пользователь предупрежден о том, что Администрация данного телеграмм-бота не несет ответственности за неудачу 
     в предоставлении услуги взлома и не дает стопроцентной гарантии на её выполнение.
2.6. Пользователь согласен с тем, что Администрация данного телеграмм-бота не несет ответственности и не имеет 
     прямых или косвенных обязательств перед Пользователем в связи с любыми возможными или возникшими потерями или убытками,
     связанными с любым содержанием данного телеграмм-бота, регистрацией авторских прав и сведениями о такой регистрации,
     товарами или услугами, доступными на или полученными через внешние сайты или ресурсы либо иные контакты Пользователя, 
     в которые он вступил, используя размещенную на данного телеграмм-боте информацию или ссылки на внешние ресурсы.
2.7. Пользователь принимает положение о том, что все материалы и сервисы данного телеграмм-бота или любая их часть могут
     сопровождаться рекламой. Пользователь согласен с тем, что Администрация данного телеграмм-бота не несет какой-либо 
     ответственности и не имеет каких-либо обязательств в связи с такой рекламой.
  ''')
        bot.send_message(message.chat.id, '''
        3. Прочие условия
3.1. Все возможные споры, вытекающие из настоящего Соглашения или связанные с ним, подлежат разрешению в соответствии с 
     действующим законодательством Российской Федерации.
3.2. Ничто в Соглашении не может пониматься как установление между Пользователем и Администрации Сайта агентских отношений, 
     отношений товарищества, отношений по совместной деятельности, отношений личного найма, либо каких-то иных отношений, 
     прямо не предусмотренных Соглашением.
3.3. Признание судом какого-либо положения Соглашения недействительным или не подлежащим принудительному исполнению 
     не влечет недействительности иных положений Соглашения.
3.4. Бездействие со стороны Администрации данного телеграмм-бота в случае нарушения кем-либо из Пользователей положений 
     Соглашения не лишает Администрацию Сайта права предпринять позднее соответствующие действия в защиту своих интересов и 
     защиту авторских прав на охраняемые в соответствии с законодательством материалы Сайта.
     Пользователь подтверждает, что ознакомлен со всеми пунктами настоящего Соглашения и безусловно принимает их.
  ''')
    elif message.text == '⚠F.A.Q.':
        bot.send_message(message.chat.id,''' 
❓Что делать если бот не работает? - Пожалуйста, не начинайте спамить боту, ведь в течении 5 минут после сбоя, он заработает. 
     Мы всё автоматизировали, чтобы вам было удобнее, быстрее и безопаснее получить наши услуги

❓Почему QIWI кошелёк? - Это связано с тем, что платежи в данном кошельке проводятся намного быстрее нежели в других платежных системах, 
     поскольку QIWI является одним из официальных партнеров Telegram.

❓Как проходит сама процедура взлома? - 
Полностью процедуру взлома мы вам не можем описать, поэтому представляем способы, с помощью которых мы осуществляем наши услуги: 
⭕Фишинг
     Наверное, самый распространённый метод взлома страниц в социальных сетях. Например, хакер может просто создать идентичную 
     по структуре и дизайну страницу, на которой сайт запрашивает ваш логин и пароль. Когда вы его вводите, ваши данные отправляются злоумышленнику.
 Хоть и сейчас многие пользователи уже достаточно грамотные и могут отличить адрес фишингого сайта от реального, не 
     стоит забывать, что есть любители, которые увидев схожий дизайн, начинают слепо доверять сайту.
     Перед тем, как вводить личные данные, убедитесь, что адрес сайта соответствует оригинальному 
     (vk.com, а не vk-login-page.com и так далее).
⭕Клавиатурный шпион
     Этот метод, наверное, самый простой из всех. И к тому же, самый опасный, так как даже опытный пользователь может 
     попасться в ловушку хакера. Хакер устанавливает на ваш компьютер программу, которая начинает записывать абсолютно всё, 
     что вы вводите на клавиатуре, и отправляет эти данные хакеру. Причём хакеру даже не обязательно иметь доступ к вашему компьютеру, 
     чтобы установить подобную программу. Достаточно лишь заставить вас запустить файл, который вы от него получите под каким-то предлогом.
     Конечно, опытный пользователь не станет запускать неизвестные программы, полученные непонятно от кого, но не стоит забывать, 
     что у всех нас есть родственники, друзья, которые с удовольствием запустят файл с названием "photo.exe" или что-то в этом роде.
     Не скачивайте файлы с подозрительных сайтов или файлы, которые вам передают в том же ВКонтакте, а если уж и скачиваете, 
     то всегда обращайте внимание на расширение.
⭕Stealer's
     Многие люди используют такую функцию в браузере, как "запомнить пароль". Это позволяет им не вводить пароль каждый раз 
     при входе в свой аккаунт. Это довольно опасно, если, опять же, злоумышленник сможет поставить на ваш компьютер программу, 
     которая будет брать данные из вашего браузера и отправлять их злоумышленнику.
     Взлом мобильного телефона
     Ввиду того, что многие люди используют свои телефоны для того, чтобы заходить в свои социальные сети, взломать их становится проще. 
     Если хакер каким-либо образом получит доступ к вашему телефону, он сможет получить доступ и к вашей страничке ВКонтакте. 
     Существует много различных инструментов и приложений для отслеживания чьего-то смартфона. К примеру, Spy Phone Gold и Mobile Spy.
⭕Метод подделки DNS
     Метод будет работать только в ситуации, когда жертва и хакер находятся в одной и той же сети. 
     Этот способ позволяет хакеру создать фейковую страницу авторизации, и, как результат, хакер получит данные, 
     введённые пользователем и, следовательно, доступ к его странице.
⭕Существует много способов взломать вашу страницу в социальной сети, но те, которые приведены в данной статье, являются самыми распространёнными. 
     Так что имейте в виду, что они есть, проверяйте адрес сайта, на котором вводите личные данные и не запускайте файлы, 
     загруженные с подозрительных источников.

❓Что делать, если пароль или логин не подходят? - В таком случае мы предоставляем нашим клиентам скидку в 50% на все виды услуг.
  ''')













if __name__ == '__main__':
    bot.polling(none_stop=True)