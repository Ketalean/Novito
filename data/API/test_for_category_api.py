from requests import get, post
from pprint import pprint

pprint(get('http://localhost:8080/api/category').json())

pprint(get('http://localhost:8080/api/category/2').json())

#  работы с таким id не существует
print(get('http://localhost:8080/api/category/20234234903490').json())

#  вместо номера посылаем строку
print(get('http://localhost:8080/api/category/BlaBlaBlaBleBleBleBluBluBlu').json())

#  пустой запрос, ничего отправляем
print(post('http://localhost:8080/api/category', json={}).json())

#  неполный запрос, не хватает полей
print(post('http://localhost:8080/api/category',
           json={'job': 'РАБОТААА'}).json())

print(post('http://localhost:8080/api/category',
           json={'name': 'Еда'}).json())

#  проверяем, добавилась ли работа
pprint(get('http://localhost:8080/api/category').json())
