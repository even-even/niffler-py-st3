import allure

""" Обертки для человекочитаемых степов в тестах """
Given = allure.step  # предусловия
Step = allure.step   # шаги
Check = allure.step  # проверки
After = allure.step  # действия после окончания теста (обычно деактивация сущностей)
