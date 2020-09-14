"""
Utility scripts for data extraction and dataset generation
"""

from typing import Tuple

def day2month(day: int) -> Tuple[int, int]:
    days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    m, d = 0, 0

    while day > 0:
        d = day
        day -= days[m]
        m += 1
    
    return (m, d)

def getClaps(claps: str) -> int:
    pass