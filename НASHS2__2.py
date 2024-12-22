import random
import numpy as np
import pandas as pd
from hashlib import sha3_224
from scipy.stats import t, sem
import matplotlib.pyplot as plt
from tabulate import tabulate

# Хеш-функція
def get_hash(message):
    return sha3_224(message.encode()).hexdigest()

# Функція генерації змінених повідомлень
def generate_char(base_message):
    len_char = len(base_message)
    char = [chr(i) for i in range(32, 127)]
    base_message = list(base_message)
    base_message[random.randint(0, len_char - 1)] = random.choice(char)
    return "".join(base_message)


def attack_analysis(base_message, iterations):
    # Збирання кількості ітерацій для кожного повідомлення
    iteration_counts = []

    #for msg in messages
    #   count, _ = attack_function(msg, 1000)
    messages = []
    for i in range(iterations):
        count, msg = example_attack(base_message, 1000000)  # Отримуємо кількість ітерацій
        iteration_counts.append(count)  # Додаємо тільки кількість ітерацій
        messages.append(msg)

    # Перевірка, чи є достатня кількість даних для статистики
    if len(iteration_counts) < 2:
        print("Недостатня кількість даних для розрахунку статистики.")
        return  # Завершити функцію, якщо недостатньо даних

    # Таблиця результатів
    results_table = pd.DataFrame({
        "Повідомлення": messages,
        "Кількість ітерацій": iteration_counts
    })

    # Вивід з використанням tabulate
    print("\nРезультати аналізу:")
    print(tabulate(results_table, headers='keys', tablefmt='grid', showindex=False))

    # Розрахунок статистики
    mean_val = np.mean(iteration_counts)
    variance_val = np.var(iteration_counts)
    conf_interval = t.interval(
        confidence=0.95,
        df=len(iteration_counts) - 1,
        loc=mean_val,
        scale=sem(iteration_counts)
    )

    results = f"""
    Результати аналізу:
    ------------------------------------
    Показник                 | Значення
    ------------------------------------
    Середня кількість ітерацій | {mean_val}
    Дисперсія                 | {variance_val}
    Довірчий інтервал (95%)   | {conf_interval}
    ------------------------------------
    """
    print(results)

    # Побудова гістограми
    plt.figure(figsize=(10, 6))
    plt.hist(
        iteration_counts, bins=15, alpha=0.8, color="#6A5ACD", 
        edgecolor="#4B0082", linewidth=1.2
    )
    # Налаштування стилю графіка
    plt.xlabel("Кількість ітерацій", fontsize=12, color="#2E8B57")
    plt.ylabel("Частота", fontsize=12, color="#2E8B57")
    plt.xticks(fontsize=10, color="#696969")
    plt.yticks(fontsize=10, color="#696969")
    plt.legend(fontsize=10, loc="best")
    plt.grid(axis="y", linestyle=":", alpha=0.6)
    plt.tight_layout()
    plt.show()


# Реалізація атаки
def example_attack(base_message, max_iterations):
    i = 0
    base_hash = get_hash(base_message)[-8:]
    mangled_message = generate_char(base_message)
    while i < max_iterations:
        new_hash = get_hash(mangled_message)[-8:]
        if new_hash == base_hash:
            print("FOUND")
            return i, mangled_message
        mangled_message = generate_char(mangled_message)
        i += 1
    return i, None  # Якщо колізія не знайдена


# Основний код
if __name__ == "__main__":
    base_message = "KutsaienkoOlegovuchDmytro"
    cut_length = 4
    target_length = 100

    num_runs = 100  # Максимальна кількість ітерацій
    count, collision_data = example_attack(base_message, num_runs)

    # Запуск аналізу
    attack_analysis(base_message, iterations=num_runs)
