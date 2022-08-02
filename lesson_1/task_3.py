import asyncio
from asyncio.subprocess import PIPE
import locale
import platform
from ipaddress import ip_address
from tabulate import tabulate

ENCODING = locale.getpreferredencoding()


async def host_ping_range(ip_addr: str, count: int) -> str:
    if count < 257:
        param = '-n' if platform.system().lower() == 'windows' else '-c'
        cmd = f'ping {param} 5 {ip_addr}'
        proc = await asyncio.create_subprocess_shell(cmd=cmd, stdout=PIPE, stderr=PIPE)
        stdout, stderr = await proc.communicate()

        results = []

        for i in range(count):
            if proc.returncode:
                availability = '-'
            else:
                availability = '+'
            result = availability, str(ip_address(stdout.decode(ENCODING).split()[2][1:-3] + '0') + i)
            results.append(result)
        return tabulate(results, headers=('Доступность', 'IP-адрес'), tablefmt="grid", stralign="center")

    return 'Значение count не более 256'
