# -*- coding: utf-8 -*-

#Imports
import telebot
from telebot import types
import sqlite3

#SQL
conn = sqlite3.connect('base.db', check_same_thread=False) #создание файла бд
cur = conn.cursor()  # подключение к бд
cur.execute("""CREATE TABLE IF NOT EXISTS users(
   userid INT PRIMARY KEY,
   fname TEXT,
   lname TEXT,
   hisdolg INT,
   mydolg INT);
""")
conn.commit()

def addtobd(adddbyou):
    new_id = int(mvp) + 1
    cur.execute("""INSERT INTO users(userid, fname, lname, hisdolg, mydolg ) VALUES(?, ?, ?, ?, ?);""", (adddbyou))
    conn.commit()

def vivodsbd():
    cur.execute("""SELECT * FROM users;""")
    global all_results
    all_results = cur.fetchall()

def zaprosone():
    global one_result
    cur.execute(f"SELECT * FROM users WHERE userid = {idedit}")
    one_result = cur.fetchone()

def updatefunc(message):
    allmess = message.text.split()
    name, liname, dolg, mydolg = '"'+ allmess[0] + '"',  '"'+ allmess[1] + '"', allmess[2], allmess[3]
    print(name, liname, dolg, mydolg)
    print(allmess)
    sql_update_query = f"""UPDATE users set fname = {name} WHERE userid = {idedit}"""
    sql_update_query1 = f"""UPDATE users set lname = {liname} WHERE userid = {idedit}"""
    sql_update_query2 = f"""UPDATE users set hisdolg = {dolg} WHERE userid = {idedit}"""
    sql_update_query3 = f"""UPDATE users set mydolg = {mydolg} WHERE userid = {idedit}"""
    cur.execute(sql_update_query)
    cur.execute(sql_update_query1)
    cur.execute(sql_update_query2)
    cur.execute(sql_update_query3)
    conn.commit()

def dellfrombd():
    sql_del_query = """DELETE from users where userid = ?"""
    cur.execute(sql_del_query, (Id_ydal, ))
    conn.commit()

Id_ydal, all_result, names, snames, dolgus, mydolgus, kolstr, not_tmp, idedit, one_result = " " * 10
c = 0
mvp = 1
zap = ","

bot = telebot.TeleBot('5351176501:AAFSOnNfiYKcovWGTHUtVyOUlLjS4W5cSDw') # Токен бота
@bot.message_handler(commands=['start']) # Получение сообщений в боте
def start_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Вывод всех должников")
    markup.add(btn1)
    bot.send_message(message.chat.id, "Привет".format(message.from_user), reply_markup=markup)

@bot.message_handler(content_types=['text'])
def vivodtg(message):

    if(message.text == "Вывод всех должников"):
        vivodsbd()
        global kolstr
        global not_tmp
        not_tmp = all_results
        tmp1 = str(not_tmp).strip('[]')
        tmp2 = tmp1.replace("(", " ").replace( ")", " ").replace("'", " ").replace(",", " ")
        not_tmp = tmp2.split(sep=None, maxsplit=-1)
        for i in range (5, len(not_tmp), 5):
            zapros = not_tmp[i]
            global mvp
            if not_tmp[i] < not_tmp[i-5]:
                mvp = not_tmp[i - 5]
            elif not_tmp[i] > not_tmp[i-5]:
                mvp = not_tmp[i]
            elif not_tmp[i] == not_tmp[i-5]:
                mvp = not_tmp[i]
        kolstr = int(len(not_tmp) / 5)
        x = 5
        for n in range(0, kolstr) :
            tmp1 = "id:  " + str(not_tmp[0 + x * n]) + zap + " Имя:  " + str(not_tmp[1 + x * n]) + zap + " Фамилия: " + str(not_tmp[2 + x * n]) + zap + " Его(Ее) долг: " + str(not_tmp[3 + x * n]) + " | " + " Мой долг: " + str(not_tmp[4 + x * n ] + "\n")
            bot.send_message(message.chat.id, tmp1.format(message.from_user))

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Добавить должников")
        btn2 = types.KeyboardButton("Удалить должников")
        btn3 = types.KeyboardButton("Изменить данные")
        btn4 = types.KeyboardButton("Вывод всех должников")
        markup.add(btn1, btn2, btn3, btn4)
        bot.send_message(message.chat.id, "Что прикажете делать милорд?".format(message.from_user), reply_markup=markup)

    elif (message.text == "Добавить должников"):
        bot.send_message(message.chat.id, "Введите имя".format(message.from_user))
        bot.register_next_step_handler(message, nachalos)

    elif (message.text == "Удалить должников"):
        bot.send_message(message.chat.id, "Введите ID".format(message.from_user))
        bot.register_next_step_handler(message, tgydal)

    elif (message.text == "Изменить данные"):
        bot.send_message(message.chat.id, "Введите ID".format(message.from_user))
        bot.register_next_step_handler(message, edittg)

def tgydal(message):
    global Id_ydal
    Id_ydal = int(message.text)
    dellfrombd()

def nachalos(message):
    bot.send_message(message.chat.id, "Введите Фамилию".format(message.from_user))
    global names
    names = message.text
    bot.register_next_step_handler(message, fam)

def fam(message):
    bot.send_message(message.chat.id, "Введите данные по долгу человека".format(message.from_user))
    global snames
    snames = message.text
    bot.register_next_step_handler(message, dolog)

def dolog(message):
    bot.send_message(message.chat.id, "Введите данные по своему долгу".format(message.from_user))
    global dolgus
    dolgus = message.text
    bot.register_next_step_handler(message, mydolgs)

def mydolgs(message):
    global mydolgus
    mydolgus = message.text
    reg(message)

def reg(message):
    bot.send_message(message.chat.id, "Добавляю".format(message.from_user))
    new_id = int(mvp) + 1
    adddbyou = (new_id, names, snames, dolgus, mydolgus)
    addtobd(adddbyou)

def edittg(message):
    global idedit
    global one_result
    idedit = int(message.text)
    zaprosone()
    tmp1 = str(one_result).strip('[]')
    tmp2 = tmp1.replace("(", " ").replace(")", " ").replace("'", " ").replace(",", " ")
    one_result = tmp2.split(sep=None, maxsplit=-1)
    viv = "id:  " + str(one_result[0]) + zap + " Имя:  " + str(one_result[1]) + zap + " Фамилия: " + str(one_result[2]) + zap + " Его(Ее) долг: " + str(one_result[3]) + " | " + " Мой долг: " + str(one_result[4] + "\n")
    bot.send_message(message.chat.id, viv.format(message.from_user))
    bot.send_message(message.chat.id, "Введите новые данные:".format(message.from_user))
    bot.register_next_step_handler(message, updatefunc)

bot.polling()