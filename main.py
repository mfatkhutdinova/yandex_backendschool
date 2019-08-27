#coding=utf-8
import sqlite3
import random
from datetime import datetime
from flask import Flask, request, json, Response

TABLENAME = "citizens"

class Connection:
    def __init__(self):
        self.conn = sqlite3.connect("citizens.db", check_same_thread=False)
        #self.drop_table()
        self.create_to_do_table()

    def drop_table(self):
        """ Удаляем базу данных.
        
        :return: None
        """
        query = """DROP TABLE IF EXISTS {0} """.format(TABLENAME)
        self.conn.execute(query)

    def create_to_do_table(self):
        """ Создаем базу данных.
        
        :return: None
        """
        query = """
        CREATE TABLE IF NOT EXISTS {0}
        (
          import_id INTEGER,
          citizen_id INTEGER,
          town TEXT,
          street TEXT,
          building TEXT,
          apartment INTEGER,
          name TEXT,
          birth_date TEXT,
          gender TEXT,
          relatives TEXT
        );
        """.format(TABLENAME)
        self.conn.execute(query)

    def add_value(self, query):
        """ Запрос в базу данных для добавления значений.
        
        :param query: 
        :return: 
        """

        self.conn.execute(query)
        self.conn.commit()

    def select_citizens(self, import_id):
        """ Функция возвращает данные о жителях import_id
        
        :param import_id: import_id
        :return: данные о жителях import_id
        """

        self.cur = self.conn.cursor()
        query = """SELECT * FROM {0} WHERE import_id='{1}'""".format(TABLENAME, import_id)
        self.cur.execute(query)

        rows = self.cur.fetchall()

        return rows

    def select_import_id_citizens(self, import_id, citizen_id):
        """ Функция возвращает данные о жителе citizen_id из import_id
        
        :param import_id: import_id
        :param citizen_id: id жителя
        :return: данные о жителе citizen_id
        """

        self.cur = self.conn.cursor()
        query = """SELECT * FROM {0} WHERE import_id='{1}' AND citizen_id='{2}' """.format(TABLENAME, import_id, citizen_id)
        self.cur.execute(query)

        rows = self.cur.fetchall()

        return rows

    def modify_citizens(self, query, import_id, citizen_id):
        """ Функция изменяет для citizen_id и возвращает актуальные данные 
        
        :param query: запрос
        :param import_id: import_id
        :param citizen_id: id жителя
        :return: данные о жителе 
        """

        self.conn.execute(query)
        self.conn.commit()

        rows = self.select_import_id_citizens(import_id, citizen_id)
        return rows

    def change_relatives(self, import_id, citizen_id, value):
        """ Измеяняет родственные связи с двух сторон.
        
        :param import_id: import_id
        :param citizen_id: id жителя
        :param value: родственные связи
        :return: None
        """

        for val in value:
            self.cur = self.conn.cursor()
            query = """SELECT relatives FROM {0} WHERE import_id='{1}' AND citizen_id='{2}' """.format(TABLENAME, import_id, val)
            self.cur.execute(query)

            return_relatives = [item[0] for item in self.cur.fetchall()]
            try:
                value_ = return_relatives[0][1:len(return_relatives[0]) - 1]
                list_relatives = [int(i.strip()) for i in value_.split(',')]
            except:
                list_relatives = []

            list_relatives.append(citizen_id)
            list_relatives_ = list(set(list_relatives))
            query_for_update = """ UPDATE {0} SET relatives = '{1}' WHERE import_id = '{2}' AND citizen_id = '{3}' """.format(TABLENAME, list_relatives_, import_id, val)
            self.conn.execute(query_for_update)
            self.conn.commit()

    def delete_relatives(self, import_id, citizen_id):
        """ Удаляет родственные связи для citizen_id.
        
        :param import_id: import_id
        :param citizen_id: id жителя
        :return: None
        """

        self.cur = self.conn.cursor()
        query = """SELECT relatives FROM {0} WHERE import_id='{1}' AND citizen_id='{2}' """.format(TABLENAME, import_id, citizen_id)
        self.cur.execute(query)

        return_relatives = [item[0] for item in self.cur.fetchall()]
        try:
            value_ = return_relatives[0][1:len(return_relatives[0]) - 1]
            list_relatives = [int(i.strip()) for i in value_.split(',')]
        except:
            list_relatives = []

        for rel in list_relatives:
            query_for_rel = """SELECT relatives FROM {0} WHERE import_id='{1}' AND citizen_id='{2}' """.format(
                TABLENAME, import_id, rel)
            self.cur.execute(query_for_rel)
            return_relatives_rel = [item[0] for item in self.cur.fetchall()]

            try:
                value_rel = return_relatives_rel[0][1:len(return_relatives_rel[0]) - 1]
                list_relatives_rel = [int(i.strip()) for i in value_rel.split(',')]
            except:
                list_relatives_rel = []

            list_relatives_rel.remove(citizen_id)
            query_for_update = """ UPDATE {0} SET relatives = '{1}' WHERE import_id = '{2}' AND citizen_id = '{3}' """.format(
                TABLENAME, list_relatives_rel, import_id, rel)
            self.conn.execute(query_for_update)
            self.conn.commit()

connection_class = Connection()
app = Flask(__name__)

@app.route("/imports", methods=["POST"])
def post():
    """ Функция позволяет добавлять данные в базу данных.
    
    :return: код успеха
    """
    data = request.json
    if not data:
        return "400: Bad request", 400

    import_id = random.randint(0, 10000)

    quote = {
        "data": {
            "import_id": import_id
        }
    }

    check_relatives_dict = {}
    enum = 0
    query = """ INSERT INTO {0}(import_id, citizen_id, town, street, building, apartment, name, birth_date, gender, relatives) VALUES """.format(TABLENAME)
    for citizen_list in data.values():
        for citizen in citizen_list:
            check_relatives_dict[citizen["citizen_id"]] = citizen["relatives"]

            # Возвращаем Bad request, если нет недостаюших данных
            if len(citizen) < 9:
                return "400: Bad request", 400

            # Возвращаем Bad request, если дата некорректная
            try:
                date_object = datetime.strptime(citizen["birth_date"], "%d.%m.%Y").date()
                if date_object >= datetime.now().date():
                    return "400: Bad request", 400
            except:
                return "400: Bad request", 400

            if citizen["citizen_id"] < 0 or citizen["apartment"] < 0:
                return "400: Bad request", 400

            query += """('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', '{8}', '{9}')""".format(import_id, citizen["citizen_id"],
                                                                                                       citizen["town"], citizen["street"],
                                                                                                       citizen["building"], citizen["apartment"],
                                                                                                       citizen["name"], citizen["birth_date"],
                                                                                                       citizen["gender"], citizen["relatives"])
            # Собираем все данные, которые нужно заменить в один запрос
            if enum < len(citizen_list) - 1:
                query += """, """

            enum += 1

    # Проверка корректных двухсторонних отношений
    for key, value in check_relatives_dict.items():
        for val in value:
            try:
                if key not in check_relatives_dict[val]:
                    return "400: Bad request", 400
            except:
                return "400: Bad request", 400


    # Записываем в базу, если все корректно
    connection_class.add_value(query)

    json_string = json.dumps(quote, ensure_ascii=False)
    response = Response(json_string, content_type="application/json; charset=utf-8")
    return response, 201

@app.route("/imports/<int:import_id>/citizens", methods=["GET"])
def get_citizens(import_id):
    """ Возвращает список всех жителей для указанного набора данных.
    
    :param import_id: import_id
    :return: данные о жителях 
    """
    # Делаем запрос в базу для получения данных о жителях с указанным import_id
    rows = connection_class.select_citizens(import_id)

    if not rows:
        return "400: Bad request", 400

    quote = {"data" : []}
    for row in rows:
        # Конвертируем relatives в тип list
        try:
            value_ = row[9][1:len(row[9]) - 1]
            list_relatives = [int(i.strip()) for i in value_.split(",")]
        except:
            list_relatives = []

        data = {"citizen_id": row[1],
                "town": row[2],
                "street": row[3],
                "building": row[4],
                "apartment": row[5],
                "name": row[6],
                "birth_date": row[7],
                "gender": row[8],
                "relatives": list_relatives}

        quote["data"].append(data)
    json_string = json.dumps(quote, ensure_ascii=False)
    response = Response(json_string, content_type="application/json; charset=utf-8")
    return response, 200

@app.route("/imports/<int:import_id>/citizens/birthdays", methods=["GET"])
def get_birthdays(import_id):
    """ Возвращает жителей и количество подарков, которые они будут покупать своим 
    ближайшим родственникам (1-го порядка), сгруппированных по месяцам из
    указанного набора данных.
    
    :param import_id: import_id
    :return: данные о подарках 
    """
    rows = connection_class.select_citizens(import_id)

    # Если введенного import_id нет в базе, возвращаем Bad request
    if not rows:
        return "400: Bad request", 400

    quote = {"data": {}}
    data = {}

    # Для всех месяцев присваиваем пустой list, чтобы в дальнейшем было легко добавлять
    for num in range(1, 13):
        data[str(num)] = []

    # Для каждого citizen_id ищем relatives
    for row in rows:
        birthdays = row[7][3:5].lstrip("0")
        relatives = row[9]
        try:
            relatives_ = relatives[1:len(relatives) - 1].split(",")
        except:
            relatives_ = []

        # Для каждого relatives присваиваем количество подарков, которые relatives должны подарить citizen_id
        for rel in relatives_:
            if not rel:
                continue
            if data[birthdays]:
                for birth in data[birthdays]:
                    Flaq_citizen = False
                    if birth["citizen_id"] == int(rel.strip()):
                        birth["presents"] += 1
                        Flaq_citizen = True
                        break
                if not Flaq_citizen:
                    data[birthdays].append({"citizen_id": int(rel.strip()), "presents": 1})
            else:
                data[birthdays].append({"citizen_id": int(rel.strip()), "presents": 1})

    quote["data"] = data
    json_string = json.dumps(quote, ensure_ascii=False)
    response = Response(json_string, content_type="application/json; charset=utf-8")
    return response, 200

@app.route("/imports/<int:import_id>/citizens/<int:citizen_id>", methods=["PATCH"])
def patch_citizen(import_id, citizen_id):
    """ Функция изменяет информацию о жителе в указанном наборе данных.
    
    :param import_id: import_id
    :param citizen_id: id жителя
    :return: код запроса (успех/неуспех)
    """
    rows = connection_class.select_import_id_citizens(import_id, citizen_id)

    # Если введенного import_id и citizen_id нет в базе, возвращаем Bad request
    if not rows:
        return "400: Bad request", 400

    data = request.json

    enum = 0
    query = """ UPDATE {0} SET """.format(TABLENAME)

    for key, value in data.items():

        if key == "apartment" and value < 0:
            return "400: Bad request", 400

        query += """{0} = '{1}'""".format(key, value)

        # Собираем все данные, которые нужно заменить в один запрос
        if enum < len(data)-1:
            query += """, """
        elif enum == len(data)-1:
            query += """WHERE import_id = '{1}' AND citizen_id = '{3}' """.format('import_id', import_id, 'citizen_id', citizen_id)
        enum += 1

        # Если есть изменения в поле relatives
        if key == "relatives":
            # Если есть значения в поле relatives, то для этого relatives добавляем citizen_id
            if value:
                connection_class.change_relatives(import_id, citizen_id, value)
            # Если значений в поле relatives отсутствует, то идем в базу и находим прежние relatives и для этих
            # relatives удаляем citizen_id
            else:
                connection_class.delete_relatives(import_id, citizen_id)

    # Изменяем данные
    rows = connection_class.modify_citizens(query, import_id, citizen_id)

    if not rows:
        return "400: Bad request", 400

    quote = {"data": []}
    for row in rows:
        # Конвертируем relatives в тип list
        try:
            value_ = row[9][1:len(row[9]) - 1]
            list_relatives = [int(i.strip()) for i in value_.split(",")]
        except:
            list_relatives = []

        data = {"citizen_id": row[1],
                "town": row[2],
                "street": row[3],
                "building": row[4],
                "apartment": row[5],
                "name": row[6],
                "birth_date": row[7],
                "gender": row[8],
                "relatives": list_relatives
                }
        quote["data"].append(data)
    json_string = json.dumps(quote, ensure_ascii=False)
    response = Response(json_string, content_type="application/json; charset=utf-8")
    return response, 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port='8080', debug=True)
    #app.run(host='127.0.0.1', port=5000, debug=True)


