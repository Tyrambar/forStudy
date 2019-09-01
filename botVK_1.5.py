import json
import re
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
from datetime import datetime as dat

url_id = 'https://vk.com/id'
# Default buttons
to_begin = 'Вернуться в начало'
cancel1 = 'Отменить запись'
see_my_e = 'Мои записи'
x = ['Ближайшие мероприятия']
agree = ['Пойду на это мероприятие']
show_org = 'Мои посетители'
show_all = 'чо по чем?'

# Default messages from bot
hi_from_bot = ("Добро пожаловать! Хотите посмотреть ближайшие планируемые мероприятия?\n"
"Вы можете записаться на любое из них и всегда посмотреть имеющиеся записи🙂."
"А если планы изменились, отменить записи\n"
'\n\nТакже предлагаем посетить мероприятия наших партнеров - они подсвечены синим цветом\n'
"📌Обратите внимание на значок в поле сообщений, рядом со смайлом. "
"Нажмите на него, чтобы увидеть кнопки для удобной работы.")
choice_e = 'Выберите мероприятие: напишите его дату, порядковый номер или нажмите на кнопку:\n'
confirm = 'Вы записались на '
wrong = ('😔 Я не могу вас понять\nВы можете попробовать снова:\n'
'📌 Откройте рядом со смайликами квадратную иконку для удобной навигации\n📌 Напишите Привет, чтобы начать разговор заново')
cancel_all = 'Ваша запись отменена.'
mes_see = 'Можете снова просмотреть те мероприятия💬, куда вы записались.\n' \
          'Чтобы отменить запись, нажмите на него или напиши - ' \
          'там будет кнопка "отменить запись"\n\nРанее Вы записались на:\n'
options = 'Чтобы добавить мероприятие, вам нужно заполнить поэтапно :\n' \
          '📌Краткое описание мероприятия, которое будет отображаться на кнопке - ДО 40 СИМВОЛОВ\n' \
          '📌Адрес места проведения\n' \
          '📌Описание места проведения - обычный enter для разделения абзацев не подойдет. Пишите \\n и если хотите оставить пустую строку, то пишите два раза: \\n\\n \n' \
          '📌Ключевые слова по мероприятию СТРОГО через ЗАПЯТУЮ\n' \
          '📌Напечатать/нажать кнопку - является ли это мероприятие от фрайдата или нет? (да/нет)\n' \
          '📌Ввести номер id организатора этого мероприятия\n' \

mes_a_che_tam = 'Нормас\nна движ-то какой-нибудь пойдешь?'
welc = 'Пожалуйста)\nЭто моя работа😄'
e = ["Фестиваль 25.05 12ч м.Красносельская", "Настолки 26.05 18ч м.Китай-город", "Туса в Турции 1-15 июля"]
e_adress = ["Нижняя Красносельская 35сК", 'Маросейка 13с1', 'Турция']

confirmed = {e[0]: [], e[1]: [95372442, 159542333, 166307242, 382620531, 293320616, 273880438], e[len(e)-1]: []}
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
e[1]: ("Настолки 26 мая в 18:00 в Jeffrey's Coffee на Маросейке 13с1, м. Китай-город.\n\n"
'Хей, скучал по нашим настолкам?\n\n'
"Приходи в антикафе Jeffrey's Coffee на Маросейке и сразись с лучшими из лучших!\n"
'Не уверен в своих силах? Не знаешь правила игры? Ничего страшного! Наши очаровательные ведущие всему научат и обо всем расскажут.\n'
'Считаешь себя экспертом? Приходи и докажи!\n'
'Просто хочешь хорошо провести время? Присоединяйся к нашей дружной компании и проведи запоминающийся вечер.\n'),
e[len(e)-1]: ("Летом, с 1 по 15 июля состоится Sea || Summer || Students - большая летняя тусовка на море для молодежи.\n"
"Более 100 человек отправится на южный берег Турции. Уже второй по счету выезд станет еще масштабнее и интереснее!\n"
"Бары, дискотеки, экскурсии и квесты - нам будет чем заняться! "
"А теплое Средиземное море создаст лучшую атмосферу для большого молодежного праздника)")
}
# Words for reading from keyboard
e_anss = (
(e[0], ['25.05', '25.5', '25 мая', 'фестиваль', 'культурный', 'культурный фестиваль', 'вс']),
(e[1], ['26.05', '26.5', '26 мая', 'настолки', 'настолочки', 'вс']),
(e[len(e)-1], ['01.07', '15.07', '01.07-15.07', '1-15 июля', '1.7', '1 июля', 'июль',
               "туса на море", "море", "турция"])
)


def e_anss_all_f():
    lst = []
    for i in e_anss:
        lst.extend(i[1])
    return lst
e_anss_all = e_anss_all_f()

def e_a_numb(m):
    return [f'{m}', f'{m}.', f'{m}-ое']

e_anss_numb_e = []
for n in range(len(e)):
    e_anss_numb_e.extend(e_a_numb(n+1))

def e_anss_del(e_anss_f):
    if args_ind[event.user_id]['pp']:
        for o in seen_all:
            for k in range(args_ind[event.user_id]['pp']):
                for j in e_a_numb(k + 1):
                    if j in e_anss_f[o][1]:
                        e_anss_f[o][1].remove(j)
    elif args_ind[event.user_id]['seen_xx']:
        for k in range(len(e_types[some_x])):
            for m in e_anss_f:
                if e_types[some_x][k] == m[0]:
                    for j in e_a_numb(k + 1):
                        if j in m[1]:
                            e_anss_f[e_anss_f.index(m)][1].remove(j)
    else:
        for o in range(len(e)):
            for j in e_a_numb(o + 1):
                if j in e_anss_f[o][1]:
                    e_anss_f[o][1].remove(j)
    return e_anss_f
## Function for

ok = r'(записаться)|(х[очуатю]{3})|(д[ао]вай)|(п[ао]й[дуеёмти])|(п[ао]?шли)|(да+)|((го)+у*)|(ид[ёемду])|(к[ао]не[чш]н[ао]*)|(ок[ейи]*)'
nearest = r'(близ?жайш[ие]е!*)|([после]*завтр[ао])|([в ]*выходн[ыеой]*)'
begin = r'(меню)|(старт[уй]*)|(прив[етствую]*)|(добр[огоыйе]+( )?[утроаодняденьвечера]*)|' \
        r'([вс]* ?нач[ниалоать]*)|([здао]*р[аоваствуйте]*)|(хай)|(hi)|(hello)|(ку)'
a_che_tam = r'([а ]*ч[еёо]{1} там\??)|(как [тыдела]\??)'
welcom = r'(с?пас[ие]б[ао]*)|(благодарю?[ствую]*[им]*)|(но?рм[ас]*)|(к ?р ?а ?с ?[иа]? ?в ?[ао]?[чик]*)'


# Supporting functions
def butt(dct, size, c, color, label1, label2 = None, color2 = None):
    if size == 1:
        if label1 == e[len(e)-1]:
            color = 'default'
        if label1 == e[0]:
            color = 'primary'
        dct['buttons'].append([{
            "action": {
            "type": "text",
            "payload": '{"button": "%d"}' % (c),
            "label": label1
            },
            "color": color
        }])
    elif size == 2:
        dct['buttons'].append([{
            "action": {
            "type": "text",
            "payload": '{"button": "%d"}' % c,
            "label": label1},
            "color": color},
            {"action": {
            "type": "text",
            "payload": '{"button": "%d"}' % (c + 1),
            "label": label2},
            "color": color2
            }])

    return dct

def keyb1(lst=None, y=None, conf=None, id=None, canc=None):
    keyb = {"one_time": None, "buttons": []}
    c=1
    seen = False
    if canc:
        for i in conf:
            if id in conf[i]:
                butt(keyb, 1, c, "positive", i)

        butt(keyb, 1, c, "primary", to_begin)

    else:
        if lst:
            if lst == x:
                butt(keyb, 1, c, "positive", x[0])
            else:
                for i in lst:
                    butt(keyb, 1, c, "positive", str(i))

        if id == None and conf == None and y != 0:
            butt(keyb, 1, c, "primary", to_begin)

        elif id != None and conf != None:
            for i in conf:
                if id in conf[i]:
                    if y == 0:
                        butt(keyb, 1, c, "primary", see_my_e)
                    else:
                        butt(keyb, 2, c, "primary", to_begin, see_my_e, "positive")
                        if y == 2:
                            butt(keyb, 1, c, "default", cancel1)
                    seen = True

                    break
            if seen == False and y != 0:
                butt(keyb, 1, c, "primary", to_begin)

    if id in admins:
        butt(keyb, 1, c, "negative", show_all)
    elif id in orgs:
        butt(keyb, 1, c, "negative", show_org)

    return keyb

def m_send(user, message, keyboard = None):
    return vk.messages.send(user_id = user, message = message, keyboard = keyboard, random_id = get_random_id())

# Main with data
token = ''
admins = [43132896, 293320616, 291093703, 95372442]
orgs = {98384985: [e[0]]}
vk_session = vk_api.VkApi(token=token)
longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()

# Supporting arguments for order of actions of bot
def clear_go_e():
    go_e = []
    for i in e:
        go_e.append(False)
    return go_e
go_e = clear_go_e()

def args_ind_add(argss_ind, ind_id, pp, deep, seen_xx):
    argss_ind[ind_id] = {'pp': pp, 'deep': deep, 'seen_xx': seen_xx}
    return argss_ind


# Helpings args
password = 'праотцы'
args_ind = {}
previous = ''
# подтверждение/отмена записи - 0; приветствие - 1; список - 2; мои записи - 3; мероприятие - 4
for event in longpoll.listen():
    try:
        if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
            current = event.text
            if event.user_id not in args_ind:
                args_ind = args_ind_add(args_ind, event.user_id, 0, 0, 0)
            print(args_ind[event.user_id]['deep'])
            if re.match(begin, current.lower()) or current == to_begin:
                args_ind[event.user_id]['deep'] = 0
            if current.lower() == password and event.user_id in admins:
                m_send(event.user_id, cancel_all, json.dumps(keyb1(None, 1, None, None), ensure_ascii=False))

            if current == show_all and event.user_id in admins:
                text = ''
                for i in range(len(e)):
                    text += f"На мероприятие '{e[i]}' идут: {url_id}{f', {url_id}'.join([str(j) for j in confirmed[e[i]]])}\n"
                m_send(event.user_id, text)
                text = ''
            elif current == show_org and event.user_id in orgs:
                text = ''
                if confirmed[orgs[event.user_id][0]] == []:
                    text+='Пока записей нет\n'
                else:
                    for i in orgs[event.user_id]:
                        text += f"На твое мероприятие '{i}' идут: " \
                           f"{url_id}{f', {url_id}'.join([str(j) for j in confirmed[i]])}\n"
                m_send(event.user_id, text)
                e_anss = e_anss_del(e_anss)
                text = ''
            elif 'записи' in current.lower() or current == see_my_e:
                args_ind[event.user_id]['deep'] = 3
                see_my = mes_see
                pp = 0
                seen_all = []
                for n, i in enumerate(confirmed):
                    if event.user_id in confirmed[i]:
                        see_my += f'{n}. {i} по адресу {e_adress[e.index(i)]}\n'
                        if e_a_numb(pp+1)[0] not in e_anss[n][1]:
                            e_anss[n][1].extend(e_a_numb(pp+1))
                            e_anss_all.extend(e_a_numb(pp+1))
                            seen_all.append(n)
                        pp+=1
                args_ind[event.user_id]['pp'] = pp
                m_send(event.user_id, see_my, json.dumps(keyb1(None, None, confirmed, event.user_id, 1),
                                                          ensure_ascii=False))
                see_my = ''
            elif re.match(a_che_tam, current.lower()):
                m_send(event.user_id, mes_a_che_tam)
            # Возврат сообщения о неверном вводе, отображение подсказок
            elif re.match(welcom, current.lower()):
                m_send(event.user_id, welc)
            # Приветствуем пользователя - начало работы
            elif args_ind[event.user_id]['deep'] == 0 and current.lower() not in e_anss_all and current.lower() not in e_anss_numb_e:
                print('suka')
                args_ind[event.user_id]['deep'] = 1
                m_send(event.user_id, hi_from_bot, json.dumps(keyb1(x, 0, confirmed, event.user_id),
                                                              ensure_ascii = False))
                # При приветствии обнуляется предшествующий выбор какого-либо мероприятия
                go_e = clear_go_e()
                e_anss = e_anss_del(e_anss)
                e_anss_all = e_anss_all_f()
                args_ind[event.user_id]['seen_xx'] = 0
            # Отображение списка грядущих мероприятий
            elif args_ind[event.user_id]['deep'] == 1 and current.lower() not in e_anss_all and current.lower() not in e_anss_numb_e:
                text = choice_e
                args_ind[event.user_id]['pp'] = 0
                args_ind[event.user_id]['deep'] = 2
                for k, i in enumerate(e):
                    text += f"{k+1}. {i}\n"
                m_send(event.user_id, text, json.dumps(keyb1(e, 1, confirmed, event.user_id),
                                                       ensure_ascii=False))
                # Добавление порядкового номера мероприятия
                for n in range(len(e)):
                    if e_a_numb(n+1)[0] not in e_anss[n][1]:
                        e_anss[n][1].extend(e_a_numb(n+1))
                        e_anss_all.extend(e_a_numb(n+1))
                text = ''
            # Описание выбранного мероприятия, возврат переменной, подтверждающией просмотр конкретного мероприятия
            elif (args_ind[event.user_id]['deep'] in (2, 3) and current in e) or current.lower() in e_anss_all:
                args_ind[event.user_id]['deep'] = 4
                for n, i in enumerate(e):
                    if current.lower() in e_anss[n][1] or current == i:
                        if event.user_id in confirmed[e[n]]:
                            m_send(event.user_id, events_d[i], json.dumps(keyb1(None, 2, confirmed, event.user_id),
                                              ensure_ascii=False))
                        else:
                            m_send(event.user_id, events_d[i], json.dumps(keyb1(agree, 1, confirmed, event.user_id),
                                                                      ensure_ascii=False))
                        go_e[n] = True
                        numb = n
                        e_anss = e_anss_del(e_anss)
                        break
                e_anss_all = e_anss_all_f()
            elif args_ind[event.user_id]['deep'] == 4:
                # Отмена всех записей пользователя
                if current == cancel1 or 'отмен' in current.lower() or ((previous == see_my_e or 'записи' in previous.lower()) and \
                    current.lower() in e_anss_all):
                    m_send(event.user_id, cancel_all, json.dumps(keyb1(None, 1, None, None), ensure_ascii=False))
                    if current != cancel1 and 'отмен' not in current.lower():
                        for i in e_anss:
                            if current.lower() in i[1]:
                                if event.user_id in confirmed[i[0]]:
                                    confirmed[i[0]].remove(event.user_id)
                                break
                    else:
                        if event.user_id in confirmed[e[numb]]:
                            confirmed[e[numb]].remove(event.user_id)
                    e_anss = e_anss_del(e_anss)
                    e_anss_all = e_anss_all_f()
                # Подтверждение записи на мероприятие, обнуление переменной, подтверждавшей просмотр выбранного мероприятия
                elif True in go_e and (previous in e or re.match(ok, current.lower())):
                    m_send(event.user_id, f'{confirm}{e[n]}', json.dumps(keyb1(None, 1, confirmed, event.user_id),
                                                                  ensure_ascii=False))
                    go_e[numb] = False
                    # Запись человека на мероприятие, отсылка сообщений админам, что человек посетит данное мероприятие
                    confirmed[e[numb]].append(event.user_id)
                    e_anss = e_anss_del(e_anss)
                    e_anss_all = e_anss_all_f()
                else:
                    m_send(event.user_id, wrong)
            # Просмотр пользователем своих записей с более подробным адресом
            else:
                m_send(event.user_id, wrong)
            previous = current
    except (IndexError, KeyError):
        m_send(event.user_id, wrong)