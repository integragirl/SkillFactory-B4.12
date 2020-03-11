#!/usr/bin/python
# -*- coding: utf-8 -*-

import uuid
import datetime

# импортируем библиотеку sqlalchemy и некоторые функции из нее 
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# константа, указывающая способ соединения с базой данных
DB_PATH = "sqlite:///sochi_athletes.sqlite3"

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = sa.Column(sa.INTEGER, primary_key=True, index=True, unique=True, autoincrement=True)
    first_name = sa.Column(sa.TEXT)
    last_name = sa.Column(sa.TEXT)
    email = sa.Column(sa.TEXT)
    gender = sa.Column(sa.TEXT)
    birthdate = sa.Column(sa.DATETIME)
    height = sa.Column(sa.FLOAT)


class Athelete(Base):
    __tablename__ = 'athelete'

    id = sa.Column(sa.INTEGER, primary_key=True)

    age = sa.Column(sa.INTEGER)
    birthdate = sa.Column(sa.DATETIME)
    gender = sa.Column(sa.TEXT)
    height = sa.Column(sa.FLOAT)
    name = sa.Column(sa.TEXT)
    weight = sa.Column(sa.INTEGER)
    gold_medals = sa.Column(sa.INTEGER)
    silver_medals = sa.Column(sa.INTEGER)
    bronze_medals = sa.Column(sa.INTEGER)
    total_medals = sa.Column(sa.INTEGER)
    sport = sa.Column(sa.TEXT)
    country = sa.Column(sa.TEXT)


def connect_db():
    """
    Устанавливает соединение к базе данных, создает таблицы, если их еще нет и возвращает объект сессии 
    """
    # создаем соединение к базе данных
    engine = sa.create_engine(DB_PATH)
    # создаем описанные таблицы
    Base.metadata.create_all(engine)
    # создаем фабрику сессию
    session = sessionmaker(engine)
    # возвращаем сессию
    return session()


def request_data():
    """
    Запрашивает у пользователя данные и добавляет их в список users
    """
    # выводим приветствие
    print("Привет! Я запишу твои данные!")
    # запрашиваем у пользователя данные
    first_name = str(input("Введи своё имя: "))
    last_name = str(input("А теперь фамилию: "))
    email = str(input("Мне еще понадобится адрес твоей электронной почты: "))
    gender = str(input('Пол Female or Male'))
    birthdate = str(input('Дата рождения в формате год-месяц-день'))
    birthdate = datetime.datetime.strptime(birthdate, '%Y-%m-%d')
    height = float(input('Рост'))
    # создаем нового пользователя
    user = User(
        first_name=first_name,
        last_name=last_name,
        email=email,
        gender=gender,
        birthdate=birthdate,
        height=height
    )
    # возвращаем созданного пользователя
    return user


def find(name, session):
    """
    Производит поиск пользователя в таблице user по заданному имени name
    """
    # нахдим все записи в таблице User, у которых поле User.first_name совпадает с парарметром name
    query = session.query(User).filter(User.first_name == name)
    # подсчитываем количество таких записей в таблице с помощью метода .count()
    users_cnt = query.count()
    # составляем список идентификаторов всех найденных пользователей
    user_ids = [user.id for user in query.all()]
    # возвращаем кортеж количество_найденных_пользователей, список_идентификаторов, словарь_времени_активности
    return (users_cnt, user_ids)


def print_users_list(cnt, user_ids):
    """
    Выводит на экран количество найденных пользователей, их идентификатор и время последней активности.
    Если передан пустой список идентификаторов, выводит сообщение о том, что пользователей не найдено.
    """
    # проверяем на пустоту список идентификаторов
    if user_ids:
        # если список не пуст, распечатываем количество найденных пользователей
        print("Найдено пользователей: ", cnt)
        # легенду будущей таблицы
        print("Идентификатор пользвоателя")
        # проходимся по каждому идентификатору
        for user_id in user_ids:
            # выводим на экран идентификатор - время_последней_активности
            print("{}".format(user_id))
    else:
        # если список оказался пустым, выводим сообщение об этом
        print("Пользователей с таким именем нет.")


def main():
    """
    Осуществляет взаимодействие с пользователем, обрабатывает пользовательский ввод
    """
    session = connect_db()
    # просим пользователя выбрать режим
    mode = input("Выбери режим.\n1 - найти пользователя по имени\n2 - ввести данные нового пользователя\n")
    # проверяем режим
    if mode == "1" or mode==1:
        # выбран режим поиска, запускаем его
        name = input("Введи имя пользователя для поиска: ")
        # вызываем функцию поиска по имени
        users_cnt, user_ids = find(name, session)
        # вызываем функцию печати на экран результатов поиска
        print_users_list(users_cnt, user_ids)
    elif mode == "2" or mode==2:
        # запрашиваем данные пользоватлея
        user = request_data()
        # добавляем нового пользователя в сессию
        session.add(user)
        # сохраняем все изменения, накопленные в сессии
        session.commit()
        print("Спасибо, данные сохранены!")
    else:
        print("Некорректный режим:(")


if __name__ == "__main__":
    main()