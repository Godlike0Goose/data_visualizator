"""Пакет GUI для приложения визуализации данных.

Этот модуль делает доступной функцию `start` из `main_window` на уровне пакета,
чтобы упростить запуск приложения.
"""

from .main_window import start
from ._base import BaseWidget
