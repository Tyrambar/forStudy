from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, InlineQueryHandler, RegexHandler, BaseFilter
from telegram import InlineQueryResultArticle, InputTextMessageContent, KeyboardButton, ReplyKeyboardMarkup
import re
import logging
from datetime import datetime

TG_URL = 'https://telegg.ru/orig/bot'
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

# Default buttons
to_begin = 'Вернуться в начало'
cancel1 = 'Отменить запись'
see_my_e = 'Мои записи'
x = 'Ближайшие мероприятия'
agree = 'Пойду на это мероприятие'
button_opt = ['Создать мероприятие', 'Добавить мероприятие']
button_opt_edit = ['Все правильно - дальше', 'Завершить редактирование']
show_org = 'Мои посетители'
show_all = 'чо по чем?'


# Default messages from bot
hi_from_bot = ("Добро пожаловать! Ознакомьтесь с ближайшими мероприятиями.\n"
"Вы можете записаться на любое из них и всегда посмотреть имеющиеся записи🙂."
"А если планы изменились, отменить их\n"
"📌Обратите внимание на значок в поле сообщений, рядом со смайлом. "
"Нажмите на него, чтобы открыть меню")
choice_e = 'Выберите мероприятие: напишите порядковый номер или нажмите на кнопку:\n'
confirm = 'Вы записались на '
wrong = ('😔 Я не могу вас понять\nВы можете попробовать снова:\n'
'📌 Откройте рядом со смайликами квадратную иконку для удобной навигации\n📌 Напишите Привет, чтобы начать разговор заново')
cancel_all = 'Ваша запись отменена.'
mes_see = 'Можете снова просмотреть те мероприятия💬, куда вы записались.\n' \
          'Чтобы отменить запись, нажмите на него или напиши номер ' \
          'там будет кнопка "отменить запись"\nРанее Вы записались на:\n'

options = 'Чтобы добавить мероприятие, вам нужно заполнить поэтапно :\n' \
          '📌Краткое описание мероприятия, которое будет отображаться на кнопке\n' \
          '📌Адрес места проведения мероприятия. Пример: Маросейка 13с1\n' \
          '📌Дата проведения (месяц, дата, час - разделение через запятую). Пример: 5, 25, 18\n' \
          '📌Описание места проведения\n' \

choose_edit_e = 'Выберете мероприятия, данные которого хотели бы изменить:\n'
old_option = '\nСтарое значение:\n'
options_edit_succ = 'Мероприятие успешно изменено!'
fail_right_4_edit_e = 'Вы не являетесь создателем этого мероприятия, поэтому Вы не можете его изменить'

options_str = options.split('\n')
options_fail = 'Неправильно записаны данные'
options_almost = 'Подтвердите добавление мероприятия'
options_succ = 'Мероприятие успешно добавлено!'

destroy_succ = 'Мероприятие успешно испепелено!!!'

mes_a_che_tam = 'Нормас\nна движ-то какой-нибудь пойдешь?'
welc = 'Пожалуйста)\nЭто моя работа😄'

# Regular Expressions
ok = r'(записаться)|(х[очуатю]{3})|(д[ао]вай)|(п[ао]й[дуеёмти])|(п[ао]?шли)|(да+)|((го)+у*)|(ид[ёемду])|(к[ао]не[чш]н[ао]*)|(ок[ейи]*)'
nearest = r'(близ?жайш[ие]е!*)|([после]*завтр[ао])|([в ]*выходн[ыеой]*)'
begin = r'(меню)|(старт[уй]*)|(прив[етствую]*)|(добр[огоыйе]+( )?[утроадняденьвечера]*)|' \
        r'([вс]* ?нач[ниалоать]*)|(з?д[ао]+р[аоваствуйте]+)|(хай)|(hi)|(hello)|(ку)'
a_che_tam = r'([а ]*ч[еёо]{1} там\??)|(как [тыдела]\??)'
welcom = r'(с?пас[ие]б[ао]*)|(благодарю?[ствую]*[им]*)|(но?рм[ас]*)|(к ?р ?а ?с ?[иа]? ?в ?[ао]?[чик]*)'

e = ["Фестиваль 25.05 12ч м.Красносельская", "Настолки 26.05 18ч м.Китай-город", "Туса в Турции 1-15 июля"]
e_adress = ["Нижняя Красносельская 35сК", 'Маросейка 13с1', 'Турция']
def make_date(month, date, hour, min = 0):
    return datetime(2019, month, date, hour, min)
e_dates = {
    e[0]: datetime(2019, 5, 25, 19),
    e[1]: datetime(2019, 5, 26, 19),
    e[2]: datetime(2019, 7, 1, 1)
}
months = {1: 'января', 2: 'февраля', 3: 'марта', 4: 'апреля', 5: 'мая', 6: 'июня',
          7: 'июля', 8: 'августа', 9: 'сентября', 10: 'октября',  11: 'ноября', 12: 'декабря'}
daysweek = {'Monday': 'понедельник', 'Tuesday': 'вторник', 'Wednesday': 'среда',
'Thursday': 'четверг','Friday': 'пятница', 'Saturday': 'суббота', 'Sunday': 'воскресенье'}

#95372442, 159542333, 166307242, 382620531, 293320616, 273880438
#confirmed = {e[0]: [], e[1]: [], e[len(e)-1]: []}
events_d = {
e[0]: (
'Культурный фестиваль с увлекательными лекциями и мастер-классами 25 мая с 12:00 рядом с м. Красносельская (или Бауманская), по адресу Нижняя Красносельская 35сК.\n'
'Мы ждем всех, кому интересен калейдоскоп изменений России за прошедшие 40 лет в области культуры, искусства, '
'городской среды, музыки и технологий.\n' 'Организатор: Московский многофункциональный культурный центр, направление "Культура в городе".\n\n'
'😯Впервые на центральной площадке Москвы — творческое переосмысление современной истории, интерактивные «порталы» '
'в прошлое, спортивные мастер-классы, лекции на актуальные темы в области искусства, творчества и культуры, а также волшебный '
'музыкальный квартирник от проекта "Все свои": это стенд-ап, музыкальное выступление и караоке под гитару.\n'
'Будет весело   и познавательно👨🎓, все как мы любим: с игровыми ретро-автоматами, пинг-понгом, мехенди и антуражными декорациями.\n\n'
'Программа фестиваля:\n'
'📌Лекционный блок:\n'
'12:30-14:00 – «И тогда обиделось время…: повседневные практики эпохи Застоя». Лекция Ирины Глущенко (НИУ ВШЭ)\n'
'14:30-16:30 – «За столом»: обсуждение 2010-х в России, экологии, интернета и феминизма\n'
'16:30-17:30 – «Поп-музыка 3019 года или Почему поп-музыка — это современный авангард». Лекция Гриши Пророкова (канал Blitz and Chips)\n\n'
'📌Мастер-классы:\n'
'12:00 — 13:00 Утренняя йога от студии Zaryad\n'
'13:30 — 14:30 Sekta: тренировка в стиле 90-х\n'
'13:00 — 14:00 Кулинарный мастер-класс европейской кухни от FOOD TASTY cafe\n'
'14:30 — 16:40 Турнир по пинг-понгу Ping Tablet\n'
'14:00 — 18:00 Мехенди для всех желающих\n'
'15:00 — 16:00 Mynameisspace: лекция — перформанс «Нафталин или зачем нам современное искусство»\n'
'15:00 — 16:00 MAGIC LAB: творческий мастер-класс "Центробежное рисование"\n'
'18:00 — 21:00 Музыкальный квартирник ВСЕ СВОИ\n'
),
e[1]: ('Хей, скучал по нашим настолкам?\n\n'
"Приходи в антикафе Jeffrey's Coffee на Маросейке и сразись с лучшими из лучших!\n"
'Не уверен в своих силах? Не знаешь правила игры? Ничего страшного! Наши очаровательные ведущие всему научат и обо всем расскажут.\n'
'Считаешь себя экспертом? Приходи и докажи!\n'
'Просто хочешь хорошо провести время? Присоединяйся к нашей дружной компании и проведи запоминающийся вечер.\n'),
e[len(e)-1]: ("Летом, с 1 по 15 июля состоится Sea || Summer || Students - большая летняя тусовка на море для молодежи.\n"
"Более 100 человек отправится на южный берег Турции. Уже второй по счету выезд станет еще масштабнее и интереснее!\n"
"Бары, дискотеки, экскурсии и квесты - нам будет чем заняться! "
"А теплое Средиземное море создаст лучшую атмосферу для большого молодежного праздника)")
}

# Main classes
class Arg:
    def __init__(self, numb_see_my_e, deep, previous, see_my_e_lst, change):
        self.numb_see_my_e = numb_see_my_e
        self.deep = deep
        self.previous = previous
        self.see_my_e_lst = see_my_e_lst
        self.change = change

class User:
    users = {}
    def __init__(self, chat_id, numb_see_my_e,
                    deep, previous, see_my_e_lst, change = 0):
        self.u = chat_id
        User.users[self.u] = Arg(numb_see_my_e, deep, previous, see_my_e_lst, change)


class Event:
    evs_names = []
    confirmed_all = []
    host_all = []
    def __init__(self, name, addr, date, desc, host_id):
        self.date = date
        self.address = addr
        self.description = desc
        self.name = name
        self.host_id = host_id
        Event.host_all.append(self.host_id)
        self.confirmed = []
        self.nicknames = []
        if evs:
            for i in Event.evs_names:
                if self.date < evs[i].date:
                    self.ev_id = Event.evs_names.index(i)
                    Event.evs_names.insert(self.ev_id, self.name)
                    break
            else:
                Event.evs_names.append(self.name)
                self.ev_id = len(Event.evs_names)
        else:
            Event.evs_names.append(self.name)

    def __str__(self):
        return self.name
    def __repr__(self):
        return self.name + '__class_Event'

#ex_evs_objs = [make_date(1, 1, 1, 1) for _ in range(3)]
admin = 203292486
ex_evs_objs = {}
evs = {}
for i in range(3):
    ex_evs_objs[e[i]] = Event(e[i], e_adress[i], e_dates[e[i]], events_d[e[i]], admin)
evs = ex_evs_objs.copy()
print(evs)
#argss_ind[ind_id] = {'numb_see_my_e': pp, 'deep': deep, 'previous': prev, 'see_my_e_lst': see_my_e_lst}

#us = User(12345, 3, 2, 'some', ['aha', 'huh'])
#print(12345 in User.users, us.users[12345], User.users[12345].numb_see_my_e)

# Helping funcs
def m_send(up, co, txt, keyboard = None,):
    return co.bot.send_message(chat_id=up.message.chat_id, text=txt, reply_markup=keyboard)

def make_menu(user_arg, buttons = [], n_cols=1, footer_buttons = [to_begin], seeing_my_e = 0, while_edit = 0):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    pre_footer_buttons = []
    print(footer_buttons, Event.confirmed_all)
    if not while_edit:
        if user_arg in Event.confirmed_all:
            if see_my_e not in footer_buttons:
                pre_footer_buttons.append(see_my_e)
            if seeing_my_e:
                pre_footer_buttons.remove(see_my_e)
        if see_my_e in footer_buttons and not user_arg in Event.confirmed_all:
            pre_footer_buttons.remove(see_my_e)
        if user_arg in Event.host_all:
            pre_footer_buttons.append(show_org)
    if pre_footer_buttons:
        menu.append(pre_footer_buttons)
    if footer_buttons:
        menu.append(footer_buttons)

    return menu

def check_input_number(n, lst):
    if len(n) > 1:
        if re.match(r"\d", n[1]) and int(n[:2]) <= len(lst) - 1:
            return int(n[:2])
        elif int(n[0]) <= len(lst) - 1:
            return int(n[0])
        else:
            return
    else:
        if int(n[0]) <= len(lst):
            return int(n[0])
        else: return



# Main with data
ac_token = ''
updater = Updater(token= ac_token, base_url = TG_URL, use_context= True)
dispatcher = updater.dispatcher


user = None
args_4_create = {}
password = 'праотцы'
pass_determine = 'кара'
pass_edit = 'правка'

# Additional funcs-handlers
def welc_ans(update, context):
    m_send(update, context, welc)

def how_a_u(update, context):
    m_send(update, context, mes_a_che_tam)

def wrong_ans(update, context):
    print(update.message.text)
    m_send(update, context, wrong)


# argss_ind[ind_id] = {'numb_see_my_e': pp, 'deep': deep, 'previous': prev, 'see_my_e_lst': see_my_e_lst}
# Main funcs-handlers
def start(update, context):
    global user
    menu = make_menu(update.message.chat_id, buttons = [x], footer_buttons = [])
    reply_markup = ReplyKeyboardMarkup(menu, resize_keyboard = True, one_time_keyboard = True)
    m_send(update, context, hi_from_bot, reply_markup)
    user = User(update.message.chat_id, 0, 0, '', [])

    print(update.effective_user.username)

def step_1(update, context):
    global user
    menu = make_menu(update.message.chat_id, Event.evs_names)
    reply_markup = ReplyKeyboardMarkup(menu, resize_keyboard = True, one_time_keyboard = True)
    text = ''
    if user.users[update.message.chat_id].change == 1:
        text = choose_edit_e
    print(Event.evs_names)
    for kk, i in enumerate(Event.evs_names):
        text += f"{kk+1}. {i}\n"
    m_send(update, context, text, reply_markup)
    if update.message.chat_id not in User.users:
        user = User(update.message.chat_id, 0, 0, '', [])
    if not user.users[update.message.chat_id].change:
        user.users[update.message.chat_id].deep = 1

# Most popular function-handler for processing events, depending from what do you want
def step_in_e(update, context):
    global user, evs
    if update.message.chat_id not in User.users:
        user = User(update.message.chat_id, 0, 0, '', [])
    print('in step_in_e')
    # Function-handler for see some event
    def step_e(update, context, numb = None):
        global user, evs
        if update.message.text in Event.evs_names:
            user.users[update.message.chat_id].previous = update.message.text
            if update.message.chat_id in evs[update.message.text].confirmed:
                menu = make_menu(update.message.chat_id, [cancel1])
            else:
                menu = make_menu(update.message.chat_id, [agree])
            date_of_e = evs[update.message.text].date
            text = f'{user.users[update.message.chat_id].previous}\n' \
                   f'{int(date_of_e.strftime("%d"))} {months[int(date_of_e.strftime("%m"))]}, ' \
                   f'{daysweek[date_of_e.strftime("%A")]}, в {date_of_e.strftime("%H:%M")}\nпо адресу: ' \
                   f'{evs[update.message.text].address}\n\n' \
                   f'{evs[update.message.text].description}'
            reply_markup = ReplyKeyboardMarkup(menu, resize_keyboard=True, one_time_keyboard=True)
            m_send(update, context, text, reply_markup)

        elif numb:
            if user.users[update.message.chat_id].see_my_e_lst:
                user.users[update.message.chat_id].previous = user.users[update.message.chat_id].see_my_e_lst[numb-1]

                if update.message.chat_id in evs[user.users[update.message.chat_id].previous].confirmed:
                    menu = make_menu(update.message.chat_id, [cancel1])
                else:
                    menu = make_menu(update.message.chat_id, [agree])
                reply_markup = ReplyKeyboardMarkup(menu, resize_keyboard=True, one_time_keyboard=True)
                date_of_e = evs[user.users[update.message.chat_id].previous].date
                text = f'{user.users[update.message.chat_id].previous}\n' \
                       f'{int(date_of_e.strftime("%d"))} {months[int(date_of_e.strftime("%m"))]}, ' \
                       f'{daysweek[date_of_e.strftime("%A")]}, в {date_of_e.strftime("%H:%M")}\nпо адресу: ' \
                       f'{evs[user.users[update.message.chat_id].previous].address}\n\n' \
                       f'{evs[user.users[update.message.chat_id].previous].description}'
                m_send(update, context, text, reply_markup)
            else:
                user.users[update.message.chat_id].previous = Event.evs_names[numb-1]
                if update.message.chat_id in evs[Event.evs_names[numb-1]].confirmed:
                    menu = make_menu(update.message.chat_id)
                else:
                    menu = make_menu(update.message.chat_id, [agree])
                date_of_e = evs[Event.evs_names[numb-1]].date
                text = f'{user.users[update.message.chat_id].previous}\n' \
                       f'{int(date_of_e.strftime("%d"))} {months[int(date_of_e.strftime("%m"))]}, ' \
                       f'{daysweek[date_of_e.strftime("%A")]}, в {date_of_e.strftime("%H:%M")}\nпо адресу: ' \
                       f'{evs[Event.evs_names[numb-1]].address}\n\n' \
                       f'{evs[Event.evs_names[numb-1]].description}'
                reply_markup = ReplyKeyboardMarkup(menu, resize_keyboard=True, one_time_keyboard=True)
                m_send(update, context, text, reply_markup)
        else:
            return wrong_ans(update, context)

        if user.users[update.message.chat_id].numb_see_my_e:
            user.users[update.message.chat_id].numb_see_my_e = 0
        user.users[update.message.chat_id].see_my_e_lst = []
        user.users[update.message.chat_id].deep = 2
    # Function-handler for confirm to event
    def step_confirm(update, context):
        global user, evs
        menu = make_menu(update.message.chat_id)
        reply_markup = ReplyKeyboardMarkup(menu, resize_keyboard=True, one_time_keyboard=True)
        m_send(update, context, f'{confirm} `{user.users[update.message.chat_id].previous}`', reply_markup)
        if update.message.chat_id not in evs[user.users[update.message.chat_id].previous].confirmed:
            evs[user.users[update.message.chat_id].previous].confirmed.append(update.message.chat_id)
            Event.confirmed_all.append(update.message.chat_id)
            context.bot.send_message(
                chat_id=evs[user.users[update.message.chat_id].previous].host_id,
                text=f'Пользователь @{update.effective_user.username} записался на Ваше мероприятие')
            print(evs[user.users[update.message.chat_id].previous])
            evs[user.users[update.message.chat_id].previous].nicknames.append(f'@{update.effective_user.username}')
            print(evs[user.users[update.message.chat_id].previous].nicknames)

    # Function-handler for cancel confirm to event
    def step_canc(update, context):
        global user, evs
        menu = make_menu(update.message.chat_id)
        reply_markup = ReplyKeyboardMarkup(menu, resize_keyboard=True, one_time_keyboard=True)
        m_send(update, context, cancel_all, reply_markup)
        evs[user.users[update.message.chat_id].previous].confirmed.remove(update.message.chat_id)
        Event.confirmed_all.remove(update.message.chat_id)
        context.bot.send_message(
            chat_id=evs[user.users[update.message.chat_id].previous].host_id,
            text=f'Пользователь @{update.effective_user.username} отменил запись на Ваше мероприятие')
        evs[user.users[update.message.chat_id].previous].nicknames.remove(
            f'@{update.effective_user.username}')
    # Conditions returns needed function
    if user.users[update.message.chat_id].change == -1:
        return succ_destroy_e_f(update, context)
    elif (update.message.text in Event.evs_names or re.match(r"[1-9]\d?", update.message.text[:2]))\
            and user.users[update.message.chat_id].deep < 10 and user.users[update.message.chat_id].change == 0:
        if update.message.text in Event.evs_names:
            return step_e(update, context)
        elif user.users[update.message.chat_id].numb_see_my_e:
            numb_for_see_my = check_input_number(update.message.text, user.users[update.message.chat_id].see_my_e_lst)
            print(user.users[update.message.chat_id].numb_see_my_e, [j for j in range(1,user.users[update.message.chat_id].numb_see_my_e+1)], numb_for_see_my)
            return step_e(update, context, numb_for_see_my) if numb_for_see_my else wrong_ans(update, context)
        elif user.users[update.message.chat_id].deep == 1 and check_input_number(update.message.text, Event.evs_names):
            return step_e(update, context, check_input_number(update.message.text, Event.evs_names))
        else:
            return wrong_ans(update, context)
    elif update.message.text == agree or re.match(ok, update.message.text):
        return step_confirm(update, context)
    elif update.message.text == cancel1 and \
            update.message.chat_id in evs[user.users[update.message.chat_id].previous].confirmed:
        return step_canc(update, context)
    elif 10 <= user.users[update.message.chat_id].deep < 20:
        return creating_e_f(update, context)
    elif user.users[update.message.chat_id].change == 1 or user.users[update.message.chat_id].deep >= 20:
        return edit_e_f(update, context)
    else:
        return wrong_ans(update, context)

# Seeing yours confirmed
def see_my_e_f(update, context):
    global user, evs
    if update.message.chat_id not in User.users:
        user = User(update.message.chat_id, 0, 0, '', [])
        return wrong_ans(update, context)
    see_my = mes_see
    for i in Event.evs_names:
        if update.message.chat_id in evs[i].confirmed:
            user.users[update.message.chat_id].see_my_e_lst.append(i)
            see_my += f"{user.users[update.message.chat_id].numb_see_my_e+1}. {i} по адресу {evs[i].address}\n"
            user.users[update.message.chat_id].numb_see_my_e += 1
    menu = make_menu(update.message.chat_id, user.users[update.message.chat_id].see_my_e_lst, seeing_my_e=1)
    reply_markup = ReplyKeyboardMarkup(menu, resize_keyboard=True, one_time_keyboard=True)
    m_send(update, context, see_my, reply_markup)
    user.users[update.message.chat_id].deep = 3


# Functions for creating events in bot
def begin_create_e_f(update, context):
    global user
    user = User(update.message.chat_id, 0, 0, '', [])
    menu = make_menu(update.message.chat_id, buttons= [button_opt[0]], while_edit = 1)
    reply_markup = ReplyKeyboardMarkup(menu, resize_keyboard=True, one_time_keyboard=True)
    m_send(update, context, options, reply_markup)

def to_create_e_f(update, context):
    global user
    user.users[update.message.chat_id].deep = 10
    menu = make_menu(update.message.chat_id, while_edit = 1)
    reply_markup = ReplyKeyboardMarkup(menu, resize_keyboard=True, one_time_keyboard=True)
    m_send(update, context, options_str[1], reply_markup)

def creating_e_f(update, context):
    global user, args_4_create, evs
    menu = make_menu(update.message.chat_id, while_edit=1)
    reply_markup = ReplyKeyboardMarkup(menu, resize_keyboard=True, one_time_keyboard=True)

    if user.users[update.message.chat_id].deep == 10:
        args_4_create['name'] = update.message.text
        user.users[update.message.chat_id].deep = 11
        m_send(update, context, options_str[2], reply_markup)
    elif user.users[update.message.chat_id].deep == 11:
        args_4_create['address'] = update.message.text
        user.users[update.message.chat_id].deep = 12
        m_send(update, context, options_str[3], reply_markup)
    elif user.users[update.message.chat_id].deep == 12:
        t = update.message.text.split(',')
        try:
            if len(t) == 4:
                args_4_create['date'] = make_date(int(t[0]), int(t[1]), int(t[2]), int(t[3]))
            else:
                args_4_create['date'] = make_date(int(t[0]), int(t[1]), int(t[2]))
        except (IndexError, ValueError):
            m_send(update, context, options_fail)
        else:
            user.users[update.message.chat_id].deep = 13
            m_send(update, context, options_str[4], reply_markup)
    elif user.users[update.message.chat_id].deep == 13:
        args_4_create['description'] = update.message.text
        user.users[update.message.chat_id].deep = 14
        menu = make_menu(update.message.chat_id, buttons = [button_opt[1]], while_edit=1)
        reply_markup = ReplyKeyboardMarkup(menu, resize_keyboard=True, one_time_keyboard=True)
        m_send(update, context, options_almost, reply_markup)
    elif user.users[update.message.chat_id].deep == 14 and update.message.text == button_opt[1]:
        new_ev_obj = Event(args_4_create['name'], args_4_create['address'],
                           args_4_create['date'], args_4_create['description'], update.message.chat_id)
        evs[args_4_create['name']] = new_ev_obj
        user.users[update.message.chat_id].deep = 0
        m_send(update, context, options_succ, reply_markup)


# Functions for change existing events in bot
def to_to_edit_e_f(update, context):
    global user
    user = User(update.message.chat_id, 0, 0, '', [])
    user.users[update.message.chat_id].change = 1
    step_1(update, context)

def edit_e_f(update, context):
    global user, args_4_create, evs
    menu = make_menu(update.message.chat_id, buttons=[button_opt_edit[0]], while_edit=1)
    reply_markup = ReplyKeyboardMarkup(menu, resize_keyboard=True, one_time_keyboard=True)
    if user.users[update.message.chat_id].change == 1:
        user.users[update.message.chat_id].deep = 20
        user.users[update.message.chat_id].change = 0
        user.users[update.message.chat_id].previous = update.message.text
        if evs[update.message.text].host_id == update.message.chat_id or admin == update.message.chat_id:
            text = options_str[1]+old_option+user.users[update.message.chat_id].previous
            m_send(update, context, text, reply_markup)
        else:
            context.bot.send_message(update.message.text, fail_right_4_edit_e)
            user = User(update.message.chat_id, 0, 0, '', [])
    elif user.users[update.message.chat_id].deep == 20:
        if update.message.text != button_opt_edit[0]:
            args_4_create['name'] = update.message.text
        else:
            args_4_create['name'] = user.users[update.message.chat_id].previous
        obj_ev = evs.pop(user.users[update.message.chat_id].previous)
        obj_ev.name = args_4_create['name']
        evs[args_4_create['name']] = obj_ev
        curr_index = Event.evs_names.index(user.users[update.message.chat_id].previous)
        del Event.evs_names[curr_index]
        Event.evs_names.insert(curr_index, args_4_create['name'])
        user.users[update.message.chat_id].deep = 21
        text = options_str[2] + old_option + evs[args_4_create['name']].address
        print(evs)
        m_send(update, context, text, reply_markup)
    elif user.users[update.message.chat_id].deep == 21:
        if update.message.text != button_opt_edit[0]:
            args_4_create['address'] = update.message.text
        else:
            args_4_create['address'] = evs[args_4_create['name']].address
        user.users[update.message.chat_id].deep = 22
        text = options_str[3]+old_option+str(evs[args_4_create['name']].date)
        m_send(update, context, text, reply_markup)
    elif user.users[update.message.chat_id].deep == 22:
        if update.message.text != button_opt_edit[0]:
            t = update.message.text.split(',')
            try:
                if len(t) == 4:
                    args_4_create['date'] = make_date(int(t[0]), int(t[1]), int(t[2]), int(t[3]))
                else:
                    args_4_create['date'] = make_date(int(t[0]), int(t[1]), int(t[2]))
            except (IndexError, ValueError):
                m_send(update, context, options_fail)
            else:
                user.users[update.message.chat_id].deep = 23
                text = options_str[4] + old_option + evs[args_4_create['name']].description
                m_send(update, context, text, reply_markup)
        else:
            args_4_create['date'] = evs[args_4_create['name']].date
            user.users[update.message.chat_id].deep = 23
            text = options_str[4] + old_option + evs[args_4_create['name']].description
            m_send(update, context, text, reply_markup)
    elif user.users[update.message.chat_id].deep == 23:
        if update.message.text != button_opt_edit[0]:
            args_4_create['description'] = update.message.text
        else:
            args_4_create['description'] = evs[args_4_create['name']].description
        user.users[update.message.chat_id].deep = 24
        menu = make_menu(update.message.chat_id, buttons=[button_opt_edit[1]], while_edit=1)
        reply_markup = ReplyKeyboardMarkup(menu, resize_keyboard=True, one_time_keyboard=True)
        m_send(update, context, options_almost, reply_markup)
    elif user.users[update.message.chat_id].deep == 24 and update.message.text == button_opt_edit[1]:
        evs[args_4_create['name']].address = args_4_create['address']
        evs[args_4_create['name']].date = args_4_create['date']
        evs[args_4_create['name']].description = args_4_create['description']
        user = User(update.message.chat_id, 0, 0, '', [])
        menu = make_menu(update.message.chat_id, while_edit=1)
        reply_markup = ReplyKeyboardMarkup(menu, resize_keyboard=True, one_time_keyboard=True)
        m_send(update, context, options_edit_succ, reply_markup)


# Functions for delete events in bot
def destroy_e_f(update, context):
    global user
    user.users[update.message.chat_id].change = -1
    step_1(update, context)

def succ_destroy_e_f(update, context):
    global user, evs
    user.users[update.message.chat_id].change = 0
    evs.pop(update.message.text)
    Event.evs_names.remove(update.message.text)
    menu = make_menu(update.message.chat_id, while_edit=1)
    reply_markup = ReplyKeyboardMarkup(menu, resize_keyboard=True, one_time_keyboard=True)
    m_send(update, context, destroy_succ, reply_markup)

def see_my_host(update, context):
    global user, evs
    text = ''
    for i in evs:
        if update.message.chat_id == evs[i].host_id:
            print(evs[i].nicknames)
            text += "На ваше мероприятие`" + i + "`записались:\n" + '\n@'.join(evs[i].nicknames) + '\n'
    m_send(update, context, text)


# Filters for handlers
class F_step1(BaseFilter):
    def filter(self, message):
        return x in message.text

class F_step_e(BaseFilter):
    def filter(self, message):
        return not re.match(begin, message.text) and not x in message.text and \
               not see_my_e in message.text and not password in message.text and button_opt[0] != message.text and \
                not pass_determine in message.text and not show_org in message.text and \
               not pass_edit in message.text

class F_see_my_e(BaseFilter):
    def filter(self, message):
        return see_my_e in message.text

class F_to_create_e(BaseFilter):
    def filter(self, message):
        return button_opt[0] in message.text

class F_to_to_create_e(BaseFilter):
    def filter(self, message):
        return password in message.text

class F_to_destroy_e(BaseFilter):
    def filter(self, message):
        return pass_determine in message.text

class F_to_to_edit_e(BaseFilter):
    def filter(self, message):
        return pass_edit in message.text

class F_to_see_my_host(BaseFilter):
    def filter(self, message):
        return show_org in message.text



ff_step1 = F_step1()
ff_step_e = F_step_e()
ff_see_my_e = F_see_my_e()
ff_to_to_edit_e = F_to_to_edit_e()

ff_to_create_e = F_to_create_e()
ff_to_to_create_e = F_to_to_create_e()
ff_to_destroy_e = F_to_destroy_e()

ff_to_see_my_host = F_to_see_my_host()

st_handler = CommandHandler('start', start)
st_handler2 = MessageHandler(Filters.regex(begin), start)

to_e_handler = MessageHandler(ff_step1, step_1)
in_e_handler = MessageHandler(ff_step_e, step_in_e)
see_my_e_handler = MessageHandler(ff_see_my_e, see_my_e_f)

begin_create_e_handler = MessageHandler(ff_to_to_create_e, begin_create_e_f)
to_create_e_handler = MessageHandler(ff_to_create_e, to_create_e_f)
to_destroy_e_handler = MessageHandler(ff_to_destroy_e, destroy_e_f)
to_to_edit_e_handler = MessageHandler(ff_to_to_edit_e, to_to_edit_e_f)

to_see_my_host_handler = MessageHandler(ff_to_see_my_host, see_my_host)

welc_handler = MessageHandler(Filters.regex(welcom), welc_ans)
how_a_u_handler = MessageHandler(Filters.regex(a_che_tam), how_a_u)
wrong_handler = MessageHandler(Filters.command, wrong_ans)


for i in (
        st_handler, st_handler2, wrong_handler, welc_handler, how_a_u_handler,
        to_e_handler, in_e_handler, see_my_e_handler,
        begin_create_e_handler, to_create_e_handler, to_destroy_e_handler,
        to_see_my_host_handler, to_to_edit_e_handler
    ):
    dispatcher.add_handler(i)

updater.start_polling()
