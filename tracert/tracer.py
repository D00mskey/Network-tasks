from urllib import request
from prettytable import PrettyTable
import subprocess
import re
import json


def trace_as(address, table):
    trace_process = subprocess.Popen(["tracert", address], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    number = 0
    reg = '\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'

    for raw_line in iter(trace_process.stdout.readline, ''):
        line = raw_line.decode('cp866')
        ip = re.findall(reg, line)

        if complete(line):
            print(table)
            return
        if invalid_input(line):
            print('invalid input')
            return
        if is_beginning(line):
            print(line)
            continue
        if timed_out(line):
            print('request timed out')
            continue
        if ip:
            number += 1
            print(f'{"".join(ip)}')
            info = get_ip_info(ip[0])
            if 'bogon' in info:
                table.add_row(get_bogon_args(number, info))
            else:
                table.add_row(get_args(number, info))


def get_ip_info(ip):
    return json.loads(request.urlopen('https://ipinfo.io/' + ip + '/json').read())


def get_args(count, info):
    try:
        as_number = info['org'].split()[0][2::]
        provider = " ".join(info['org'].split()[1::])
    except KeyError:
        as_number, provider = '*', '*'
    return [f"{count}.", info['ip'], info['country'], as_number, provider]


def get_bogon_args(count, info):
    return [f"{count}.", info['ip'], '*', '*', '*']


def complete(text_data):
    return 'Trace complete' in text_data or 'Трассировка завершена' in text_data


def timed_out(text_data):
    return 'Request timed out' in text_data \
           or 'Превышен интервал ожидания' in text_data


def is_beginning(text_data):
    return 'Tracing route' in text_data \
           or 'Трассировка маршрута' in text_data


def invalid_input(text_data):
    return 'Unable to resolve' in text_data \
           or 'Не удается разрешить' in text_data


def generate_table():
    table = PrettyTable()
    table.field_names = ["number", "ip", "country", "AS number", "provider"]
    return table


if __name__ == '__main__':
    address = input('Enter domain or ip: ')
    table = generate_table()
    trace_as(address, table)
