from requests import get, post
from pprint import pprint

pprint(get('http://localhost:8080/api/users').json())

pprint(get('http://localhost:8080/api/users/2').json())

#  работы с таким id не существует
print(get('http://localhost:8080/api/users/20234234903490').json())

#  вместо номера посылаем строку
print(get('http://localhost:8080/api/users/BlaBlaBlaBleBleBleBluBluBlu').json())

#  пустой запрос, ничего отправляем
print(post('http://localhost:8080/api/users', json={}).json())

#  неполный запрос, не хватает полей
print(post('http://localhost:8080/api/users',
           json={'job': 'РАБОТААА'}).json())

print(post('http://localhost:8080/api/users',
           json={'username': 'MIH',
                 'phone': '+7 (987) 654-32-10',
                 'password': '123',
                 'address': 'г. Москва'}).json())

#  проверяем, добавилась ли работа
pprint(get('http://localhost:8080/api/users').json())
