from telebot import types
import functions as func 
import random
import datetime
import config
import sqlite3


my_games_txt = """
Мои игры: {}

Выигрыш: {} RUB
Проигрыш: {} RUB
Профит: {} RUB

Данные приведены за все время
"""

raiting_txt = """
📊 ТОП 3 игроков:

🥇 1 место - {} RUB
🥈 2 место - {} RUB
🥉 3 место - {} RUB

"""

dice_game_info_txt = """
🎲 Кости #{}
💰 Ставка: {} RUB

🧑🏻‍💻 Создал: @{}
"""


dice_game_result_txt = """
🎲 Кости #{}
💰 Банк: {} RUB

👤 @{} and @{}

👆Ваш результат: {}
👇Результат соперника: {}

{}
"""


game_result_txt = """
{} #{}
💰 Банк: {} RUB

ℹ️ Результаты:
❕ {} | {}
❕ {} | {}

Итог: {}
"""

class Game():

    def __init__(self, code):
        conn = sqlite3.connect('db.db')
        cursor = conn.cursor()

        cursor.execute(f'SELECT * FROM dice WHERE id_game = "{code}"')
        info = cursor.fetchall()

        if len(info) == 0:
            self.status = False
        else:
            self.status = True

            self.id_game = info[0][0]
            self.user_id = info[0][1]
            self.bet = float(info[0][2])

    def del_game(self):
        conn = sqlite3.connect('db.db')
        cursor = conn.cursor()

        cursor.execute(f'DELETE FROM dice WHERE id_game = "{self.id_game}"')
        conn.commit()


def dice_menu():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton(text='Создать игру', callback_data='create_dice'),
        types.InlineKeyboardButton(text='Обновить', callback_data='reload_dice'),
    )

    markup = get_games_menu(markup)

    markup.add(
        types.InlineKeyboardButton(text='📝Мои игры', callback_data='my_games:dice')
    )

    return markup


def get_games_menu(markup):
    conn = sqlite3.connect('db.db')
    cursor = conn.cursor()

    cursor.execute(f'SELECT * FROM dice')
    games = cursor.fetchall()

    for i in games:
        markup.add(types.InlineKeyboardButton(text=f'🎲Игра #{i[0]} | {i[2]} RUB', callback_data=f'dice_game:{i[0]}'))

    return markup

def cancel_dice():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton(text='❌Отменить', callback_data='cancel_dice')
    )

    return markup

def check_dice():
    conn = sqlite3.connect('db.db')
    cursor = conn.cursor()

    cursor.execute('SELECT COUNT(*) from dice')
    check = cursor.fetchone()[0]

    return check

def create_game(id_games, user_id, bet):
    conn = sqlite3.connect('db.db')
    cursor = conn.cursor()

    cursor.execute(f'INSERT INTO dice VALUES("{id_games}", "{user_id}", "{bet}")')
    conn.commit()


def my_games_dice(user_id):
    conn = sqlite3.connect('db.db')
    cursor = conn.cursor()

    cursor.execute(f'SELECT * FROM dice_logs WHERE user_id = "{user_id}"')
    games = cursor.fetchall()

    amount_games = len(games)

    win_money = 0
    lose_money = 0

    if len(games) < int(100):
        amount = len(games)
    else:
        amount = int(100)


    for i in range(amount):
        if games[i][2] == 'win':
            win_money += float(games[i][3])


        elif games[i][2] == 'lose':
            lose_money += float(games[i][3])


    profit_money = win_money - lose_money
    profit_money = '{:.2f}'.format(profit_money)

    win_money = '{:.2f}'.format(win_money)
    lose_money = '{:.2f}'.format(lose_money)

    msg = my_games_txt.format(
        amount_games,
        win_money,
        lose_money,
        profit_money,
    )

    return msg


def dice_game(code):
    game = Game(code)

    if game.status == False:
        return False
    else:
        msg = dice_game_info_txt.format(
            game.id_game,
            game.bet,
            func.profile(game.user_id)[5]
        )

        msg += f'🧑🏻‍💻 2Player: Ожидание...'

        markup = types.InlineKeyboardMarkup(row_width=1)


        markup.add(
            types.InlineKeyboardButton(text='🎲 Кости', callback_data=f'start_game_dice:{game.id_game}'),
            types.InlineKeyboardButton(text='🔙 Назад', callback_data=f'back_dice')
        )
        return msg, markup


def start_game_dice(user_id, game, value_dice1, value_dice2):
    user = func.profile(user_id)

    func.update_balances(user_id, game.bet)

    value_dice1 = value_dice1
    value_dice2 = value_dice2

    win_money = ((game.bet * 2) / 100) * (100 - float(config.com_percent))
    profit_money = ((game.bet * 2) / 100) * float(config.com_percent)

    if value_dice1[0] > value_dice2[0]:
        func.update_balances(user_id, win_money)

        dice_write_game_log(game.id_game, user_id, 'win', win_money)
        dice_write_game_log(game.id_game, game.user_id, 'lose', win_money)

        status1 = '✅Поздравляем с победой!'
        status2 = '🔴Вы проиграли!'

    elif value_dice1[0] < value_dice2[0]:
        func.update_balance(game.user_id, win_money)

        dice_write_game_log(game.id_game, game.user_id, 'win', win_money)
        dice_write_game_log(game.id_game, user_id, 'lose', win_money)

        status1 = '🔴Вы проиграли!'
        status2 = '✅Поздравляем с победой!'


    try:
        conn = sqlite3.connect('db.db')
        cursor = conn.cursor()

        msg = f"{user_id} | {game.user_id}"

        cursor.execute(f'INSERT INTO dice_logs VALUES ("{msg}", "{profit_money}", "{datetime.datetime.now()}")')
        conn.commit()
    except:
        pass

    msg1 = dice_game_result_txt.format(
        game.id_game,
        win_money,
        func.profile(user_id)[5],
        func.profile(game.user_id)[5],
        value_dice1[0],
        value_dice2[0],
        status1
    )

    msg2 = dice_game_result_txt.format(
        game.id_game,
        win_money,
        func.profile(user_id)[5],
        func.profile(game.user_id)[5],
        value_dice2[0],
        value_dice1[0],
        status2
    )

    return [user_id, game.user_id], [msg1, msg2], [value_dice2[1], value_dice1[1]]

def dice_write_game_log(id, user_id, status, bet):
    conn = sqlite3.connect('db.db')
    cursor = conn.cursor()

    cursor.execute(f'INSERT INTO dice_logs VALUES("{id}", "{user_id}", "{status}", "{bet}", "{datetime.datetime.now()}")')
    conn.commit()

    cursor.execute(f'SELECT * FROM dice_stats WHERE user_id = "{user_id}"')
    stats = cursor.fetchall()

    if len(stats) == 0:
        cursor.execute(f'INSERT INTO dice_stats VALUES("{user_id}", "0")')
        conn.commit()
    else:
        cursor.execute(f'UPDATE dice_stats SET money = {float(stats[0][1]) + float(bet)} WHERE user_id = "{user_id}"')
        conn.commit()

def roll_dice(bot, user_id):
    value = bot.send_dice(user_id)

    return int(value.dice.value), value.message_id



def start_roll(bot, game, chat_id):
    bot.send_message(chat_id=chat_id, text='❕ Бросаем кости...')

    value_dice1 = roll_dice(bot, chat_id)
    value_dice2 =  roll_dice(bot, game.user_id)

    while value_dice1[0] == value_dice2[0]:
        bot.send_message(chat_id=chat_id, text='❕ Противник бросает кости...')
        bot.forward_message(chat_id=chat_id, from_chat_id=game.user_id, message_id=value_dice2[1])
        bot.send_message(chat_id=chat_id, text='🔵Ничья!!!\n\nПеребрасываем кости...')

        bot.send_message(chat_id=game.user_id, text='❕ Противник бросает кости...')
        bot.forward_message(chat_id=game.user_id, from_chat_id=chat_id, message_id=value_dice1[1])
        bot.send_message(chat_id=game.user_id, text='🔵Ничья!!!\n\nПеребрасываем кости...')
        value_dice1 = roll_dice(bot, chat_id)
        value_dice2 =  roll_dice(bot, game.user_id)

        #return start_roll(bot, game, chat_id)
    #else:
    return value_dice1, value_dice2

def main_start(game, bot, chat_id):
    game.del_game()

    value_dice1, value_dice2 = start_roll(bot, game, chat_id)

    info = start_game_dice(chat_id, game, value_dice1, value_dice2)

    from_chat_id = lambda i: 1 if i == 0 else 0 if i == 1 else 100

    for i in range(2):
        bot.send_message(chat_id=info[0][i], text='❕ Противник бросает кости...')
        bot.forward_message(chat_id=info[0][i], from_chat_id=info[0][from_chat_id(i)], message_id=info[2][i])
        bot.send_message(chat_id=info[0][i], text=info[1][i])


def my_games_cancel(user_id):
    conn = sqlite3.connect('db.db')
    cursor = conn.cursor()

    cursor.execute(f'SELECT * FROM dice WHERE user_id = "{user_id}"')
    games = cursor.fetchall()
    if len(games) > 0:
        markup = types.InlineKeyboardMarkup(row_width=1)
        for i in games:
            markup.add(
                types.InlineKeyboardButton(text=f'🌀 Game_{i[0]} | {i[2]} ₽',callback_data=f'games_user:{i[0]}'))

        return markup
    else:
        return False

def get_info_games(code):
    conn = sqlite3.connect('db.db')
    cursor = conn.cursor()
    
    cursor.execute(f'SELECT * FROM dice WHERE id_game = "{code}"')
    info = cursor.fetchone()

    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add( 
        types.InlineKeyboardButton(text=f'Удалить', callback_data=f'game_del:{code}'),
        types.InlineKeyboardButton(text=f'Выйти', callback_data=f'back_dice'),
    )

    msg = f"""
Игра: #Game_{info[0]}

🆔 ID: {info[1]}

🕹 Link: @{func.profile((info[1]))[5]}

💰 SUM: {info[2]} RUB

    """

    return msg, markup

def delete_game(id_game):
    conn = sqlite3.connect('db.db')
    cursor = conn.cursor()

    cursor.execute(f'SELECT * FROM dice WHERE id_game = "{id_game}"')
    info = cursor.fetchone()

    func.update_balance(info[1], info[2])

    cursor.execute(f'DELETE FROM dice WHERE id_game = "{id_game}"')
    conn.commit()