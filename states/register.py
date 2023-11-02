from aiogram.dispatcher.filters.state import State, StatesGroup


class Client(StatesGroup):
    name = State()
    phone = State()
    is_true = State()


class Taxi(StatesGroup):
    name = State()
    phone = State()
    is_true = State()


class Profile(StatesGroup):
    update = State()
    delete = State()


class TaxiAtDe(StatesGroup):
    st = State()


class TaxiAtUp(StatesGroup):
    st = State()


class Yunalish(StatesGroup):
    where = State()
    to_where = State()


class Travel(StatesGroup):
    where = State()
    to_where = State()
    person = State()
    note = State()
    location = State()
    is_true = State()
    completed = State()
