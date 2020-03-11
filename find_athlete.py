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


class Athelete(Base):
    __tablename__ = 'athelete'

    id = sa.Column(sa.INTEGER, primary_key=True)

    age = sa.Column(sa.INTEGER)
    birthdate = sa.Column(sa.TEXT)
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


def find(name, session):
    """
    Производит поиск пользователя в таблице user по заданному имени name
    """
    # нахдим все записи в таблице User, у которых поле User.first_name совпадает с парарметром name
    query = session.query(Athelete).filter(Athelete.id == name)
    # подсчитываем количество таких записей в таблице с помощью метода .count()
    users_cnt = query.count()
    # составляем список идентификаторов всех найденных пользователей
    user_ids = {}
    for row in query:
        user_ids = {'id':row.id, 'birthdate':row.birthdate, 'height':row.height }
        break
    # возвращаем кортеж количество_найденных_пользователей, список_идентификаторов, словарь_времени_активности
    return (users_cnt, user_ids)


def print_users_list(cnt, user, session):

    if user:
        print("Найдено пользователей: ", cnt)
        print("Идентификатор пользвоателя")

        print(" id {} - дата рождения {} - рост {}".format(user.get('id'), user.get('birthdate'), user.get('height')))

        greater = session.query(Athelete).filter(Athelete.birthdate > user.get('birthdate')).\
        order_by(Athelete.birthdate.asc()).limit(1)

        for row in greater.all():
            print('Нашли ближайшего по дате рождения id {} - дата рождения {} - рост {}'.format(row.id, row.birthdate, row.height))

        greater = session.query(Athelete).filter(Athelete.height > user.get('height')).\
        order_by(Athelete.height.asc()).limit(1)

        for row in greater.all():
            print('Нашли ближайшего по росту id {} - дата рождения {} - рост {}'.format(row.id, row.birthdate, row.height))

        

    else:
        print("Пользователей с таким именем нет.")


def main():
    """
    Осуществляет взаимодействие с пользователем, обрабатывает пользовательский ввод
    """
    session = connect_db()
    # просим пользователя выбрать режим

    # выбран режим поиска, запускаем его
    name = input("Введи id атлета для поиска: ")
    # вызываем функцию поиска по имени
    users_cnt, user_ids = find(name, session)
    # вызываем функцию печати на экран результатов поиска
    print_users_list(users_cnt, user_ids, session)



if __name__ == "__main__":
    main()