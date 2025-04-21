from requests import get, post
from pprint import pprint

pprint(get('http://localhost:8080/api/markets').json())

pprint(get('http://localhost:8080/api/markets/2').json())

#  работы с таким id не существует
print(get('http://localhost:8080/api/markets/20234234903490').json())

#  вместо номера посылаем строку
print(get('http://localhost:8080/api/markets/BlaBlaBlaBleBleBleBluBluBlu').json())

#  пустой запрос, ничего отправляем
print(post('http://localhost:8080/api/markets', json={}).json())

#  неполный запрос, не хватает полей
print(post('http://localhost:8080/api/markets',
           json={'title': 'РАБОТААА'}).json())

print(post('http://localhost:8080/api/markets',
           json={'title': 'Борщ',
                 'description': 'Вкусный, питательный, красный.',
                 'seller': 3,
                 'price': 985,
                 'contacts': '+7 (912) 354-39-11',
                 'address': 'г. Москва',
                 'stock': True,
                 'img': '/static/images/borsh.jpg',
                 'category': 'Еда'}).json())

#  проверяем, добавилась ли работа
pprint(get('http://localhost:8080/api/markets').json())
