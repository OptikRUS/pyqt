import asyncio
from asyncio.subprocess import PIPE
import locale
import platform
from ipaddress import ip_address, IPv4Address

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
