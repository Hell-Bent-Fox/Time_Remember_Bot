import telebot
# from queue import PriorityQueue #Очереди
import requests
from bs4 import BeautifulSoup as BS
import random
import pickle
import urllib3
from ast import literal_eval as le
from telebot import types
import schedule #Планировщик
import time
from datetime import timedelta
import threading #Потоки
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
'''''''''
1) Напомни через 5 минут
2) Напомни через 15 минут
3) Напомни через 30 минут
4) Напомни через час
5) Напомни сегодня в 12:12
6) Напомни завтра в 12:12
7) Напомни 16 в 12:12
8) Напомни 16.06 в 12:12
9) Напомни 16.06.2020 в 12.12
'''''


def caesar(string, num,key,Scrypt):#Шифрование информации
    alpha = ''' !@#^*()_+'"№;:?-={}[]\|/<>.,~`1234567890zyxwvutsrqponmlkjihgfedcbaZYXWVUTSRQPONMLKJIHGFEDCBAяюэьыъщшчцхфутсрпонмлкйизжёедгвбаЯЮЭЬЫЪЩШЧЦХФУТСРПОНМЛКЙИЗЖЁЕДГВБА'''
    res = ''
    if Scrypt==True:
        for c in string:
            res += alpha[(alpha.index(c) + num) % len(alpha)]
        res=key_crypt(res, key, True)
        return res
    elif Scrypt==False:
        string=key_crypt(string,key,False)
        for c in string:
            res += alpha[(alpha.index(c) - num) % len(alpha)]
        return res

def key_crypt(string,key,Scrypt):
    g = len(string)
    def crypt(stroka,key):
        alpha = ' !@#^*()_+"№;:?-={}[]\|/<>.,~`1234567890zyxwvutsrqponmlkjihgfedcbaZYXWVUTSRQPONMLKJIHGFEDCBAяюэьыъщшчцхфутсрпонмлкйизжёедгвбаЯЮЭЬЫЪЩШЧЦХФУТСРПОНМЛКЙИЗЖЁЕДГВБА'
        new_stroka = ''
        for i in range(len(stroka)):
            code = alpha.find(stroka[i]) ^ alpha.find(key[i])
            new_stroka += alpha[code]
        return new_stroka
    def decrypt(stroka,key):
        alpha = ' !@#^*()_+"№;:?-={}[]\|/<>.,~`1234567890zyxwvutsrqponmlkjihgfedcbaZYXWVUTSRQPONMLKJIHGFEDCBAяюэьыъщшчцхфутсрпонмлкйизжёедгвбаЯЮЭЬЫЪЩШЧЦХФУТСРПОНМЛКЙИЗЖЁЕДГВБА'
        new_stroka=''
        for i in range(len(stroka)):
            code = alpha.find(stroka[i]) ^ alpha.find(key[i])
            new_stroka += alpha[code]
        return new_stroka
    def key_mod(key):
        if len(key)<g:
            key=key*(g//len(key))
            i=0
            while len(key)!=g:
                key+=key[i]
                i+=1
        elif len(key)==g:
            key=key
        else:
            do=len(key)-1
            while len(key)!=g:
                key=key[0:do]
                do-=1
        return key
    '''''''''
    def generateKeystream(n):
        m = ''
        for i in range(n):
            n = random.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ -')
            m = m + n
        return m
    '''''
    key=key_mod(key)
    if Scrypt==True:
        string = crypt(string, key)
        return string
    elif Scrypt==False:
        string = decrypt(string, key)
        return string

def crypt_members(members):
    members2=caesar(str(members),3,"qsxcft",True)
    with open('M.txt', 'wb') as out:
        pickle.dump(members2, out)
def decrypt_members():
    with open('M.txt', 'rb') as inp:
        members2 = pickle.load(inp)
    members_f = caesar(str(members2), 3, "qsxcft", False)
    return le(members_f)
def crypt_Turn_mass(Turn_mass):
    Turn_mass2=caesar(str(Turn_mass),4,"qsxcft",True)
    with open('TM.txt', 'wb') as out:
        pickle.dump(Turn_mass2, out)
def decrypt_Turn_mass():
    with open('TM.txt', 'rb') as inp:
        Turn_mass2 = pickle.load(inp)
    Turn_mass_f=caesar(str(Turn_mass2),4,"qsxcft",False)
    return le(Turn_mass_f)
def crypt_Turn_mass_wait(Turn_mass_wait):
    Turn_mass_wait2=caesar(str(Turn_mass_wait),4,"qsxcft",True)
    with open('TMW.txt', 'wb') as out:
        pickle.dump(Turn_mass_wait2, out)
def decrypt_Turn_mass_wait():
    with open('TMW.txt', 'rb') as inp:
        Turn_mass_wait2 = pickle.load(inp)
    Turn_mass_wait_f=caesar(str(Turn_mass_wait2),4,"qsxcft",False)
    return le(Turn_mass_wait_f)

# members=decrypt_members()#chat_id:type,Time,Name,settings,call.message.message_id
# Turn_mass=decrypt_Turn_mass()#time:{chat_id:type,message, chat_id2:type, message}
# Turn_mass_wait=decrypt_Turn_mass_wait() #time:{chat_id:type,message}
def send_remember(time_name,type_send_remember):
    Turn_mass=decrypt_Turn_mass()
    k=Turn_mass[int(time_name)].keys()#Получение chat_id
    for i in k:
        f=Turn_mass[int(time_name)][i] #получение информации для отправки по chat_id
        if type_send_remember=="1":
            bot.send_message(i,text="Вы просили напомнить: "+f[1])
        elif type_send_remember=="2":
            bot.forward_message(i,i,f[1])
    del Turn_mass[int(time_name)]
    crypt_Turn_mass(Turn_mass)
    #bot.send_message(chat_id,text_or_message_id)
    #return schedule.CancelJob
def process(name,sec,type_send_r):
    time.sleep(sec)
    send_remember(name,type_send_r)
# def process_x(name,sec,type_send_r):#Выполняет несколько раз команду, хотя должен только один раз
#     schedule.every(sec).seconds.do(send_remember, *(name,type_send_r))
#     while True:
#         schedule.run_pending()
#         time.sleep(1)

def Small_process_updates(name,sec,type_send_rSPU):#sec - минуты
    run_process = []
    try:
        for thread in threading.enumerate():
            run_process.append(int(thread.name))
    except Exception as err:
        pass
    if int(name) in run_process:
        pass
    else:
        Time_for_process=(sec*60)-7
        threading.Thread(target=process,daemon=True, name="{0}".format(name), args=(
        "{0}".format(name), Time_for_process, type_send_rSPU,)).start()


def check_time():
    Hour_dict=decrypt_Turn_mass()
    Hour_check=TimeNow(base_url, headers)
    numbers = "1234567890"
    new_time = ''
    for j in Hour_check:
        for i in j:
            if i in numbers:
                new_time += i
    Hour_check_str=new_time
    Hour_check_int = int(new_time)
    Hour_check_int2=Hour_check_int+10000
    new_task=[]
    for i in Hour_dict.keys():
        if i<=Hour_check_int2:
            new_task.append(i)
    run_process=[]
    for thread in threading.enumerate():
        run_process.append(int(thread.name))
    for new_i in range(0,len(new_task)):
        if new_task[new_i] in run_process:
            del new_task[new_i]
    for new_task_download in new_task:
        new_task_download=str(new_task_download)
        Time_for_process =(int(new_task_download[0:4]) - int(Hour_check_str[0:4]))*31536000+(int(new_task_download[5:7]) - int(Hour_check_str[5:7]))*2628000+(int(new_task_download[8:10])- int(Hour_check_str[8:10]))*86400+(int(new_task_download[11:13]) - int(Hour_check_str[11:13]))*3600+(int(new_task_download[14:16]) - int(Hour_check_str[14:16]))*60 +(int(new_task_download[17:19]) - int(Hour_check_str[17:19]))
        Time_for_process-=10
        threading.Thread(target=process,daemon=True, name="{0}".format(new_task_download), args=("{0}".format(new_task_download), Time_for_process,Hour_dict[int(new_task_download)][0],)).start()
def check_time_wait():
    Five_min_dict=decrypt_Turn_mass_wait()
    # print(Five_min_dict, type(Five_min_dict))
    # print(Five_min_dict.keys())
    Hour_check=TimeNow(base_url, headers)
    numbers = "1234567890"
    new_time = ''
    for j in Hour_check:
        for i in j:
            if i in numbers:
                new_time += i
    Hour_check_int = int(new_time)
    new_task=[]
    for i in Five_min_dict.keys():
        if i<=Hour_check_int:
            new_task.append(i)
            #print(type(i))
    for i in new_task:
        fun=Five_min_dict[int(i)].keys()# Получение chat_id
        for kim in fun:
            bot.send_message(kim,"Вы хотели чтобы я что-то напомнил, но не оставили сообщение для напоминания.")
        del Five_min_dict[int(i)]
    crypt_Turn_mass_wait(Five_min_dict)

def turn_V2(chat_id, my_time,time_remember,Now_not_Now,user_time,type_remember, remember):
    numbers = "1234567890"
    new_time = ''
    for j in my_time:
        for i in j:
            if i in numbers:
                new_time += i
    if Now_not_Now == True:
        new_time = int(new_time) + time_remember%60*100+ time_remember//60*10000 #Если меньше 62 минут то здесь считается время
    elif Now_not_Now == False:  # time_remember + new_time если больше 62 минут
        d = timedelta(minutes=time_remember)
        m = ''
        for i in str(d):
            if i != ":":
                m += i
        new_time= int(new_time)+int(m)
    Turn_mass_wait = decrypt_Turn_mass_wait()
    Turn_mass_wait_keys = Turn_mass_wait.keys()
    user_chat_id_wait = {}
    for i in Turn_mass_wait_keys:
        some_new_chat_id = Turn_mass_wait[i].keys()
        for j in some_new_chat_id:
            if (j in user_chat_id_wait.keys()) == False:
                user_chat_id_wait[j] = i
    if chat_id in user_chat_id_wait:
        del Turn_mass_wait[user_chat_id_wait[chat_id]][chat_id]
        if len(Turn_mass_wait[user_chat_id_wait[chat_id]].keys()) == 0:
            del Turn_mass_wait[user_chat_id_wait[chat_id]]
    if Turn_mass_wait.get(new_time) == None:
        Turn_mass_wait[new_time]={chat_id:[type_remember,remember]}
    elif Turn_mass_wait.get(new_time) != None:
        Turn_mass_wait[new_time][chat_id] = [type_remember, remember]
    crypt_Turn_mass_wait(Turn_mass_wait)


def turn(chat_id, my_time,time_remember,Now_not_Now,user_time,type_remember, remember):#,chat_id, время сейчас,через сколько минут,(5,15,30,60 или на другую дату),  время пользователя(запрос при регистрации),тип запоминания, что запомнить, список = очереди
    numbers="1234567890"
    new_time=''
    for j in my_time:
        for i in j:
            if i in numbers:
                new_time+=i
    if Now_not_Now==True:
        new_time=int(new_time)+time_remember%60*100 + time_remember//60*10000
    elif Now_not_Now==False: # time_remember + new_time если больше 62 минут
        d = timedelta(minutes=time_remember)
        m = ''
        for i in str(d):
            if i != ":":
                m += i
        new_time = int(new_time) + int(m)
    Turn_mass=decrypt_Turn_mass()
    if Turn_mass.get(new_time)==None:
        Turn_mass[new_time]={chat_id:[type_remember, remember]}
    elif Turn_mass.get(new_time)!=None:
        Turn_mass[new_time][chat_id]=[type_remember, remember]
    if Now_not_Now == True: #Напоминание в пределах часа
        Small_process_updates(new_time,time_remember,type_remember)
    crypt_Turn_mass(Turn_mass)

base_url='https://www.utctime.net'
headers={'accept': '*/*', 'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'}
def TimeNow(base_url,headers):
    session = requests.Session()
    request = session.get(base_url, headers=headers,verify=False)
    if request.status_code == 200:
        soup = BS(request.content, 'html.parser')
        tables = soup.find('table')
        rows = tables.find_all('tr')[1:]
        TIMENOW = []
        for row in rows:
            TIMENOW.append(row.find_all('td'))
        TIMENOWM = (TIMENOW[0][1].text)
        DATE=TIMENOWM.split('T')[0]
        TIMENOWM = TIMENOWM.split('T')[1]
        TIMENOWM = TIMENOWM[0:8]
        return (DATE,TIMENOWM)

# def Delay_check_wait(): #Функция для проверки раз в 5 минут ерсия 1 (ошибка в работе(повторение))
#     Mass_wait=decrypt_Turn_mass_wait()
#     print("DCW, MASS= ",Mass_wait,type(Mass_wait))
#     schedule.every(5).minutes.do(check_time_wait, )
#     while True:
#         schedule.run_pending()
#         time.sleep(1)

def Delay_check_wait(): #Функция для проверки раз в 5 минут версия 2
    Mass_wait = decrypt_Turn_mass_wait()
    print("DCW, MASS= ",Mass_wait,type(Mass_wait))
    while True:
        time.sleep(300)
        check_time_wait()
def Delay_check(): #Функция для проверки раз в час
    while True:
        time.sleep(3600)
        check_time()
threading.Thread(target=Delay_check, name="Check once per hour").start() #Процесс проверки раз в час
threading.Thread(target=Delay_check_wait, name="Check once per 5 min").start() #Процесс проверки раз в 5 минут напоминаний в два сообщения
token=""
bot = telebot.TeleBot(token)
@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id,'Привет. Я бот, который может напомнить тебе через время о чём либо.')
    bot.send_message(message.chat.id,'Выберите режим работы:\n1) Бот запоминает и сохраняет ваше напоминание и в указанное время вам напишет от своего имени ваш текст.\n2) Бот не запоминает сообщение, а только id сообщения и в указанное время перешлет его вам.')
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    callback_button = types.InlineKeyboardButton(text="Первый режим", callback_data="1")
    callback_button1 = types.InlineKeyboardButton(text="Второй режим", callback_data="2")
    keyboard.add(callback_button, callback_button1)
    bot.send_message(message.chat.id, "Вы всегда сможете изменить режим работы отправив команду /settings", reply_markup=keyboard)

@bot.message_handler(commands=['settings'])
def handle_settings(message):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    callback_button = types.InlineKeyboardButton(text="Изменить режим", callback_data="type")
    callback_button1 = types.InlineKeyboardButton(text="Изменить время", callback_data="time")
    callback_button2 = types.InlineKeyboardButton(text="Назад", callback_data="no_settings")
    keyboard.add(callback_button, callback_button1,callback_button2)
    bot.send_message(message.chat.id, 'Вы можете изменить время или режим работы бота. Эти изменения не влияют на предыдущии напомнинания.', reply_markup=keyboard)
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    members=decrypt_members()
    if call.data=="1" or call.data=="2":
        if call.data == "1":
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Вы выбрали первый режим.")
        elif call.data == "2":
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,text="Вы выбрали второй режим.")
        bot.send_message(chat_id=call.message.chat.id, text="Введите разницу во времени относитьельно UTC. От -12 часов до +14 часов.\nНапример Москва +3, Киев +2, США -5.\nВы всегда сможете изменить режим работы отправив команду /settings")
        members[call.from_user.id]=[call.data,"Error",call.from_user.username,False,0]
    elif call.data=="type" or call.data=="time":#settings
        if call.data == "type":
            keyboard = types.InlineKeyboardMarkup(row_width=2)
            callback_button = types.InlineKeyboardButton(text="Первый режим", callback_data="11")
            callback_button1 = types.InlineKeyboardButton(text="Второй режим", callback_data="22")
            callback_button2 = types.InlineKeyboardButton(text="Назад", callback_data="no_settings_type")
            keyboard.add(callback_button, callback_button1,callback_button2)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text='Выберите режим работы:\n1) Бот запоминает и сохраняет ваше напоминание и в указанное время вам напишет от своего имени ваш текст.\n2) Бот не запоминает сообщение, а только id сообщения и в указанное время перешлет его вам.', reply_markup=keyboard)
            members[call.from_user.id][3] = True
        elif call.data=="time":
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            callback_button = types.InlineKeyboardButton(text="Назад", callback_data="no_settings_time")
            keyboard.add(callback_button)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Введите разницу во времени относитьельно UTC. От -12 часов до +14 часов.\nНапример Москва +3, Киев +2, США -5.", reply_markup=keyboard)
            members[call.from_user.id][3]=True
            members[call.from_user.id][4]=call.message.message_id
    elif call.data=="11" or call.data=="22":
        if call.data == "11":
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Вы выбрали первый режим.")
            members[call.from_user.id][0]="1"
            members[call.from_user.id][3] = False
        elif call.data == "22":
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,text="Вы выбрали второй режим.")
            members[call.from_user.id][0] = "2"
            members[call.from_user.id][3] = False
    elif call.data=="no_settings":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="Изменений нет")
    elif call.data=="no_settings_type" or call.data=="no_settings_time":
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        callback_button = types.InlineKeyboardButton(text="Изменить режим", callback_data="type")
        callback_button1 = types.InlineKeyboardButton(text="Изменить время", callback_data="time")
        callback_button2 = types.InlineKeyboardButton(text="Назад", callback_data="no_settings")
        keyboard.add(callback_button, callback_button1, callback_button2)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id = call.message.message_id, text='Вы можете изменить время или режим работы бота. Эти изменения не влияют на предыдущии напомнинания.', reply_markup=keyboard)
        members[call.from_user.id][3] = False
    crypt_members(members)
# crypt_Turn_mass_wait({})
# crypt_Turn_mass({})
@bot.message_handler(content_types=['text'])
def handle_message(message):
    Tic_Tac=TimeNow(base_url, headers) #время UTC
    # numbers = "1234567890"
    # new_time = ''
    # for j in Tic_Tac:
    #     for i in j:
    #         if i in numbers:
    #             new_time += i
    # new_time = int(new_time)

    members=decrypt_members()
    if message.chat.id in members:
        Result_in_mass=True
    else:
        bot.send_message(message.chat.id, "Вы не выбрали режим работы бота.")
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        callback_button = types.InlineKeyboardButton(text="Первый режим", callback_data="1")
        callback_button1 = types.InlineKeyboardButton(text="Второй режим", callback_data="2")
        keyboard.add(callback_button, callback_button1)
        bot.send_message(message.chat.id,
                         'Выберите режим работы:\n1) Бот запоминает и сохраняет ваше напоминание и в указанное время вам напишет от своего имени ваш текст.\n2) Бот не запоминает сообщение, а только id сообщения и в указанное время перешлет его вам.',
                         reply_markup=keyboard)
        Result_in_mass=False
    if Result_in_mass==True:
        if (members[message.chat.id][1])=="Error":
            r = len(message.text.split())
            if (r in [1,2]) and (message.text.split()[0].startswith("+") or message.text.split()[0].startswith("-") or message.text.split()[0]=="0"):
                user_time=message.text.split()
                UTC_TIME_NORMAL = ['−12', '−11', '−10', '−9:30', '−9', '−8:30', '−8', '−7', '−6', '−5', '−4:30', '−4',
                                   '−3:30', '−3', '−2:30', '−2', '−1', '−0:44', '−0:25', '0', '+0:20', '+0:30', '+1',
                                   '+2', '+3', '+3:30', '+4', '+4:30', '+4:51', '+5', '+5:30', '+5:40', '+5:45', '+6',
                                   '+6:30', '+7', '+7:20', '+7:30', '+8', '+8:30', '+8:45', '+9', '+9:30', '+10',
                                   '+10:30', '+11', '+11:30', '+12', '+12:45', '+13', '+13:45', '+14']
                if len(user_time)==1:
                    if user_time[0][1:] in UTC_TIME_NORMAL or user_time[0] in UTC_TIME_NORMAL:
                        members[message.chat.id][1]=int(user_time[0])
                        members[message.chat.id][3] = False
                        bot.send_message(message.chat.id,"Теперь вы можете оставить напоминание так:")
                        bot.send_message(message.chat.id,"1) Напомни через 5 минут\n2) Напомни через 15 минут\n3) Напомни через 30 минут\n4) Напомни через час\n5) Напомни сегодня в 12:12\n6) Напомни завтра в 12:12\n7) Напомни 16 в 12:12\n8) Напомни 16.06 в 12:12\n9) Напомни 16.06.2020 в 12.12")
                        bot.send_message(message.chat.id,"Сам текст может находиться в том же сообщении, что и команда бота или в следующем за ним сообщении.")
                    else:
                        bot.send_message(message.chat.id, "Вы что-то ввели неверно. Введите число формата: +3")
                elif len(user_time)==2:
                    if user_time[0] in UTC_TIME_NORMAL:
                        members[message.chat.id][1]=int(user_time[0])
                        members[message.chat.id][3] = False
                    elif user_time[0] in ["+","-"]:
                        if user_time[1] in UTC_TIME_NORMAL:
                            if user_time[1][0] in ["+","-"]:
                                members[message.chat.id][1] = int(user_time[1])
                                members[message.chat.id][3] = False
                            else:
                                members[message.chat.id][1] = int(user_time[0]+user_time[1])
                                members[message.chat.id][3] = False
                    else:
                        bot.send_message(message.chat.id, "Вы что-то ввели неверно. Введите число формата: +3")
            else:
                bot.send_message(message.chat.id,"Вы не выбрали часовую зону. Напишите сообщение цифрой от -12 до +14.")
        elif (members[message.chat.id][3])==True:
            user_time = message.text.split()
            UTC_TIME_NORMAL = ['−12', '−11', '−10', '−9:30', '−9', '−8:30', '−8', '−7', '−6', '−5', '−4:30', '−4',
                               '−3:30', '−3', '−2:30', '−2', '−1', '−0:44', '−0:25', '0', '+0:20', '+0:30', '+1', '+2',
                               '+3', '+3:30', '+4', '+4:30', '+4:51', '+5', '+5:30', '+5:40', '+5:45', '+6', '+6:30',
                               '+7', '+7:20', '+7:30', '+8', '+8:30', '+8:45', '+9', '+9:30', '+10', '+10:30', '+11',
                               '+11:30', '+12', '+12:45', '+13', '+13:45', '+14']
            if len(user_time) == 1:
                if user_time[0][1:] in UTC_TIME_NORMAL or user_time[0] in UTC_TIME_NORMAL:
                    members[message.chat.id][1] = int(user_time[0])
                    members[message.chat.id][3] = False
                    bot.delete_message(chat_id=message.chat.id, message_id= members[message.chat.id][4])
                    bot.send_message(chat_id=message.chat.id,text='Настройки времени успешно изменены.')
                    members[message.chat.id][4] = 0
                else:
                    bot.send_message(message.chat.id, "Вы что-то ввели неверно. Введите число формата: +3")
            elif len(user_time) == 2:
                if user_time[0][1:] in UTC_TIME_NORMAL or user_time[0] in UTC_TIME_NORMAL:
                    members[message.chat.id][1] = int(user_time[0])
                    members[message.chat.id][3] = False
                    bot.delete_message(chat_id=message.chat.id, message_id= members[message.chat.id][4])
                    bot.send_message(chat_id=message.chat.id,text='Настройки времени успешно изменены.')
                    members[message.chat.id][4] = 0
                elif user_time[0] in ["+", "-"]:
                    if user_time[1] in UTC_TIME_NORMAL:
                        if user_time[1][0] in ["+", "-"]:
                            members[message.chat.id][1] = int(user_time[1])
                            members[message.chat.id][3] = False
                            bot.delete_message(chat_id=message.chat.id, message_id=members[message.chat.id][4])
                            bot.send_message(chat_id=message.chat.id, text='Настройки времени успешно изменены.')
                            members[message.chat.id][4] = 0
                        else:
                            members[message.chat.id][1] = int(user_time[0] + user_time[1])
                            members[message.chat.id][3] = False
                            bot.delete_message(chat_id=message.chat.id, message_id=members[message.chat.id][4])
                            bot.send_message(chat_id=message.chat.id, text='Настройки времени успешно изменены.')
                            members[message.chat.id][4] = 0
                    else:
                        bot.send_message(message.chat.id, "Вы что-то ввели неверно. Введите число формата: +3")
                else:
                    bot.send_message(message.chat.id, "Вы что-то ввели неверно. Введите число формата: +3")
        elif message.text.lower().startswith("напомни через"):
            message_mass=message.text.split()
            if message_mass[2].isdigit()==True and (message_mass[3].lower() in ["минут","минуты","минуту"] or message_mass[3].lower() in ["минут.","минуты.","минуту."]):
                if (len(message_mass)>4 and message_mass[4]!=".") or len(message_mass)>5: # Если в одном сообщении время + напоминание
                    if 0<int(message_mass[2])<62:
                        if members[message.chat.id][0] == "1":
                            turn(message.chat.id,Tic_Tac,int(message_mass[2]),True, members[message.chat.id][1],members[message.chat.id][0], message.text[22:])
                        elif members[message.chat.id][0] == "2":
                            turn(message.chat.id, Tic_Tac,int(message_mass[2]),True, members[message.chat.id][1], members[message.chat.id][0], message.message_id)
                    elif int(message_mass[2])>62: #Не работает из-за необходимости передачи уже готового времени
                        if members[message.chat.id][0] == "1":
                            turn(message.chat.id,Tic_Tac,int(message_mass[2]),False, members[message.chat.id][1],members[message.chat.id][0], message.text[22:])
                        elif members[message.chat.id][0] == "2":
                            turn(message.chat.id, Tic_Tac,int(message_mass[2]),False, members[message.chat.id][1], members[message.chat.id][0], message.message_id)
                    bot.send_message(message.chat.id,'Хорошо.')
                else: # Если только время
                    if 0<int(message_mass[2])<62:# должно быть от 5 минут минимум
                        if members[message.chat.id][0] == "1":
                            turn_V2(message.chat.id,Tic_Tac,int(message_mass[2]),True, members[message.chat.id][1],members[message.chat.id][0], None)
                        elif members[message.chat.id][0] == "2":
                            turn_V2(message.chat.id, Tic_Tac,int(message_mass[2]),True, members[message.chat.id][1], members[message.chat.id][0], None)
                    elif int(message_mass[2])>62: #Не работает из-за необходимости передачи уже готового времени
                        if members[message.chat.id][0] == "1":
                            turn_V2(message.chat.id,Tic_Tac,int(message_mass[2]),False, members[message.chat.id][1],members[message.chat.id][0], None)
                        elif members[message.chat.id][0] == "2":
                            turn_V2(message.chat.id, Tic_Tac,int(message_mass[2]),False, members[message.chat.id][1], members[message.chat.id][0], None)

            else:
                bot.send_message(message.chat.id,"Вы что-то не так ввели. Пример ввода: Напомни через 7 минут\nВ следующем или в этом же сообщении оставьте своё напоминание.")
        else: # необходимо удалять предыдущие не заполненые сообщения - напоминания
            Turn_mass_wait=decrypt_Turn_mass_wait()
            Turn_mass_wait_keys=Turn_mass_wait.keys()
            user_chat_id_wait={}
            for i in Turn_mass_wait_keys:
                some_new_chat_id=Turn_mass_wait[i].keys()
                for j in some_new_chat_id:
                    if (j in user_chat_id_wait.keys())==False:
                        user_chat_id_wait[j]=i
            if message.chat.id in user_chat_id_wait.keys():#Проверка ожидания второго сообщения
                time_transfer=user_chat_id_wait[message.chat.id]
                type_transfer=Turn_mass_wait[time_transfer][message.chat.id][0]
                if type_transfer=="1":
                    Turn_mass_wait[time_transfer][message.chat.id][1] = message.text
                elif type_transfer=="2":
                    Turn_mass_wait[time_transfer][message.chat.id][1] = message.message_id
                Turn_mass = decrypt_Turn_mass()#Добовление в основной поток
                if Turn_mass.get(time_transfer) == None:
                    Turn_mass[time_transfer] = {message.chat.id: [type_transfer, Turn_mass_wait[time_transfer][message.chat.id][1]]}
                elif Turn_mass.get(time_transfer) != None:
                    Turn_mass[time_transfer][message.chat.id] = [type_transfer, Turn_mass_wait[time_transfer][message.chat.id][1]]
                del Turn_mass_wait[user_chat_id_wait[message.chat.id]][message.chat.id]
                if len(Turn_mass_wait[user_chat_id_wait[message.chat.id]].keys())==0:
                    del Turn_mass_wait[user_chat_id_wait[message.chat.id]]
                bot.send_message(message.chat.id, 'Хорошо.')
                numbers = "1234567890"
                new_time = ''
                my_time=TimeNow(base_url, headers) #время UTC
                for j in my_time:
                    for i in j:
                        if i in numbers:
                            new_time += i
                if int(time_transfer)-int(new_time)<10000:
                    Now_not_Now=True
                else:
                    Now_not_Now=False
                if Now_not_Now == True:  # Напоминание в пределах часа
                    time_now_uts_sec=int(new_time[6:8])*86400+int(new_time[8:10])*3600+int(new_time[10:12])*60+ int(new_time[12:14]) #UTC в секундах начиная с дней
                    time_now_remember=int(str(time_transfer)[6:8])*86400+int(str(time_transfer)[8:10])*3600+int(str(time_transfer)[10:12])*60+ int(str(time_transfer)[12:14])#Время записанное в секундах начиная с дней
                    time_remember = ((time_now_uts_sec - time_now_remember))
                    #print(time_remember,type(time_remember))
                    if time_remember>0:
                        time_remember=round((time_now_uts_sec-time_now_remember)/60)
                    else:
                        time_remember = 1
                    Small_process_updates(time_transfer, time_remember, type_transfer)#time_remember - секунды
                    
                elif Now_not_Now==False: #Если напомнинание больше чем через час
                    pass
                crypt_Turn_mass(Turn_mass)
            crypt_Turn_mass_wait(Turn_mass_wait)
    crypt_members(members)
    print("TMW",decrypt_Turn_mass_wait())
    print("TM",decrypt_Turn_mass())

    #print(message.text)
    #bot.forward_message(message.chat.id, message.chat.id, message.message_id)


#caesar('abcdefghig',3,'key',True)




'''
k={1:2,11:(77,12,[45,11])}
f=str(k)
g=caesar(f,3,"key",True)
print("g= ",g)
g2=caesar(g,3,"key",False)
print("g2= ", g2)
print(type(le(g2)))
k.get()#опытка взять элемент без исключения
'''

# def work(f):
#     print(f+ " Read")
#     return schedule.CancelJob
# def test(name):
#
#
#     schedule.every(10).seconds.do(work, *"I")
#
#     while True:
#         schedule.run_pending()
#         time.sleep(1)
#
# for i in range(5):
#     k=True
#     t = threading.Thread(target=test,name="1111{0}".format(i), args=("1111{0}".format(i),)).start()
#
#     time.sleep(1)
#
# for thread in threading.enumerate():
#     print(thread.name)
# print("GOGO")

bot.polling(none_stop=True)
