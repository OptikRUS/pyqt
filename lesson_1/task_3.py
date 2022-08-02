from ipaddress import ip_address
import asyncio
from tabulate import tabulate
from task_2 import ping_ip


async def host_range_ping_tab(ip_addr: str, count: int) -> str:
    results = []
    for i in range(count):
        results.append(ping_ip(ip_address(ip_addr[:-1] + '0') + i))
    result = await asyncio.gather(*results)
    return tabulate(result, headers=('Доступность', 'IP-адрес'), tablefmt="grid")
