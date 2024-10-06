
pre_buy_demo_alert = '''\
Так как сейчас я запущен в тестовом режиме, для оплаты нужно использовать карточку с номером 1111 1111 1111 1026
Счёт для оплаты:
'''
tm_title = 'Премиум подписка на бота'

tm_description = '''\
Премиум подписка предоставляет дополнительные возможности для вас
'''

successful_payment = '''
Ура! Платеж на сумму `{total_amount} {currency}` совершен успешно! Приятного пользования
'''


MESSAGES = {
    'pre_buy_demo_alert': pre_buy_demo_alert,
    'tm_title': tm_title,
    'tm_description': tm_description,
    'successful_payment': successful_payment,
}