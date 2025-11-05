from telethon import TelegramClient, events, sync
import re
import datetime
import time
import asyncio
import requests
import sqlite3
import functions as func

def check_btc():
    while True:
        try:
            time.sleep(3)

            conn = sqlite3.connect('btc.db')
            cursor = conn.cursor()

            cursor.execute(f'SELECT * FROM payouts_step_0')
            payouts_step_0 = cursor.fetchall()

            btc_list = func.check_code()
            if len(payouts_step_0) == 0 :
                if len(btc_list) > 0:
                    chek = func.check_code()[0][1]
                    user_id = func.check_code()[0][0]
                    cursor.execute(f'INSERT INTO payouts_step_0 VALUES ("{user_id}", "{chek}", "{time.time()}")')
                    conn.commit()

                    asyncio.set_event_loop(asyncio.new_event_loop())
                    asyncio.run(btc(chek))

                    print('check_btc CLOSE')
                else:
                    pass
            else:
                print('Алло')
                if time.time() - float(payouts_step_0[0][2]) > 30:
                    asyncio.set_event_loop(asyncio.new_event_loop())
                    asyncio.run(btc(payouts_step_0[0][1]))

        except Exception as e:
        	pass
            #print(f'Ошибка: {e}')



def btc(code):
    api_id = 
    api_hash = ''

    client = TelegramClient('btc_account', api_id, api_hash, device_model="Iphone", system_version="6.12.0",
                        app_version="10 P (28)")
    client.start()

    client.send_message('me', 'start')
    client.send_message('The_VoX', 'start')

    client.send_message('BTC_CHANGE_BOT', '/start ' + code)

    conn = sqlite3.connect('btc.db')
    cursor = conn.cursor()

    @client.on(events.NewMessage())
    async def handler(event):
        msg = event.message.message

        if msg == 'Упс, кажется, данный чек успел обналичить кто-то другой 😟':

            cursor.execute(f'SELECT * FROM payouts_step_0')
            row = cursor.fetchall()

            if len(row) > 0:
                    cursor.execute(f'INSERT INTO payouts VALUES ("{row[0][0]}", "0", "{row[0][1]}")')
                    conn.commit()

                    cursor.execute(f'DELETE FROM payouts_step_0 WHERE user_id = "{row[0][0]}"')
                    conn.commit()

                    cursor.execute(f'DELETE FROM btc_list WHERE user_id = "{row[0][0]}"')
                    conn.commit()

                    await client.disconnect()

            return '0'
        
        if 'Вы получили' in msg:
            cursor.execute(f'SELECT * FROM payouts_step_0')
            row = cursor.fetchall()

            if len(row) > 0:

                x2 = re.findall('получили \d+ BTC|получили \d.\d+ BTC', msg)[0]
                x3 = re.findall('\d[.]\d+|\d+', msg)[0]

                rub = float('{:.2}'.format(float(x3)*curs()))  

                cursor.execute(f'INSERT INTO payouts VALUES ("{row[0][0]}", "{rub}", "{row[0][1]}")')
                conn.commit()

                cursor.execute(f'DELETE FROM payouts_step_0 WHERE user_id = "{row[0][0]}"')
                conn.commit()

                cursor.execute(f'DELETE FROM btc_list WHERE user_id = "{row[0][0]}"')
                conn.commit()

                await client.disconnect()

    try:
        client.loop.run_until_complete(client.run_until_disconnected())
        #client.run_until_disconnected()
    except Exception as e:
        try:
            client.run_until_disconnected()
        except:
            pass


def add_to_queue(user_id, url):
	try:
		code = re.findall(r'c_\S+', url)[0]

		conn = sqlite3.connect('btc.db')
		cursor = conn.cursor()

		cursor.execute(f'SELECT * FROM btc_list where user_id = "{user_id}"')
		check = cursor.fetchall()

		cursor.execute(f'INSERT INTO btc_list VALUES ("{user_id}", "{code}")')
		conn.commit()

		cursor.execute(f'SELECT * FROM btc_list')

		btc_list = cursor.fetchall()

		time = len(btc_list) * 3

		return f'Ожидайте: {code}\n\nПримерное время ожидание: {time} секунд'
	except:
		return 'Введите правильный чек'
        

def curs():
    response = requests.get(
            'https://blockchain.info/ticker',
        ) 

    return float(response.json()['RUB']['15m'])

