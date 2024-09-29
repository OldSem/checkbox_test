import datetime
import os
import textwrap

from jinja2 import Template, Environment


def center(text, max_length, filler=' '):
    indent = round((max_length - text.__len__()) / 2)
    return f'{indent * filler}{text}{(max_length - indent - text.__len__()) * filler}'


def expand(start, end, max_length, filler=' '):
    return f'{start}{filler * (max_length - start.__len__() - end.__len__())}{end}'


def format_number(value):
    return '{:,}'.format(value).replace(',', ' ')


def create_check(max_length, company='ФОП',

                 ):

    output = ''


def wrap_expand(value, amount=0.00, width=10):
    amount = format_number(amount)
    text = f'{value} {amount}'
    text = textwrap.wrap(text, width)

    text[-1] = expand(text[-1][:text[-1].__len__() - amount.__len__()], amount, width)

    return '\n'.join(text)


def render(filename: str, context: dict = {}, width=10) -> str:
    print(os.getcwd())
    env = Environment()
    env.filters['wrap_expand'] = wrap_expand
    env.filters['strftime'] = datetime.datetime.strftime
    with open(filename) as file:
        content = file.read()

    template = env.from_string(content)
    return template.render(context)
