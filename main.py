import numpy as np
import pandas as pd
from graphviz import Digraph

# Параметры процесса
params = {
    "ad_budget": 10000,  # Рекламный бюджет
    "ad_conversion_rate": 0.3,  # Конверсия из рекламы в игру
    "game_retention_rate": 0.7,  # Удержание в игре
    "hate_spread_factor": 13,  # Количество людей, которых охватывает хейтер
    "positive_spread_factor": 2,  # Количество людей, которых охватывает довольный пользователь
    "hater_conversion_rate": 0.28,  # Процент хейтеров
    "task_completion_rate": [0.4, 0.1, 0.1, 0.1],  # Удержание в кругах лояльности
    "server_cost_per_user": 0.1,  # Стоимость сервера на пользователя
    "ad_cost_increase_factor": 1.1,  # Увеличение стоимости рекламы из-за хейта
}

# Симуляция процесса
def simulate_flow(params, num_users):
    results = {
        "initial_users": num_users,
        "active_users": 0,
        "haters": 0,
        "positive_users": 0,
        "total_cost": 0,
        "ad_cost": 0,
    }

    # Переходы по рекламе
    ad_cost = params["ad_budget"]
    num_users_from_ads = int(params["ad_conversion_rate"] * num_users)
    results["ad_cost"] = ad_cost

    # Удержание в игре
    active_users = int(params["game_retention_rate"] * num_users_from_ads)

    # Круги лояльности
    for rate in params["task_completion_rate"]:
        active_users = int(active_users * rate)
        results["active_users"] += active_users

    # Хейтеры и довольные пользователи
    haters = int(results["active_users"] * params["hater_conversion_rate"])
    positive_users = results["active_users"] - haters

    # Расчёт стоимости
    hate_cost_increase = haters * params["hate_spread_factor"] * params["ad_cost_increase_factor"]
    total_server_cost = results["active_users"] * params["server_cost_per_user"]

    results["haters"] = haters
    results["positive_users"] = positive_users
    results["total_cost"] = ad_cost + total_server_cost + hate_cost_increase

    return results

# Визуализация блок-схемы
def draw_flowchart(params, num_users):
    graph = Digraph(format="png")
    graph.attr(rankdir="LR")

    # Узлы
    graph.node("A", "Закуп рекламы\n{} пользователей".format(num_users))
    graph.node("B", "Переходы по рекламе\n{}%".format(int(params["ad_conversion_rate"] * 100)))
    graph.node("C", "Игра\n{}% удержание".format(int(params["game_retention_rate"] * 100)))
    graph.node("D", "Круги лояльности\n{}\n{}\n{}\n{}".format(*params["task_completion_rate"]))
    graph.node("E", "Хейтеры\n{}%".format(int(params["hater_conversion_rate"] * 100)))
    graph.node("F", "Довольные пользователи")
    graph.node("G", "Серверные затраты\n{} руб./пользователь".format(params["server_cost_per_user"]))

    # Рёбра
    graph.edge("A", "B", label="Рекламные переходы")
    graph.edge("B", "C", label="В игру")
    graph.edge("C", "D", label="Удержание")
    graph.edge("D", "E", label="28% хейтеров")
    graph.edge("D", "F", label="Довольные пользователи")
    graph.edge("D", "G", label="Оплата серверов")

    # Сохранение схемы
    graph.render("flowchart")
    return "Блок-схема сохранена как flowchart.png"

# Запуск симуляции
initial_users = 1000
simulation_result = simulate_flow(params, initial_users)

# Вывод результатов
print(pd.DataFrame([simulation_result]))

# Рисуем блок-схему
flowchart_path = draw_flowchart(params, initial_users)
print(flowchart_path)
