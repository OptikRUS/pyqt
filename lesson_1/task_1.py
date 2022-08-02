"""
Написать функцию host_ping(), в которой с помощью утилиты ping будет проверяться доступность сетевых узлов.
Аргументом функции является список, в котором каждый сетевой узел должен быть представлен именем хоста или ip-адресом.
В функции необходимо перебирать ip-адреса и проверять их доступность с выводом соответствующего сообщения
(«Узел доступен», «Узел недоступен»). При этом ip-адрес сетевого узла должен создаваться с помощью функции ip_address().
"""


import asyncio
from asyncio.subprocess import PIPE
import locale
import platform
from ipaddress import ip_address, IPv4Address
from pprint import pprint

ENCODING = locale.getpreferredencoding()


async def ping_ip(ip_addr: str) -> tuple[str, IPv4Address]:
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    cmd = f'ping {param} 5 {ip_addr}'
    proc = await asyncio.create_subprocess_shell(cmd=cmd, stdout=PIPE, stderr=PIPE)

    stdout, stderr = await proc.communicate()
    ip = ip_address(stdout.split()[2][1:-2].decode(ENCODING))
    if proc.returncode == 0:
        return "Узел доступен", ip
    return "Узел недоступен", ip


async def host_ping(ip_list: list[str]) -> tuple:
    results = []
    for ip in ip_list:
        results.append(ping_ip(ip))
    return await asyncio.gather(*results)


pprint(asyncio.run(host_ping(['192.168.0.1', 'yandex.ru', 'google.com', 'vk.com'])))
