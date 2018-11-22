from telegram import  ReplyKeyboardMarkup, KeyboardButton, TelegramObject, Contact
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import constants, texts, base_work
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

updater = Updater(token=constants.token)

registr = registr1 = op = pr = ph = an = st = close = False

dispatcher = updater.dispatcher

def start(bot, update):
    global registr
    message = update.message
    ids = base_work.all_id()
    if message.chat.id not in ids:
        registr = True
        bot.send_message(message.chat.id, 'Вы не зарегестрированны, введите ваше имя:')
    else:
        bottons = [['Лоты', 'Оплата и доставка'], ['FAQ']]
        keyboard = ReplyKeyboardMarkup(bottons)
        bot.send_message(message.chat.id, 'Вы уже зарегестрированны' , reply_markup=keyboard)

def answer(bot,update):
    message = update.message
    global registr, registr1, name, op, op1, pr, pr1, ph, ph1, an, st, close
    if registr == True:
        registr = False
        name = message.text
        registr1 = True
        bot.send_message(message.chat.id, 'Введите свой номер телефона:')
    elif registr1 == True:
        registr1 = False
        base_work.init_user(message.chat.id, name, message.chat.username, str(message.text))
        bottons = [['Лоты', 'Оплата и доставка'], ['FAQ']]
        keyboard = ReplyKeyboardMarkup(bottons)
        bot.send_message(message.chat.id, 'Регистрация завершена, добро пожаловать!', reply_markup=keyboard)
    elif message.text == 'Лоты':
        bottons = [['Открытые лоты'], ['Закрытые сделаки', 'Предложить лот', 'Закрыть лот'], ['Назад']]
        keyboard = ReplyKeyboardMarkup(bottons)
        bot.send_message(message.chat.id, 'Лоты', reply_markup=keyboard)
    elif message.text == 'Оплата и доставка':
        bot.send_message(message.chat.id, 'Здесь будет все об оплате и доставке')
    elif message.text == 'FAQ':
        bot.send_message(message.chat.id,'Здесь будет все о FAQ')
    elif message.text == 'Открытые лоты':
        final = base_work.all_lots()
        for i in final:
            bot.send_photo(message.chat.id, i[2])
            try:
                if i[10] == 1 and i[5] != None:
                    bot.send_message(message.chat.id, texts.shablon1 % (i[7], i[0],i[3], i[4], i[5]))
                elif i[10] == 0 and i[5] != None:
                    bot.send_message(message.chat.id, texts.shablon % (i[7], i[0], i[3], i[4], i[5], i[8]))
                else:
                    bot.send_message(message.chat.id, texts.shablon2 % (i[7], i[0], i[3], i[4]))
            except:
                bot.send_message(message.chat.id, 'Что-то пошло не так')
                message.text = 'Отмена'
                answer(bot, update)
        bottons = [['Сделать ставку', 'Назад']]
        keyboard = ReplyKeyboardMarkup(bottons)
        bot.send_message(message.chat.id, 'Здесь все открытые лоты', reply_markup=keyboard)
    elif message.text == 'Закрыть лот':
        close = True
        bot.send_message(message.chat.id, 'Напишите номер заказа')
    elif close == True:
        close = False
        w = base_work.close_lot(int(message.text), message.chat.id)
        if w == True:
            bot.send_message(message.chat.id, 'Ваш лот удален')
            message.text = 'Отмена'
            answer(bot, update)
        else:
            bot.send_message(message.chat.id, 'Проверьте правильность данных')
            message.text = 'Отмена'
            answer(bot, update)
    elif message.text == 'Сделать ставку':
        bottons = [['Отмена']]
        keyboard = ReplyKeyboardMarkup(bottons)
        bot.send_message(message.chat.id, 'Напишите через пробел номер лота и сумму ставки', reply_markup=keyboard)
        st = True
    elif st == True:
        st = False
        if st != 'Назад':
            try:
                q = message.text.split()
                base_work.update_lot(q[0], q[1], message.chat.id)
            except:
                bot.send_message(message.chat.id, 'Что-то пошло не так')
        else:
            answer(bot,update)
    elif message.text == 'Предложить лот':
        bottons = [['Отмена']]
        keyboard = ReplyKeyboardMarkup(bottons)
        bot.send_message(message.chat.id, 'Напишите описание лота', reply_markup=keyboard)
        op = True
    elif op == True:
        op = False
        if message.text != 'Отмена':
            op1 = message.text
            bot.send_message(message.chat.id, 'Напишите начальную ставку')
            pr = True
        else:
            message.text = 'Отмена'
            answer(bot, update)
    elif pr == True:
        pr1 = message.text
        pr = False
        if message.text != 'Отмена':
            bot.send_message(message.chat.id, 'Скиньте фотографию лота')
            ph = True
        else:
            message.text = 'Отмена'
            answer(bot, update)
    elif ph == True:
        ph = False
        if message.text != 'Отмена':
            ph1 = message.photo[0].file_id
            bot.send_message(message.chat.id, 'Хотите ли вы, чтобы ваш лот был анонимен?')
            an = True
        else:
            message.text = 'Отмена'
            answer(bot, update)
    elif an == True:
        an = False
        if message.text != 'Отмена':
            if message.text == 'Да':
                try:
                    base_work.create_lot(message.chat.id, ph1, op1, pr1, True)
                    bot.send_message(message.chat.id, 'Лот успешо сохранен')
                    message.text = 'Отмена'
                    answer(bot, update)
                except:
                    bot.send_message(message.chat.id, 'Что-то пошло не так')
                    message.text = 'Отмена'
                    answer(bot, update)
            else:
                try:
                    base_work.create_lot(message.chat.id, ph1, op1, pr1, False)
                    bot.send_message(message.chat.id, 'Ваш лот сохранен')
                    message.text = 'Отмена'
                    answer(bot, update)
                except:
                    bot.send_message(message.chat.id, 'Что-то пошло не так')
                    message.text = 'Отмена'
                    answer(bot, update)
        else:
            message.text = 'Отмена'
            answer(bot, update)
    elif (message.text == 'Назад') or (message.text == 'Отмена'):
        bottons = [['Лоты', 'Оплата и доставка'], ['FAQ']]
        keyboard = ReplyKeyboardMarkup(bottons)
        bot.send_message(message.chat.id, 'Чем могу помочь?', reply_markup=keyboard)

start_handler = CommandHandler('start', start)
answer_handler = MessageHandler(Filters.all, answer)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(answer_handler)
updater.start_polling(clean=True, timeout=5 )

