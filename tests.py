import requests
import json

url = "http://0.0.0.0:8080/"
#url = "http://127.0.0.1:5000/"

def check_post(query):
    headers = {'Content-type': 'application/json; charset=utf-8', 'Accept': 'text/plain'}
    response = requests.post(url=url + "imports", data=json.dumps(query), headers=headers)
    print(response.text)
    try:
        return_import_id = json.loads(response.text)["data"]["import_id"]
    except:
        return_import_id = None

    return return_import_id, response.status_code, response.reason

def check_get_citizens(import_id):
    headers = {'Content-type': 'application/json; charset=utf-8', 'Accept': 'text/plain'}
    response = requests.get(url=url + "imports/{0}/citizens".format(import_id), headers=headers)
    print(response.text)
    return response.status_code, response.reason

def check_get_birthdays(import_id):
    headers = {'Content-type': 'application/json; charset=utf-8', 'Accept': 'text/plain'}
    response = requests.get(url=url + "imports/{0}/citizens/birthdays".format(import_id), headers=headers)
    print(response.text)
    return response.status_code, response.reason

def check_patch(import_id, citizen_id, query):
    headers = {'Content-type': 'application/json; charset=utf-8', 'Accept': 'text/plain'}
    response = requests.patch(url=url + "imports/{0}/citizens/{1}".format(import_id, citizen_id),  data=json.dumps(query), headers=headers)
    print(response.text)
    return response.status_code, response.reason

if __name__ == '__main__':
    # Проверка POST
    query = \
        {"citizens": [
            {
                "citizen_id": 1,
                "town": "Москва",
                "street": "Денискино",
                "building": "1к1стр3",
                "apartment": 7,
                "name": "Любимова Александра Валерьевна",
                "birth_date": "12.03.1984",
                "gender": "female",
                "relatives": [2, 3, 5]
            },
            {
                "citizen_id": 2,
                "town": "Москва",
                "street": "Малаховка",
                "building": "56к3",
                "apartment": 5,
                "name": "Иванов Сергей Иванович",
                "birth_date": "01.06.1978",
                "gender": "male",
                "relatives": [1, 4]
            },
            {
                "citizen_id": 3,
                "town": "Самара",
                "street": "Кириловка",
                "building": "34к2",
                "apartment": 12,
                "name": "Шипнов Максим Вадимович",
                "birth_date": "28.10.1997",
                "gender": "male",
                "relatives": [1]
            },
            {
                "citizen_id": 4,
                "town": "Казань",
                "street": "Иосифа Бродского",
                "building": "4",
                "apartment": 99,
                "name": "Романова Мария Леонидовна",
                "birth_date": "15.03.2015",
                "gender": "female",
                "relatives": [2, 5]
            },
            {
                "citizen_id": 5,
                "town": "Казань",
                "street": "Марсианина",
                "building": "3к4",
                "apartment": 2,
                "name": "Якубовна Лидия Михайловна",
                "birth_date": "22.01.1990",
                "gender": "female",
                "relatives": [1, 4]
            },
            {
                "citizen_id": 6,
                "town": "Сочи",
                "street": "улица Гагарина",
                "building": "55к1",
                "apartment": 6,
                "name": "Шамкина Лилия Эдуардовна",
                "birth_date": "25.06.1996",
                "gender": "female",
                "relatives": []
            }
        ]
        }
    return_import_id, status_code, reason = check_post(query)
    print("POST: ", status_code, reason)

    query2 = \
        {"citizens": [
            {
                "citizen_id": 1,
                "town": "Москва",
                "street": "Денискино",
                "building": "1к1стр3",
                "apartment": 7,
                "name": "Любимова Александра Валерьевна",
                "birth_date": "12.03.1984",
                "gender": "female",
                "relatives": [2]
            },
            {
                "citizen_id": 2,
                "town": "Москва",
                "street": "Малаховка",
                "building": "56к3",
                "apartment": 5,
                "name": "Иванов Сергей Иванович",
                "birth_date": "01.06.1978",
                "gender": "male",
                "relatives": [3]
            },
            {
                "citizen_id": 3,
                "town": "Самара",
                "street": "Кириловка",
                "building": "34к2",
                "apartment": 12,
                "name": "Шипнов Максим Вадимович",
                "birth_date": "28.10.1997",
                "gender": "male",
                "relatives": []
            }
        ]
        }
    # Выдаст Bad request, т.к. неверные двухносторонние отношения
    _, status_code, reason = check_post(query2)
    print("POST: ", status_code, reason)

    query3 = \
        {"citizens": [
            {
                "citizen_id": 1,
                "town": "Москва",
                "street": "Денискино",
                "building": "1к1стр3",
                "apartment": 7,
                "name": "Любимова Александра Валерьевна",
                "birth_date": "42.01.1984",
                "gender": "female",
                "relatives": [2]
            },
            {
                "citizen_id": 2,
                "town": "Москва",
                "street": "Малаховка",
                "building": "56к3",
                "apartment": 5,
                "name": "Иванов Сергей Иванович",
                "birth_date": "01.06.1978",
                "gender": "male",
                "relatives": [3]
            }
        ]
        }

    # Выдаст Bad request, потому что 42 января у citizen_id = 1
    _, status_code, reason = check_post(query3)
    print("POST: ", status_code, reason)

    query4 = \
        {"citizens": [
            {
                "citizen_id": 1,
                "town": "Москва",
                "street": "Денискино",
                "building": "1к1стр3",
                "apartment": 7,
                "name": "Любимова Александра Валерьевна",
                "birth_date": "08.10.1984",
                "gender": "female",
                "relatives": [2]
            },
            {
                "citizen_id": 2,
                "town": "Москва",
                "street": "Малаховка",
                "building": "56к3",
                "name": "Иванов Сергей Иванович",
                "birth_date": "01.06.1978",
                "gender": "male",
                "relatives": [3]
            }
        ]
        }

    # Выдаст Bad request, потому что нет данных об apartment у citizen_id = 2
    _, status_code, reason = check_post(query4)
    print("POST: ", status_code, reason)

    # Проверка GET citizens
    # import_id = int(input("Введите import_id: "))  # Введите import_id, который создался методом POST
    import_id = return_import_id
    status_code, reason = check_get_citizens(import_id)
    print("GET: ", status_code, reason)

    # Проверка GET birthdays
    # import_id = int(input("Введите import_id: "))  # Введите import_id, который создался методом POST
    status_code, reason = check_get_birthdays(import_id)
    print("GET: ", status_code, reason)

    # Проверка PATCH
    # import_id = int(input("Введите import_id: "))  # Введите import_id, который создался методом POST
    # citizen_id = int(input("Введите citizen_id: "))  # Введите citizen_id, который создался методом POST
    query5 = {
        "town": "Анапа",
        "street": "Льва Петровича",
        "relatives": []
        }
    import_id = return_import_id
    citizen_id = 1
    status_code, reason = check_patch(import_id, citizen_id, query5)
    print("PATCH: ", status_code, reason)







