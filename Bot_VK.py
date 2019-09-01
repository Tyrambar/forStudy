import json
import re
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
from datetime import datetime as dat
from datetime import date as da
from datetime import time as ti

url_id = 'https://vk.com/id'

# Default buttons
to_begin = 'Вернуться в начало'
cancel1 = 'Отменить запись'
see_my_e = 'Мои записи'
x = ['Ближайшие мероприятия']
agree = ['Пойду на это мероприятие']
button_opt = ['Создать мероприятие', 'Добавить мероприятие']
bgc_button_opt = ['Создать день мероприятия', 'Добавить день мероприятия',
                  'Создать игру на мероприятие', 'Добавить игру на мероприятия']
show_org = 'Мои посетители'
show_all = 'чо по чем?'
spam = 'Рассылка'
spam_succ = 'Рассылка успешно разослана!'

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

send_spam = 'Выберете мероприятия, по которому хотите сделать рассылку:\n'
spam_d = 'Напишите текст оповещения мероприятия\n'

# Описание добавления мероприятия через пароли
options = 'Чтобы добавить мероприятие, вам нужно заполнить поэтапно :\n' \
          '📌Краткое описание мероприятия, которое будет отображаться на кнопке - ДО 40 СИМВОЛОВ\n' \
          '📌Адрес места проведения мероприятия. Пример: Маросейка 13с1\n' \
          '📌Дата проведения (месяц, дата, час, минуты (по умолчанию 0) - разделение через запятую). Пример: 5, 25, 18, 30\n' \
          '📌Описание места проведения\n' \
          '📌Ключевые слова по мероприятию СТРОГО через ЗАПЯТУЮ. Пример: 25 мая, настолки, настольные игры\n' \
          '📌Напечатать (да/нет) - является ли это мероприятие от фрайдата?' \
          ' И ввести номер id организатора этого мероприятия ЧЕРЕЗ ЗАПЯТУЮ. Пример, если от организатора: да, 95372442. Пример, если от фрайдат: нет'

bgc_e_options = 'Чтобы добавить день мероприятия, вам нужно заполнить поэтапно :\n' \
          '📌Краткое описание, заголовок мероприятия, которое будет отображаться на кнопке - ДО 40 СИМВОЛОВ\n' \
          '📌Этот день - официальный игровой вечер (да/нет)? Пример: да\n' \
          '📌Адрес места проведения мероприятия. Выберите из предложенных.\n' \
          '📌Дата проведения (месяц, дата - разделение через ЗАПЯТУЮ). Пример: 5, 31'

            #Начало игры в 19:00; До 7-ми игроков\nОписание игры, руководство: 'https://tesera.ru/game/bohnanza/\nДлительность партии 60 минут',
bgc_g_options = 'Чтобы добавить игру на день мероприятия, вам нужно заполнить поэтапно :\n' \
          '📌Выбрать из перечня текущих дней-мероприятий, когда будет проходить игра\n' \
          '📌Название игры, которое будет отображаться на кнопке - ДО 20 СИМВОЛОВ\n' \
          '📌Время проведения (час, минуты(по умолчанию 0) - разделение через ЗАПЯТУЮ). Пример: 19, 30\n' \
          '📌Ссылку на описание игры, или краткое пояснение к ней\n' \
          '📌Максимальное количество игроков(число), разделение через запятую затем примерная длительность партии(число-). Пример: 8, 60-120'

options_str = options.split('\n')
options_bgc_e_str = bgc_e_options.split('\n')
options_bgc_g_str = bgc_g_options.split('\n')
options_fail = 'Неправильно записаны данные'
options_almost = 'Подтвердите добавление мероприятия'
options_succ = 'Мероприятие успешно добавлено!'

destroy_succ = 'Мероприятие успешно испепелено!!!'
bgc_e_destroy_succ = 'День мероприятия успешно удалено!'
bgc_g_destroy_succ = 'Игра в день мероприятия успешно удалена!'

bgc_spam_txt = 'Посмотрите наши игры, которые пройдут в этот день:\n\n'
mes_a_che_tam = 'Нормас\nна движ-то какой-нибудь пойдешь?'
welc = 'Пожалуйста)\nЭто моя работа😄'

months = {1: 'января', 2: 'февраля', 3: 'марта', 4: 'апреля', 5: 'мая', 6: 'июня',
          7: 'июля', 8: 'августа', 9: 'сентября', 10: 'октября',  11: 'ноября', 12: 'декабря'}
daysweek = {'Monday': 'понедельник', 'Tuesday': 'вторник', 'Wednesday': 'среда',
'Thursday': 'четверг','Friday': 'пятница', 'Saturday': 'суббота', 'Sunday': 'воскресенье'}


e_dates = {"Мафия на англ. языке 7.06": dat(2019, 6, 7, 19, 30),
           'Cashflow 8.06 в 15ч': dat(2019, 6, 8, 15),
           "Туса в Турции 1-15 июля": dat(2019, 7, 1, 18)}

"""!!! Все имена переменных с bgc - это для отдельных чуваков, там структура бота многоуровневая: 
ближайшие мероприятия > эти чуваки > дни их мероприятий > сами мероприятия (настольные игры) ..
обычная же: ближайшие мероприятия > мероприятие > описание мероприятия > пойду (ты записался) / отменяю (отменил запись)
"""
bgc_e_dates = {'Официальный игровой вечер 29 Мая': da(2019, 5, 29)
}

bgc_e = ['Официальный игровой вечер 29 Мая']
bgc_games = {bgc_e[0]: ['Поморская лоция', 'Канагава', 'Pandemic:Rising Tide',
                        'Бонанза', 'Косм. дальнобойщики', 'В. западный путь',
                        'Downfall of Pompeii', 'Dice Forge', 'Bang! Dice Game:TWD',
                        'Panic Station', "Chiyo's Secret", 'Res Arcana (adv.)',
                        'Цербер', 'Кор. хроники', 'Гунны', 'Селестия с допом',
                        'Вороны', 'Гембло Q и Гембло']
}
bgc_all_games = [j for i in bgc_games for j in bgc_games[i]]
bgc_g_dates = {
    bgc_e[0]:
           {
               bgc_games[bgc_e[0]][0]: ti(18, 15),
               bgc_games[bgc_e[0]][1]: ti(19, 1),
               bgc_games[bgc_e[0]][2]: ti(19, 2),
               bgc_games[bgc_e[0]][3]: ti(19, 3),
               bgc_games[bgc_e[0]][4]: ti(19, 4),
               bgc_games[bgc_e[0]][5]: ti(19, 5),
               bgc_games[bgc_e[0]][6]: ti(19, 6),
               bgc_games[bgc_e[0]][7]: ti(20),
               bgc_games[bgc_e[0]][8]: ti(21, 1),
               bgc_games[bgc_e[0]][9]: ti(21, 2),
               bgc_games[bgc_e[0]][10]: ti(21, 3),
               bgc_games[bgc_e[0]][11]: ti(21, 4),
               bgc_games[bgc_e[0]][12]: ti(22),
               bgc_games[bgc_e[0]][13]: ti(22),
               bgc_games[bgc_e[0]][14]: ti(22),
               bgc_games[bgc_e[0]][15]: ti(22),
               bgc_games[bgc_e[0]][16]: ti(22),
               bgc_games[bgc_e[0]][17]: ti(22)
           }
}

bgc = 'Board Game Club'
# Список мероприятий, дальше из него формиуются словари по всяким другим переменным
e = ["Мафия на англ. языке 7.06", 'Cashflow 8.06 в 15ч', "Туса в Турции 1-15 июля"]
e_view = [bgc]
e_view.extend(e)

# Переменные для подсвечивания синим или зеленым - мероприятия чисто от нас или других организаторов
e_who = {bgc: 1, e[0]: 1, e[1] : 1, e[len(e)-1]: 0}

e_adress = {e[0]: 'ул. Кузнецкий мост 19с1',
            e[1]: ' м. Бауманская, ул. Нижняя Красносельская 35/52', e[len(e)-1]: 'Турция'}

bgc_places = ['паб Guns & Bears', 'Wooden Door', 'КЦ ЗИЛ', 'Шахматный клуб "Белая Ладья"']

bgc_adress = {bgc_places[0]: 'Новослободская ул. 46к1',
              bgc_places[1]: 'Милютинский пер., 6c1',
              bgc_places[2]: 'Восточная ул., 4c1',
              bgc_places[3]: 'Нескучный сад, по дороге мимо домов 18, 20 Ленинского пр-та'}
			  
bgc_adress_d = {
    bgc_adress[bgc_places[0]]: 'Основная группа игроков - в глубине помещения в красном зале + по пабу кто где.\nКак пройти: https://yandex.ru/maps/-/CCBOA0kE\n',
    bgc_adress[bgc_places[1]]: 'Оплата по формату антикафе - 2р/мин за первые 2ч, далее 1р/мин, только наличные, иметь при себе паспорт,' \
                   ' т.к. есть опции взять кальян, пиво к бургерам и пицце и т.п.\nКак пройти:https://yandex.ru/maps/-/CCvg46Zz\n',
    bgc_adress[bgc_places[2]]: 'Библиотека на третьем этаже, либо между этажами за столиками\nКак пройти: https://yandex.ru/maps/-/CCBOAT4X\n',
    bgc_adress[bgc_places[3]]: 'Можно зайти из Парка Горького (вверх от театра Стаса Намина по тропинкам. Рядом с Хлебом насущным),' \
                    ' либо с Ленинского проспескта, дорога между домами 18 и 20\nКак пройти: https://yandex.ru/maps/-/CCBOEQKr\n',
}

bgc_e_adress = {
    bgc_adress[bgc_places[0]]: [bgc_e[0]],
    bgc_adress[bgc_places[1]]: [],
    bgc_adress[bgc_places[2]]: [],
    bgc_adress[bgc_places[3]]: []
}
# Номера id зарегистрировавшихся
confirmed = {bgc: [], e[0]: [], e[1] : [], e[len(e)-1]: [293320616, 207863232]}

bgc_confirmed = {
    bgc_e[0]:
        {'Поморская лоция': ['Ира', 'Антон'],
         'Канагава': ['Денис', 'Алексей', 'Антон'],
         'Pandemic:Rising Tide': ['Борис', 'друг Бориса', 'Лев'],
         'Бонанза': ['Андрей', 'Николай', 'Настик', 'Стефа'],
         'Косм. дальнобойщики': ['Даниил', 'Алексей', 'Ян'],
         'В. западный путь': ['Лида', 'Таня', 'Боря'],
         'Downfall of Pompeii': ['Александр'],
         'Dice Forge': ['Алексей', 'Ира', 'Николай', 'Антон'],
         'Bang! Dice Game:TWD': ['Денис', 'Алексей', 'Антон', 'Ира', 'Николай', 'Марина', 'Ян'],
         'Panic Station': [],
         "Chiyo's Secret": ['Евгений', 'Лена', 'Андрей', 'Оля'],
         'Res Arcana (adv.)': [],
         'Цербер': ['Даниил', 'Паша', 'Влад'],
         'Кор. хроники': [],
         'Гунны': [], 'Селестия с допом': [], 'Вороны': [], 'Гембло Q и Гембло': []}
    }

bgc_games_d = {
    bgc_e[0]: {
        bgc_games[bgc_e[0]][0]: 'Начало игры в 18:15; До 4-ех игроков\nОписание игры, руководство: ' \
                    'https://tesera.ru/game/pomorskaya-lotsiya\nДлительность партии 30-60 минут',
        bgc_games[bgc_e[0]][1]: 'Начало игры в 19:00; До 4-ех игроков\nУчимся японской живописи ' \
                    '\nДлительность партии 60 минут',
        bgc_games[bgc_e[0]][2]: 'Игра Космические дальнобойщики. Начало в 19:00; До 4-ех игроков\nОписание игры, руководство: ' \
                    'https://tesera.ru/game/pandemic-rising-tide/\nДлительность партии 120 минут',
        bgc_games[bgc_e[0]][3]: 'Начало игры в 19:00; До 7-ми игроков\nОписание игры, руководство: ' \
                                'https://tesera.ru/game/bohnanza/\nДлительность партии 60 минут',
        bgc_games[bgc_e[0]][4]: 'Начало игры в 19:00; До 4-ех игроков\nОписание игры, руководство: ' \
                                'https://tesera.ru/game/6974\nДлительность партии 120-150 минут',
        bgc_games[bgc_e[0]][5]: 'Игра Великий западный путь. Начало в 19:40; До 3-ех игроков\nОписание игры, руководство: ' \
                                'Гони коровку в светлое будущее. ( Бургеры наше все ) \nДлительность партии 150-180 минут',
        bgc_games[bgc_e[0]][6]: 'Начало игры в 19:00; До 4-ех игроков\nОписание игры, руководство: ' \
                                'https://tesera.ru/game/The-Downfall-of-Pompeii/\nДлительность партии 60 минут',
        bgc_games[bgc_e[0]][7]: 'Начало игры в 19:00; До 4-ех игроков\nОписание игры, руководство: ' \
                    'https://tesera.ru/game/dice-forge/\nДлительность партии 60 минут',
        bgc_games[bgc_e[0]][8]: 'Начало игры в 21:00; До 8-ми игроков\nКубиковый Бэнг с ходячими мертвецами, Карл!' \
                    '\nДлительность партии 60 минут',
        bgc_games[bgc_e[0]][9]: 'Начало игры в 21:00; До 6-ти игроков\nОписание игры, руководство: ' \
                    'https://tesera.ru/game/panic-station/\nДлительность партии 60-90 минут',
        bgc_games[bgc_e[0]][10]: 'Начало игры в 21:00; До 8-ми игроков\nОписание игры, руководство: ' \
                                'https://tesera.ru/game/chiyos-secret/\nДлительность партии 45-60 минут',
        bgc_games[bgc_e[0]][11]: 'Начало игры в 21:00; До 3-ех игроков\nБыстрая игра' \
                                '\nДлительность партии 20-40 минут',
        bgc_games[bgc_e[0]][12]: 'Игры от издательства "Эврикус". Начало игры после 19:00; До 7-ми игроков\n'
                  'Описание игры, руководство: ' \
                                'https://tesera.ru/game/Cerberus/\nДлительность партии 40-90 минут',
        bgc_games[bgc_e[0]][13]: 'Игра Королевские хроники.  От издательства "Эврикус". Начало после 19:00; До 5-ти игроков\n'
                  'Описание игры, руководство: ' \
                                'https://tesera.ru/game/Paper-Tales/\nДлительность партии 60 минут',
        bgc_games[bgc_e[0]][14]: 'Игры от издательства "Эврикус". Начало игры после 19:00; До 4-ех игроков\n'
                  'Описание игры, руководство: ' \
                                'https://tesera.ru/game/huns/\nДлительность партии 60-120 минут',
        bgc_games[bgc_e[0]][15]: 'Игры от издательства "Эврикус". Начало игры после 19:00; До 6-ти игроков\n'
                  'Описание игры, руководство: ' \
                                'https://tesera.ru/game/celestia/\nДлительность партии 60 минут',
        bgc_games[bgc_e[0]][16]: 'Игры от издательства "Эврикус". Начало игры после 19:00; До 2-ух игроков\n'
                  'Описание игры, руководство: ' \
                                'https://tesera.ru/game/Odins-Ravens-2ed/\nДлительность партии 30 минут',
        bgc_games[bgc_e[0]][17]: 'Игры от издательства "Эврикус". Начало игры после 19:00; До 6-ти игроков\n'
                  'Описание игры, руководство: ' \
                                'https://tesera.ru/game/gemblo/\nДлительность партии 30 минут',
    }
}

bgc_offic = {bgc_e[0] : 'negative'}

events_d = {
e[0] : ('Если вы хотите весело привести время, а также потренировать свой английский, welcome to Mafia in English!\n' 
'Ждем вас в пятницу в антикафе Циферблат!\n\n'
'Оплата по тарифу антикафе (первые 2 часа - 3р минута, дальше 2р, стоп-чек - 600р)\n'
'Регистрация обязательна'),
e[1] : ('Игра "Денежный Поток" - финансово-образовательная настольная игра, которая обучает начальным знаниям инвестирования и финансовой грамотности.'
'Игра создана американским миллионером японского происхождения Робертом Кийосаки.\n\n'
'ПО РЕЗУЛЬТАТАМ ИГРЫ УЧАСТНИК УЗНАЕТ:\n'
'- как создать источники дохода?\n'
'- что такое инвестирование?\n'
'- куда можно инвестировать деньги?\n'
'- как распоряжаются деньгами богатые люди?\n'
'- какие у Вас «отношения» с деньгами?\n'
'- как получать доход, даже не работая?\n'
'- как можно зарабатывать не зависимо от состояния рынка?\n'
'- как заставить деньги работать на Себя?\n'
'Помимо игры происходит разбор ваших стратегий, приятное общение с активными людьми и полезные знакомства.\n'
'Сбор 150 рублей.'),
bgc : ('Мы представляем Board Game Community в Москве и проводим игровые вечера в различных публичных заведениях столицы.\n\n'
'Наши встречи подойдут Вам идеально, если Вы:\n\n'
'► Любите настольные игры или только хотите познакомиться с этим увлекательным миром\n'
'► Ищете новых знакомств, ярких эмоций или просто хотите провести вечер в приятной компании\n'
'► Цените в настольных играх не только игровую составляющую, но и социальную\n'
'► Хотите увлечь своих знакомых, друзей и близких этим замечательным хобби\n'
'Вход и участие - бесплатно.\n'
'Добро пожаловать в нашу дружную команду!\n\n'),
e[len(e)-1]: ("Летом, с 1 по 15 июля состоится Sea || Summer || Students - большая летняя тусовка на море для молодежи.\n"
"Более 100 человек отправится на южный берег Турции. Уже второй по счету выезд станет еще масштабнее и интереснее!\n"
"Бары, дискотеки, экскурсии и квесты - нам будет чем заняться! "
"А теплое Средиземное море создаст лучшую атмосферу для большого молодежного праздника)")
}


# Words for reading from keyboard - ключевые слова, которые вводишь в любом шаге, и перейдешь в шаг описания мероприятия
e_anss = {
e[0] : ['мафия'],
e[1] : ['денежный поток', 'cashflow'],
bgc: [],
e[len(e)-1]: ['01.07', '15.07', '01.07-15.07', '1-15 июля', '1.7', '1 июля', 'июль',
               "туса на море", "море", "турция"]
}
bgc_anss = {}
bgc_anss_all = []

def make_date(month, date, hour, min = 0):
    return dat(2019, month, date, hour, min)


def e_anss_all_f():
    lst = []
    for i in e_anss:
        if i != bgc:
            lst.extend(e_anss[i])
    return lst
e_anss_all = e_anss_all_f()

# Функция для того, чтоб можно было при отображении списка мероприятий вызвать мероприятие по вводу числа
def e_a_numb(m):
    return [f'{m}', f'{m}.', f'{m}-ое']

e_anss_numb_e = []
for n in range(len(e)):
    e_anss_numb_e.extend(e_a_numb(n+1))

bgc_e_numbs = []
bgc_g_numbs = []

# Функция для удаления строк-номеров мероприятий
def e_anss_del(e_anss_f):
    if e_anss[bgc] != []:
        e_anss[bgc] = []
    if args_ind[event.user_id]['pp']:
        for k in range(1, len(registr)+1):
            for u in e_anss_f:
                for j in e_a_numb(k + 1):
                    if j in e_anss_f[u]:
                        e_anss_f[u].remove(j)
    else:
        for n, o in enumerate(e_view):
            for j in e_a_numb(n + 1):
                if j in e_anss_f[o]:
                    e_anss_f[o].remove(j)
    return e_anss_f


ok = r'(записаться)|(х[очуатю]{3})|(д[ао]вай)|(п[ао]й[дуеёмти])|(п[ао]?шли)|(да+)|((го)+у*)|(ид[ёемду])|(к[ао]не[чш]н[ао]*)|(ок[ейи]*)'
nearest = r'(близ?жайш[ие]е!*)|([после]*завтр[ао])|([в ]*выходн[ыеой]*)'
to_menu = r'(меню)|([вс]* ?нач[ниалоать]*)|(назад)|(занов[ао])'
begin = r'(\bстарт[уй]*\b)|(прив[етствую]*)|(\bдобр[огоыйе]+ ?[утроаодняденьвечера]*\b)|([здао]+р[аоваствуйте]+)|(\bхай\b)|(hi)|(hello)|(\bку[ку]*\b)|(sta*rt)'
a_che_tam = r'([а ]*ч[еёо]{1} там\??)|(как [тыдела]\??)'
welcom = r'(с?пас[ие]б[ао]*)|(благодарю?[ствую]*[им]*)|(но?рм[ас]*)|(к ?р ?а ?с ?[иа]? ?в ?[ао]?[чик]*)'


# Supporting functions

# Для кнопки
def butt(dct, size, c, color, label1, label2 = None, color2 = None, label3 = None, color3 = None):
    if size == 1:
        if label1 in bgc_e:
            color = bgc_offic[label1]
        if label1 == e[len(e)-1]:
            color = 'default'
        if label1 in e_view and label1 in e_who:
            #print('e_who', e_who)   print('label1: ', label1)
            if e_who[label1] == 1:
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
    elif size == 3:
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
            "color": color2},
            {"action": {
            "type": "text",
            "payload": '{"button": "%d"}' % (c + 2),
            "label": label3},
            "color": color3
            }])
    return dct

# Параметры клавы
def keyb1(lst=None, y=1, conf=None, id=None, regist=None):
    keyb = {"one_time": None, "buttons": []}
    c=1
    seen = False
    if regist:
        for i in regist:
            butt(keyb, 1, c, "positive", i)
        butt(keyb, 1, c, "primary", to_begin)
    else:
        if lst:
            if len(lst) < 7:
                for i in lst:
                    butt(keyb, 1, c, "positive", str(i))
            else:
                z = 0
                while z <= len(lst)-1:
                    z2 = z+1
                    if z2 == len(lst):
                        butt(keyb, 1, c, "positive", str(lst[z]))
                        break
                    else:
                        butt(keyb, 2, c, "positive", str(lst[z]), str(lst[z2]), "positive")
                        z = z2
                        z+=1
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

    if args_ind[event.user_id]['deep'] < 5:
        if id in admins:
            butt(keyb, 2, c, "negative", show_all, spam, "default")
        elif id in orgs:
            butt(keyb, 1, c, "negative", show_org)


    return keyb

def m_send(user, message, keyboard = None):
    return vk.messages.send(user_id = user, message = message, keyboard = keyboard, random_id = get_random_id())

# Main with data
#pr = 158049316 ; f = 173884811 #291093703 43132896 291093703, 448434073
group_i = '158049316'
token_profit_m = ''
admins2 = [291093703, 208877115, 448434073]
admins = [95372442, 43132896, 293320616]
orgs = {448434073: bgc, 9310639: e[1]}
vk_session = vk_api.VkApi(token=token_profit_m)
longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()

members =[]
# Список кому отсылать уведомления
members_spam = []
# Сколько последних добавленных людей посмотреть (чтобы проверить на новых юзеров в сообществе,  не создавая с нуля этот список
how_much_growth = 15
# Supporting arguments for order of actions of bot

# Функция, очищающая вспомогательный список, который проверяет, какое мероприятие было выбрано
def clear_go_e():
    go_e = []
    for i in e:
        go_e.append(False)
    return go_e

go_e = clear_go_e()

# У каждого пользователя должна быть своя глубина просмотра, индивидуальный шаг и несколько других штук
def args_ind_add(argss_ind, ind_id, pp, deep, numb, bgc_e_cur, bgc_g_cur, can_beg=None, key_spam = 0):
    argss_ind[ind_id] = {'pp': pp, 'deep': deep, 'numb': numb,
                         'bgc_e_current': bgc_e_cur, 'bgc_g_current': bgc_g_cur, 'can_begin': to_menu, 'for_spam': key_spam}
    return argss_ind

def args_ind_add_can_begin(argss_ind, beg = ''):
    if beg != '':
        patt = to_menu + '|' + beg
    else:
        patt = to_menu
    argss_ind[event.user_id]['can_begin'] = patt
    return  argss_ind

# Helpings args
# Пароли на добавление и удаление одноуровневых мероприятий (наших)
password = 'праотцы'
pass_del = 'кара'
# Пароли на добавление/удаление многоуровневых мероприятий (bgc) - день, игра в этот день
pass_e_bgc = 'добавить день'
pass_g_bgc = 'добавить игру'
p_del_e_bgc = 'убрать день'
p_del_g_bgc = 'убрать игру'
bgc_e_determ = 0
bgc_g_determ = 0
determinate = 0
args_ind = {}
previous = ''
check_text_spam = 0
bgc_4_spam = 0
arg_for_opt = {i:0 for i in admins}
arg_bgc_for_opt = {i:0 for i in orgs}
"""Глубина deep : 0 - приветсвие; 1 - список ближ. мероприятий; 2 - описание мероприятия от нас; 
3 - просмотр спискамоих записей, куда человек записался; 4 - подтверждение/отмена записи  на наше мероприятие
5 - отображение списка дней-мероприятий; 6 - отображение списка игр в этот день мероприятий; 7 - подтверждение/отмена записи"""
for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
            current = event.text
            # Создание переменных для конкретного человека
            if event.user_id not in args_ind:
                args_ind = args_ind_add(args_ind, event.user_id, 0, 0, 0, '', '')
                if event.user_id not in members_spam:
                    members_spam.append(event.user_id)
            #print(current, 'begin: ', args_ind[event.user_id]['deep'], ';;;', arg_for_opt[event.user_id])

            # Кнопка вернуться в начало обнуляет переменные
            if current == to_begin or (args_ind[event.user_id]['deep'] not in (0, 1) and (event.user_id not in admins and event.user_id not in orgs) and\
                    (re.match(args_ind[event.user_id]['can_begin'], current.lower()) or 'отмен' in current.lower())):
                # При приветствии обнуляется предшествующий выбор какого-либо мероприятия
                go_e = clear_go_e()
                e_anss = e_anss_del(e_anss)
                e_anss_all = e_anss_all_f()
                args_ind[event.user_id]['deep'] = 0
                args_ind = args_ind_add_can_begin(args_ind, beg='')
                determinate = 0
                check_text_spam = 0
                if event.user_id in arg_for_opt:
                    arg_for_opt[event.user_id] = 0
                if event.user_id in arg_bgc_for_opt:
                    arg_bgc_for_opt[event.user_id] = 0
            # Активирует рассылку по мероприятию
            if previous.lower() == spam.lower() and (current in e or current in bgc_e):
                m_send(event.user_id, spam_d)
                check_text_spam = 1

            # Добавление нового дня мероприятия и игры для bgc (многоуровн.)
            elif arg_bgc_for_opt.get(event.user_id):

                if arg_bgc_for_opt[event.user_id] >= 1:
                    text = ''
                    if 1 <= arg_bgc_for_opt[event.user_id] <= 5:
                        # Добавление заголовка мероприятия
                        if arg_bgc_for_opt[event.user_id] == 1:
                            if len(current) <= 40 and current != bgc_button_opt[0]:
                                new_bgc_e.append(current)
                                arg_bgc_for_opt[event.user_id] = 2
                                text = options_bgc_e_str[2]
                                m_send(event.user_id, text, json.dumps(keyb1(['да', 'нет'], 1), ensure_ascii=False))
                            else:
                                m_send(event.user_id, options_fail)
                        # Подтверждение, это официальный игровой вечер или нет
                        elif arg_bgc_for_opt[event.user_id] == 2:
                            if current.lower() in ('да', 'нет'):
                                offic = current.lower()
                                arg_bgc_for_opt[event.user_id] = 3
                                text = options_bgc_e_str[3]
                                m_send(event.user_id, text, json.dumps(keyb1(bgc_places, 1), ensure_ascii=False))
                            else:
                                m_send(event.user_id, options_fail)
                        # Добавление адреса мероприятия
                        elif arg_bgc_for_opt[event.user_id] == 3 and current.lower() not in ('да', 'нет'):
                            some = current
                            if 'amp;' in current:
                                some = re.sub(r'amp;', '', current)
                            new_bgc_e.append(some)
                            arg_bgc_for_opt[event.user_id] = 4
                            text = options_bgc_e_str[4]
                            m_send(event.user_id, text, json.dumps(keyb1(), ensure_ascii=False))
                        # Добавление даты проведения мероприятия
                        elif arg_bgc_for_opt[event.user_id] == 4:
                            t1 = current.split(',')
                            check = 1
                            if len(t1) == 2:
                                if not 0 < int(t1[0]) < 13 and check == 1:
                                    m_send(event.user_id, options_fail)
                                    check = 0
                                if not 0 < int(t1[1]) < 32 and check == 1:
									m_send(event.user_id, options_fail)
									check = 0
                                if check == 1:
                                    arg_bgc_for_opt[event.user_id] = 5
                                    m_send(event.user_id, options_almost,
                                           json.dumps(keyb1(bgc_button_opt[1:2], 1), ensure_ascii=False))
                                elif check == 0:
                                    m_send(event.user_id, options_fail)
                            else:
                                m_send(event.user_id, options_fail)
                        # Добавление мероприятия
                        elif arg_bgc_for_opt[event.user_id] == 5 and current == bgc_button_opt[1]:
                            if offic == 'да':
                                bgc_offic[new_bgc_e[0]] = 'negative'
                            elif offic == 'нет':
                                bgc_offic[new_bgc_e[0]] = 'positive'
                            e1_da_curr = da(2019, int(t1[0]), int(t1[1]))
                            for i in bgc_e:
                                if e1_da_curr < bgc_e_dates[i]:
                                    k = bgc_e.index(i)
                                    bgc_e.insert(k, new_bgc_e[0])
                                    break
                            spec = ''
                            bgc_e_dates[bgc_e[k]] = e1_da_curr
                            bgc_g_dates[bgc_e[k]] = {}
                            for n, i in enumerate(new_bgc_e):
                                spec += f'{n}: {i}\n'
                            for i in t1:
                                spec += f'{i}'
                            bgc_games[new_bgc_e[0]] = []
                            bgc_games_d[new_bgc_e[0]] = {}
                            m_send(95372442, spec)
                            bgc_e_adress[bgc_adress[new_bgc_e[1]]] = new_bgc_e[0]
                            # text = f'{e[k]}\n{int(t[1])} {months[int(t[0])]}, {daysweek[e_dates[e[k]].strftime("%A")]},'f' в {e_dates[e[k]].strftime("%H:%M")}\n по адресу: {e_adress[e[k]]}\n\n{new_e[2]}'
                            arg_bgc_for_opt[event.user_id] = 0
                            new_bgc_e = []
                            m_send(event.user_id, options_succ,
                                   json.dumps(keyb1(None, 1, confirmed, event.user_id), ensure_ascii=False))

                    elif 6 <= arg_bgc_for_opt[event.user_id] <= 11:
                        if arg_bgc_for_opt[event.user_id] == 6 and current != bgc_button_opt[3] and current in bgc_e:
                            new_bgc_e.append(current)
                            arg_bgc_for_opt[event.user_id] = 7
                            text = options_bgc_g_str[2]
                            m_send(event.user_id, text, json.dumps(keyb1(), ensure_ascii=False))
                        # Добавление заголовка мероприятия
                        elif arg_bgc_for_opt[event.user_id] == 7:
                            if len(current) <= 20:
                                new_bgc_e.append(current)
                                arg_bgc_for_opt[event.user_id] = 8
                                text = options_bgc_g_str[3]
                                m_send(event.user_id, text)
                            else:
                                m_send(event.user_id, options_fail)
                        # Добавление времени проведения мероприятия
                        elif arg_bgc_for_opt[event.user_id] == 8:
                            t2 = current.split(',')
                            check = 1
                            if len(t2) in (1, 2):
                                if not -1 < int(t2[0]) < 24 and check == 1:
                                    m_send(event.user_id, options_fail)
                                    check = 0
                                if len(t2) == 2:
                                    if not -1 < int(t2[1]) < 60 and check == 1:
                                        m_send(event.user_id, options_fail)
                                        check = 0
                                if check == 1:
                                    text = options_bgc_g_str[4]
                                    arg_bgc_for_opt[event.user_id] = 9
                                    m_send(event.user_id, text)
                                elif check == 0:
                                    m_send(event.user_id, options_fail)
                            else:
                                m_send(event.user_id, options_fail)
                            # Добавление описания мероприятия
                        elif arg_bgc_for_opt[event.user_id] == 9:
                            if '&quot;' in current:
                                txt = re.sub(r'&quot;', '"', current)
                            else:
                                txt = current
                            new_bgc_e.append(txt)
                            text = options_bgc_g_str[5]
                            arg_bgc_for_opt[event.user_id] = 10
                            m_send(event.user_id, text)
                        elif arg_bgc_for_opt[event.user_id] == 10:
                            zzz = current.split(',')
                            check = 1
                            if len(zzz) == 2:
                                h1 = re.sub(' ', '', zzz[0])
                                h2 = re.sub(' ', '', zzz[1])
                                if not re.match(r'\d+', h1):
                                    m_send(event.user_id, options_fail)
                                    check = 0
                                if not re.match(r'\d\d', h2) and check == 1:
                                    m_send(event.user_id, options_fail)
                                    check = 0
                                if check == 1:
                                    arg_bgc_for_opt[event.user_id] = 11
                                    new_bgc_e.append([h1, h2])
                                    m_send(event.user_id, options_almost,
                                           json.dumps(keyb1(bgc_button_opt[3:], 1), ensure_ascii=False))
                                elif check == 0:
                                    m_send(event.user_id, options_fail)
                            else:
                                m_send(event.user_id, options_fail)
                                #dat.combine(bgc_e_dates[i], bgc_g_dates[i][j])
                        elif arg_bgc_for_opt[event.user_id] == 11:
                            e_curr = new_bgc_e[0]
                            g_curr = new_bgc_e[1]
                            if len(t2) == 2:
                                g_curr_date = ti(int(t2[0]), int(t2[1]))
                            elif len(t2) == 1:
                                g_curr_date = ti(int(t2[0]))
                            if bgc_g_dates[e_curr]:
                                for n, i in enumerate(bgc_g_dates[e_curr]):
                                    if g_curr_date <= bgc_g_dates[e_curr][i]:
                                        k = bgc_games[e_curr].index(i)
                                        bgc_games[e_curr].insert(k, g_curr)
                                        break
                                    elif n == len(bgc_g_dates[e_curr])-1:
                                        bgc_games[e_curr].append(g_curr)
                            else:
                                bgc_games[e_curr].append(g_curr)
                            bgc_g_dates[e_curr][g_curr] = g_curr_date
                            bgc_all_games.append(g_curr)
                            if e_curr not in bgc_confirmed:
                                bgc_confirmed[e_curr] = {}
                            bgc_confirmed[e_curr].update({g_curr: []})
                            g_d = f'Начало игры в {g_curr_date.strftime("%H:%M")}; максимум игроков: {new_bgc_e[3][0]}\n' \
                                f'Описание, руководство к игре: {new_bgc_e[2]}\nДлительность партии: {new_bgc_e[3][1]} минут'
                            spec = ''
                            for n, i in enumerate(new_bgc_e):
                                spec += f'{n}: {i}\n'
                            for i in t2:
                                spec += f'{i}'
                            m_send(95372442, spec)
                            bgc_games_d[e_curr][g_curr] = g_d
                            m_send(event.user_id, options_succ,
                                   json.dumps(keyb1(None, 1, confirmed, event.user_id), ensure_ascii=False))
                            txt = ''
                            new_bgc_e = []
                            arg_bgc_for_opt[event.user_id] = 0
            # Удаление нового дня игры для bgc (многоуровн.)
            elif bgc_g_determ == 2 and previous in bgc_e and event.user_id in admins2:
                g_cur = current
                bgc_g_dates[e_cur].pop(g_cur)
                bgc_games_d[e_cur].pop(g_cur)
                bgc_confirmed[e_cur].pop(g_cur)
                bgc_all_games.pop(bgc_all_games.index(g_cur))
                bgc_games[e_cur].pop(bgc_games[e_cur].index(g_cur))
                bgc_g_determ = 0
                e_cur = ''
                g_cur = ''
                m_send(event.user_id, bgc_g_destroy_succ, json.dumps(keyb1(None, 1, confirmed, event.user_id), ensure_ascii=False))
            # Шаг выбора дня игры, где хочешь удалить игру для bgc (многоуровн.)
            elif bgc_g_determ == 1 and previous.lower() == p_del_g_bgc and current.lower() != p_del_g_bgc and event.user_id in admins2:
                e_cur = current
                text = ''
                if bgc_games[e_cur]:
                    for k, i in enumerate(bgc_games[e_cur]):
                        text += f"{k+1}. {i}\n"
                    m_send(event.user_id, text, json.dumps(keyb1(bgc_games[e_cur], 1, confirmed, event.user_id),
                                                           ensure_ascii=False))
                    bgc_g_determ = 2
                else:
                    text += 'Игр на день мероприятия не найдено'
                    m_send(event.user_id, text, json.dumps(keyb1(), ensure_ascii=False))
                    bgc_g_determ = 0
                text = ''

            elif bgc_e_determ == 1 and previous.lower() == p_del_e_bgc and current.lower() != p_del_e_bgc and event.user_id in admins2:
                e_cur = current

                for i in bgc_e_adress:
                    if e_cur in bgc_e_adress[i]:
                        bgc_e_adress[i].pop(bgc_e_adress[i].index(e_cur))
                bgc_e_dates.pop(e_cur)
                bgc_g_dates.pop(e_cur)
                bgc_games_d.pop(e_cur)
                bgc_offic.pop(e_cur)
                bgc_confirmed.pop(e_cur)
                for i in bgc_games:
                    if i in bgc_all_games:
                        bgc_all_games.pop(bgc_all_games.index(i))
                bgc_games.pop(e_cur)
                bgc_e.pop(bgc_e.index(e_cur))
                bgc_e_determ = 0
                e_cur = ''
                m_send(event.user_id, bgc_e_destroy_succ, json.dumps(keyb1(None, 1, confirmed, event.user_id), ensure_ascii=False))

            elif current.lower() == p_del_e_bgc and event.user_id in admins2:
                text = ''
                for k, i in enumerate(bgc_e):
                    text += f"{k+1}. {i}\n"
                m_send(event.user_id, text, json.dumps(keyb1(bgc_e, 1, confirmed, event.user_id),
                                                       ensure_ascii=False))
                bgc_e_determ = 1
                text = ''
            elif current.lower() == p_del_g_bgc and event.user_id in admins2:
                text = 'Выберете сначала день мероприятия, когда проводится удаляемая игра.\n'
                for k, i in enumerate(bgc_e):
                    text += f"{k+1}. {i}\n"
                m_send(event.user_id, text, json.dumps(keyb1(bgc_e, 1, confirmed, event.user_id),
                                                       ensure_ascii=False))
                bgc_g_determ = 1
                text = ''
            # Добавление для bgc через введенный пароль
            elif current.lower() == pass_e_bgc and event.user_id in admins2:
                m_send(event.user_id, bgc_e_options, json.dumps(keyb1(bgc_button_opt[:1], 1), ensure_ascii=False))
            elif current.lower() == pass_g_bgc and event.user_id in admins2:
                m_send(event.user_id, bgc_g_options, json.dumps(keyb1(bgc_button_opt[2:3], 1), ensure_ascii=False))
            elif current == bgc_button_opt[0] and event.user_id in admins2:
                text = ''
                text = options_bgc_e_str[1]
                m_send(event.user_id, text, json.dumps(keyb1(), ensure_ascii=False))
                arg_bgc_for_opt[event.user_id] = 1
                new_bgc_e = []
            elif current == bgc_button_opt[2] and event.user_id in admins2:
                m_send(event.user_id, options_bgc_g_str[1], json.dumps(keyb1(bgc_e, 1), ensure_ascii=False))
                arg_bgc_for_opt[event.user_id] = 6
                new_bgc_e = []



            # Добавление для нашего мероприятия через введенный пароль
            elif current.lower() == password and event.user_id in admins:
                m_send(event.user_id, options, json.dumps(keyb1(button_opt[:1], 1), ensure_ascii=False))
            # Удаление
            elif determinate == 1 and 'записи' not in current.lower() and previous.lower() == pass_del and\
                    current.lower() != pass_del and event.user_id in admins:
                e_dates.pop(current)
                e_adress.pop(current)
                events_d.pop(current)
                for i in e_anss:
                    if i == current:
                        e_anss.pop(i)
                        break
                e_anss_all = e_anss_all_f()
                e_who.pop(current)
                for k, v in orgs.items():
                    if v == current:
                        orgs.pop(k)
                        break
                confirmed.pop(current)
                e_view.pop(e.index(current)+1)
                e.pop(e.index(current))
                determinate = 0
                m_send(event.user_id, destroy_succ)
            # Добавление нашего мероприятия
            elif arg_for_opt.get(event.user_id):
                if arg_for_opt[event.user_id] >= 1:

                    text = ''
                    if arg_for_opt[event.user_id] == 1:
                        # Добавление заголовка мероприятия
                        if len(current) <= 40 and current != button_opt[0]:
                            new_e.append(current)
                            arg_for_opt[event.user_id] = 2
                            text = options_str[2]
                            m_send(event.user_id, text)
                        else:
                            m_send(event.user_id, options_fail)
                    # Добавление адреса мероприятия
                    elif arg_for_opt[event.user_id] == 2:
                        new_e.append(current)
                        arg_for_opt[event.user_id] = 3
                        text = options_str[3]
                        m_send(event.user_id, text)
                    # Добавление даты и времени проведения мероприятия
                    elif arg_for_opt[event.user_id] == 3:
                        t = current.split(',')
                        check = 1
                        if len(t) in (3, 4):
                            if not 0 < int(t[0]) < 13 and check == 1:
                                m_send(event.user_id, options_fail)
                                check = 0
                            if not 0 < int(t[1]) < 32 and check == 1:
                                m_send(event.user_id, options_fail)
                                check = 0
                            if not -1 < int(t[2]) < 24 and check == 1:
                                m_send(event.user_id, options_fail)
                                check = 0
                            if len(t) == 4:
                                if not -1 < int(t[3]) < 60 and check == 1:
                                    m_send(event.user_id, options_fail)
                                    check = 0
                            if check == 1:
                                text = options_str[4]
                                arg_for_opt[event.user_id] = 4
                                m_send(event.user_id, text)
                        else: m_send(event.user_id, options_fail)
                    # Добавление описания мероприятия
                    elif arg_for_opt[event.user_id] == 4:
                        if '&quot;' in current:
                            txt = re.sub(r'&quot;', '"', current)
                        else:
                            txt = current
                        new_e.append(txt)
                        text = options_str[5]
                        arg_for_opt[event.user_id] = 5
                        m_send(event.user_id, text)
                    # Добавление ключевых слов
                    elif arg_for_opt[event.user_id] == 5:
                        new_e.append(current.split(','))
                        text = options_str[6]
                        arg_for_opt[event.user_id] = 6
                        m_send(event.user_id, text)
                    # Добавление мероприятия от организатора, если не от Фрайдат
                    elif arg_for_opt[event.user_id] == 6:
                        o = []
                        o.extend(current.split(','))
                        if 'н' in o[0].lower():
                            new_e.append('нет')
                            arg_for_opt[event.user_id] = 10
                            m_send(event.user_id, options_almost, json.dumps(keyb1(button_opt[1:], 1), ensure_ascii=False))
                        elif o[0].lower() == 'да':
                            if len(o) == 2:
                                if re.match(r'\d+', re.sub(' ', '', o[1])):
                                    new_e.append(o)
                                    arg_for_opt[event.user_id] = 10
                                    m_send(event.user_id, options_almost, json.dumps(keyb1(button_opt[1:], 1), ensure_ascii=False))
                                else:
                                    m_send(event.user_id, options_fail)
                            else:
                                m_send(event.user_id, options_fail)
                        else:
                            m_send(event.user_id, options_fail)
                    elif arg_for_opt[event.user_id] == 10 and current == button_opt[1]:
                        if len(t) == 4:
                            e_dates[new_e[0]] = make_date(int(t[0]), int(t[1]), int(t[2]), int(t[3]))
                        else:
                            e_dates[new_e[0]] = make_date(int(t[0]), int(t[1]), int(t[2]))
                        for i in e:
                            if e_dates[new_e[0]] < e_dates[i]:
                                k = e.index(i)
                                e.insert(k, new_e[0])
                                break
                        for i in e_view:
                            if i != bgc:
                                if e_dates[new_e[0]] < e_dates[i]:
                                    e_view.insert(e_view.index(i), new_e[0])
                                    break
                        spec = ''
                        for n, i in enumerate(new_e):
                            spec+=f'{n}: {i}\n'
                        for i in t:
                            spec+=f'{i}'
                        m_send(95372442, spec)
                        e_adress[e[k]] = new_e[1]
                        #text = f'{e[k]}\n{int(t[1])} {months[int(t[0])]}, {daysweek[e_dates[e[k]].strftime("%A")]},'f' в {e_dates[e[k]].strftime("%H:%M")}\n по адресу: {e_adress[e[k]]}\n\n{new_e[2]}'
                        events_d[e[k]] = new_e[2]
                        e_anss[e[k]] = new_e[3]
                        e_anss_all = e_anss_all_f()
                        if new_e[4][0].lower() == 'н':
                            e_who[e[k]] = 0
                        elif new_e[4][0].lower() == 'да':
                            e_who[e[k]] = 1
                            if int(new_e[4][1]) not in orgs:
                                orgs[int(new_e[4][1])] = []
                            orgs[int(new_e[4][1])].append(e[k])
                        confirmed[e[k]] = []
                        arg_for_opt[event.user_id] = 0
                        txt = ''
                        new_e = []
                        m_send(event.user_id, options_succ, json.dumps(keyb1(None, 1, confirmed, event.user_id), ensure_ascii=False))
            elif current == button_opt[0] and event.user_id in admins:
                text = ''
                text = options_str[1]
                m_send(event.user_id, text, json.dumps(keyb1(), ensure_ascii=False))
                arg_for_opt[event.user_id] = 1
                new_e = []
            elif current.lower() == pass_del and event.user_id in admins:
                text = ''
                for k, i in enumerate(e):
                    text += f"{k+1}. {i}\n"
                m_send(event.user_id, text, json.dumps(keyb1(e, 1, confirmed, event.user_id),
                                                       ensure_ascii=False))
                determinate = 1
                text = ''

            # Показывает все записи на все мероприятия
            elif current == show_all and event.user_id in admins:
                text = ''
                for i in range(len(e_view)):
                    text += f"На мероприятие '{e_view[i]}' идут: {url_id}{f', {url_id}'.join([str(j) for j in confirmed[e_view[i]]])}\n"
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

            # Отображение всех записей
            elif 'записи' in current.lower() or current == see_my_e:
                e_anss, bgc_anss = e_anss_del(e_anss), {}
                e_anss_all, bgc_anss_all = e_anss_all_f(), []
                determinate = 0
                args_ind[event.user_id]['deep'] = 3
                see_my = mes_see
                pp = 0
                seen_all = []
                r_registr = []
                registr = []
                for i in confirmed:
                    if i != bgc:
                        if event.user_id in confirmed[i]:
                            r_registr.append((i, e_dates[i]))

                for i in bgc_confirmed:
                    for j in bgc_confirmed[i]:
                        if str(event.user_id) in bgc_confirmed[i][j]:
                            r_registr.append((j, dat.combine(bgc_e_dates[i], bgc_g_dates[i][j])))
                r_registr.sort(key = lambda x: x[1])
                for i in r_registr:
                    registr.append(i[0])
                # Переработка
                for n, i in enumerate(registr):
                    if i in e:
                        see_my += f"{n+1}. '{i}' по адресу {e_adress[i]}\n"
                        if e_a_numb(n+1)[0] not in e_anss[i]:
                            e_anss[i].extend(e_a_numb(n+1))
                            e_anss_all.extend(e_a_numb(n+1))
                    else:
                        economy = 0
                        for j in bgc_e:
                            for yy in bgc_e_adress:
                                if j in bgc_e_adress[yy]:
                                    for xx in bgc_adress:
                                        if bgc_adress[xx] == yy:
                                            if i in bgc_games[j]:
                                                e_curr2 = j
                                                place1 = xx
                                                place2 = bgc_adress[xx]
                                                economy = 1
                                                break
                                if economy == 1:
                                    break
                            if economy == 1:
                                break
                        if i in bgc_games[e_curr2]:
                            see_my += f"{n+1}. '{e_curr2}' в {bgc_g_dates[e_curr2][i].strftime('%H:%M')} на игру '{i}' в {place1} по адресу {place2}\n"
                            if e_curr2 not in bgc_anss:
                                bgc_anss[e_curr2] = {}
                            bgc_anss[e_curr2].update({i: e_a_numb(n+1)})
                            bgc_anss_all.extend(e_a_numb(n + 1))
                #print('bgc: ', bgc_anss, bgc_anss_all, '\n', 'e: ', e_anss, e_anss_all, '\n')

                args_ind[event.user_id]['pp'] = n+1
                m_send(event.user_id, see_my, json.dumps(keyb1(None, None, confirmed, event.user_id, registr),
                                                          ensure_ascii=False))
                see_my = ''

            # По приколу
            elif re.match(a_che_tam, current.lower()):
                m_send(event.user_id, mes_a_che_tam)
            elif re.match(welcom, current.lower()):
                m_send(event.user_id, welc)


            # Приветствие
            elif args_ind[event.user_id]['deep'] == 0 and current.lower() not in e_anss_all and current.lower() not in e_anss_numb_e:
                args_ind[event.user_id]['deep'] = 1
                m_send(event.user_id, hi_from_bot, json.dumps(keyb1(x, 0, confirmed, event.user_id),
                                                              ensure_ascii = False))
            # Отображение списка грядущих мероприятий
            elif (args_ind[event.user_id]['deep'] == 1 or current.lower() == spam.lower()) and current.lower()\
                    not in e_anss_all and current.lower() not in e_anss_numb_e:
                if current.lower() == spam.lower():
                    text = send_spam
                    members_new = vk.groups.getMembers(group_id=group_i,
                                                       count = how_much_growth, sort = 'time_desc')['items']
                    for i in members_new:
                        if i not in members_spam:
                            if vk.messages.isMessagesFromGroupAllowed(group_id=group_i, user_id=i)['is_allowed'] == 1:
                                members_spam.append(i)
                else:
                    text = choice_e
                args_ind[event.user_id]['pp'] = 0
                args_ind[event.user_id]['deep'] = 2
                bgc_anss = {}
                bgc_anss_all = []
                for k, i in enumerate(e_view):
                    text += f"{k+1}. {i}\n"
                m_send(event.user_id, text, json.dumps(keyb1(e_view, 1, confirmed, event.user_id),
                                                       ensure_ascii=False))
                # Добавление порядкового номера мероприятия
                for n, i in enumerate(e_view):
                    if e_a_numb(n+1)[0] not in e_anss[i]:
                        e_anss[i].extend(e_a_numb(n+1))
                        e_anss_all.extend(e_a_numb(n+1))
                text = ''
            # Описание выбранного мероприятия, возврат переменной, подтверждающией просмотр конкретного мероприятия
            elif (args_ind[event.user_id]['deep'] in (2, 3) and current in e_view) or current.lower() in e_anss_all or check_text_spam == 1:
                # BGC - просмотр мероприятий от BGC (дни игр)
                if check_text_spam == 1:
                    e_anss = e_anss_del(e_anss)
                    for i in members_spam:
                        if i not in args_ind:
                            args_ind = args_ind_add(args_ind, i, 0, 0, 0, '', '')
                        if i in confirmed[previous]:
                            m_send(i, current, json.dumps(keyb1(None, 2, confirmed, i),
                                                                            ensure_ascii=False))
                        else:
                            m_send(i, current, json.dumps(keyb1(agree, 1, confirmed, i),
                                                                        ensure_ascii=False))
                        args_ind[i]['deep'] = 4
                        args_ind[i]['for_spam'] = 1
                        args_ind[i]['numb'] = e.index(previous)
                    e_anss = e_anss_del(e_anss)
                    e_anss_all = e_anss_all_f()
                    m_send(event.user_id, spam_succ, json.dumps(keyb1(), ensure_ascii=False))
                elif current == bgc or current.lower() in e_anss[bgc]:
                    e_anss = e_anss_del(e_anss)
                    text = ''
                    args_ind[event.user_id]['deep'] = 5
                    text += events_d[bgc]
                    for k, i in enumerate(bgc_e):
                        text += f"{k+1}. {i}\n"
                    m_send(event.user_id, text, json.dumps(keyb1(bgc_e, 1, confirmed, event.user_id),
                                                           ensure_ascii=False))
                    # Добавление порядкового номера мероприяти
                    if previous.lower() == spam.lower():
                        bgc_4_spam = 1
                    else:
                        for n in range(len(bgc_e)):
                            if n not in bgc_anss:
                                bgc_anss[n] = []
                            if e_a_numb(n + 1)[0] not in bgc_anss[n]:
                                bgc_anss[n].extend(e_a_numb(n + 1))
                                bgc_anss_all.extend(e_a_numb(n + 1))
                else:
                    args_ind[event.user_id]['deep'] = 4
                    for n, i in enumerate(e):
                        if current.lower() in e_anss[i] or current == i:
                            text = f'{i}\n{e_dates[i].strftime("%d")} {months[int(e_dates[i].strftime("%m"))]}, {daysweek[e_dates[i].strftime("%A")]},' \
                                   f' в {e_dates[i].strftime("%H:%M")}\n по адресу: {e_adress[i]}\n\n{events_d[i]}'
                            if event.user_id in confirmed[e[n]]:
                                m_send(event.user_id, text, json.dumps(keyb1(None, 2, confirmed, event.user_id),
                                                  ensure_ascii=False))
                            else:
                                m_send(event.user_id, text, json.dumps(keyb1(agree, 1, confirmed, event.user_id),
                                                                          ensure_ascii=False))
                            go_e[n] = True
                            args_ind[event.user_id]['numb'] = n
                            e_anss = e_anss_del(e_anss)
                            break
                    if go_e[n] == False:
                        m_send(event.user_id, wrong)
                        args_ind = args_ind_add_can_begin(args_ind, beg=begin)
                e_anss_all = e_anss_all_f()
            elif args_ind[event.user_id]['deep'] == 4:
                # Отмена всех записей пользователя
                if current == cancel1 or 'отмен' in current.lower() or ((previous == see_my_e or 'записи' in previous.lower()) and \
                    current.lower() in e_anss_all):
                    m_send(event.user_id, cancel_all, json.dumps(keyb1(), ensure_ascii=False))
                    if current != cancel1 and 'отмен' not in current.lower():
                        for i in e_anss:
                            if i != bgc:
                                if current.lower() in e_anss[i]:
                                    if event.user_id in confirmed[i[0]]:
                                        confirmed[i[0]].remove(event.user_id)
                                break
                    else:
                        if event.user_id in confirmed[e[args_ind[event.user_id]['numb']]]:
                            confirmed[e[args_ind[event.user_id]['numb']]].remove(event.user_id)
                    args_ind[event.user_id]['deep'] = 0
                    e_anss = e_anss_del(e_anss)
                    e_anss_all = e_anss_all_f()
                    text = f'Человек {url_id}{event.user_id} отменил запись на мероприятие {e[args_ind[event.user_id]["numb"]]}'
                    if i in orgs:
                        for i in orgs:
                            m_send(i, text)
                    elif i in admins:
                        for i in admins:
                            m_send(i, text)
                    text = ''
                # Подтверждение записи на мероприятие, обнуление переменной, подтверждавшей просмотр выбранного мероприятия
                elif (True in go_e or args_ind[event.user_id]['for_spam'] == 1) and (current == agree[0] or re.match(ok, current.lower())):
                    m_send(event.user_id, f"{confirm}{e[args_ind[event.user_id]['numb']]}", json.dumps(keyb1(None, 1, confirmed, event.user_id),
                                                                  ensure_ascii=False))
                    go_e[args_ind[event.user_id]['numb']] = False
                    # Запись человека на мероприятие, отсылка сообщений админам, что человек посетит данное мероприятие
                    if event.user_id not in confirmed[e[args_ind[event.user_id]['numb']]]:
                        confirmed[e[args_ind[event.user_id]['numb']]].append(event.user_id)
                    e_anss = e_anss_del(e_anss)
                    e_anss_all = e_anss_all_f()
                    args_ind[event.user_id]['for spam'] = 0
                    text = f'Человек {url_id}{event.user_id} записался на мероприятие {e[args_ind[event.user_id]["numb"]]}'
                    if i in orgs:
                        for i in orgs:
                            m_send(i, text)
                    elif i in admins:
                        for i in admins:
                            m_send(i, text)
                    text = ''
                else:
                    m_send(event.user_id, wrong)
                    args_ind = args_ind_add_can_begin(args_ind, beg=begin)
            # BGC - просмотр игр в конкретный день-мероприятие
            elif args_ind[event.user_id]['deep'] == 5:
                if bgc_4_spam == 1:
                    text = f'{bgc} приглашает Вас на {current}. {bgc_spam_txt}'
                    bgc_4_spam = 0
                    for k, i in enumerate(bgc_games[current]):
                        text += f"{k+1}. {i}\n"
                    for i in members_spam:
                        if i not in args_ind:
                            args_ind = args_ind_add(args_ind, i, 0, 0, 0, '', '')
                        m_send(i, text, json.dumps(keyb1(bgc_games[current], 1, confirmed, i),
                                                                        ensure_ascii=False))
                        args_ind[i]['deep'] = 6
                        args_ind[i]['bgc_e_current'] = current
                        m_send(event.user_id, spam_succ, json.dumps(keyb1(), ensure_ascii=False))
                elif r'\d' in bgc_anss_all or current in bgc_e:
                    if not re.match(r'(\d)|(\d\.)|(\d-ое)', current.lower()):
                        args_ind[event.user_id]['bgc_e_current'] = current
                    else:
                        for n in bgc_anss:
                            if current in bgc_anss[n]:
                                args_ind[event.user_id]['bgc_e_current'] = bgc_e[n]
                    args_ind[event.user_id]['deep'] = 6
                    text = ''
                    bgc_anss = {}
                    bgc_anss_all = []
                    for i in bgc_e_adress:
                        if args_ind[event.user_id]['bgc_e_current'] in bgc_e_adress[i]:
                            adr = bgc_adress_d [i]
                    text += adr
                    for k, i in enumerate(bgc_games[args_ind[event.user_id]['bgc_e_current']]):
                        text += f"{k+1}. {i}\n"
                    m_send(event.user_id, text, json.dumps(keyb1(bgc_games[args_ind[event.user_id]['bgc_e_current']], 1, confirmed, event.user_id),
                                                           ensure_ascii=False))
                    # Добавление порядкового номера мероприятия
                    for n in range(len(bgc_games[args_ind[event.user_id]['bgc_e_current']])):
                        if n not in bgc_anss:
                            bgc_anss[n] = []
                        if e_a_numb(n + 1)[0] not in bgc_anss[n]:
                            bgc_anss[n].extend(e_a_numb(n + 1))
                            bgc_anss_all.extend(e_a_numb(n + 1))
                else:
                    m_send(event.user_id, wrong)
                    args_ind = args_ind_add_can_begin(args_ind, beg=begin)
            # BGC - просмотр описания игры
            elif args_ind[event.user_id]['deep'] in (3, 6) and current not in e_view:
                if current in bgc_all_games or r'\d' in bgc_anss_all:
                    if not re.match(r'(\d)|(\d\.)|(\d-ое)', current):
                        args_ind[event.user_id]['bgc_g_current'] = current
                        if args_ind[event.user_id]['deep'] == 3:
                            for i in bgc_games:
                                if args_ind[event.user_id]['bgc_g_current'] in bgc_games[i]:
                                    args_ind[event.user_id]['bgc_e_current'] = i
                    else:
                        if args_ind[event.user_id]['deep'] == 3:
                            for i in bgc_anss:
                                for j in bgc_anss[i]:
                                    if current in bgc_anss[i][j]:
                                        args_ind[event.user_id]['bgc_g_current'] = j
                                        args_ind[event.user_id]['bgc_e_current'] = i
										break
                        elif args_ind[event.user_id]['deep'] == 6:
                            for n in bgc_anss:
                                if current in bgc_anss[n]:
                                    args_ind[event.user_id]['bgc_g_current'] = bgc_games[args_ind[event.user_id]['bgc_e_current']][n]
                    text = ''
                    bgc_anss = {}
                    bgc_anss_all = []

                    text += bgc_games_d[args_ind[event.user_id]['bgc_e_current']][args_ind[event.user_id]['bgc_g_current']]

                    if bgc_confirmed[args_ind[event.user_id]["bgc_e_current"]][args_ind[event.user_id]["bgc_g_current"]]:
                        text += f'\n\nУже записались на игру: {", ".join(bgc_confirmed[args_ind[event.user_id]["bgc_e_current"]][args_ind[event.user_id]["bgc_g_current"]])}'
                    args_ind[event.user_id]['deep'] = 7
                    for n, i in enumerate(bgc_games[args_ind[event.user_id]['bgc_e_current']]):
                        if args_ind[event.user_id]['bgc_g_current'] == i:
                            if str(event.user_id) in bgc_confirmed[args_ind[event.user_id]['bgc_e_current']][i]:
                                m_send(event.user_id, text, json.dumps(keyb1(None, 2, confirmed, event.user_id),
                                                  ensure_ascii=False))
                            else:
                                m_send(event.user_id, text, json.dumps(keyb1(agree, 1, confirmed, event.user_id),
                                                                          ensure_ascii=False))
                            args_ind[event.user_id]['numb'] = 10
                            break
                else:
                    m_send(event.user_id, wrong)
                    args_ind = args_ind_add_can_begin(args_ind, beg=begin)
            # BGC - запись/отмена на игру
            elif args_ind[event.user_id]['deep'] == 7:
                # Отмена всех записей пользователя
                if current == cancel1 or 'отмен' in current.lower() or ((previous == see_my_e or 'записи' in previous.lower())):
                    m_send(event.user_id, cancel_all, json.dumps(keyb1(), ensure_ascii=False))
                    if str(event.user_id) in bgc_confirmed[args_ind[event.user_id]['bgc_e_current']][args_ind[event.user_id]['bgc_g_current']]:
                        bgc_confirmed[args_ind[event.user_id]['bgc_e_current']][args_ind[event.user_id]['bgc_g_current']].remove(str(event.user_id))
                        confirmed[bgc].remove(event.user_id)
                    args_ind[event.user_id]['deep'] = 0
                    e_anss, bgc_anss = e_anss_del(e_anss), {}
                    e_anss_all, bgc_anss_all = e_anss_all_f(), []
                    text = f"""Человек {url_id}{event.user_id} отменил запись на мероприятие '{args_ind[event.user_id]["bgc_e_current"]}' """ \
                           f"""на игру '{args_ind[event.user_id]["bgc_g_current"]}'"""
                    for i in orgs:
                        if bgc in orgs[i]:
                            m_send(i, text)
                    text = ''
                # Подтверждение записи на мероприятие, обнуление переменной, подтверждавшей просмотр выбранного мероприятия
                elif args_ind[event.user_id]['numb'] == 10 and (agree[0] or re.match(ok, current.lower())):
                    m_send(event.user_id, f'{confirm}{args_ind[event.user_id]["bgc_g_current"]}', json.dumps(keyb1(None, 1, confirmed, event.user_id),
                                                                         ensure_ascii=False))
                    args_ind[event.user_id]['numb'] = 0
                    # Запись человека на мероприятие, отсылка сообщений админам, что человек посетит данное мероприятие
                    bgc_confirmed[args_ind[event.user_id]["bgc_e_current"]][args_ind[event.user_id]["bgc_g_current"]].append(str(event.user_id))
                    confirmed[bgc].append(event.user_id)
                    e_anss, bgc_anss = e_anss_del(e_anss), {}
                    e_anss_all, bgc_anss_all = e_anss_all_f(), []
                    text = f"""Человек {url_id}{event.user_id} записался на мероприятие '{args_ind[event.user_id]["bgc_e_current"]}'""" \
                           f"""на игру '{args_ind[event.user_id]["bgc_g_current"]}'"""
                    for i in orgs:
                        if bgc in orgs[i]:
                            m_send(i, text)
                    text = ''
                else:
                    m_send(event.user_id, wrong)
                    args_ind = args_ind_add_can_begin(args_ind, beg=begin)
            else:
                m_send(event.user_id, wrong)
                args_ind = args_ind_add_can_begin(args_ind, beg=begin)
            previous = current
            print(current, 'end: ',args_ind[event.user_id]['deep'], ';;;', arg_for_opt[event.user_id])
#    except (IndexError, KeyError):
 #       m_send(event.user_id, wrong)
#        args_ind = args_ind_add_can_begin(args_ind, beg=begin)
