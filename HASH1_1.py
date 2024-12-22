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
def generate_char(char_dict, base_message, cut_length, target_length=100):
    len_char = len(base_message)
    char = [chr(i) for i in range(32, 127)]
    
    while len(char_dict) < target_length:
        msg_list = list(base_message)
        idx = random.randint(0, len_char - 1)
        
        while True:
            new_char = random.choice(char)
            if base_message[idx] != new_char:
                break
        
        msg_list[idx] = new_char
        modified_message = ''.join(msg_list)
        char_dict[modified_message] = get_hash(modified_message)[-cut_length:]
    
    return char_dict

# Функція для аналізу атаки
def attack_analysis(attack_function, iterations, messages):
    # Збирання кількості ітерацій для кожного повідомлення
    iteration_counts = [attack_function(msg, iterations) for msg in messages]

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
    Зведена статистика:
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
def example_attack(message, max_iterations):
    original_hash = get_hash(message)[-4:]  # Останні 4 символи хешу
    number = 1  # Лічильник згенерованих повідомлень
    
    while True:
        # Генерація нового повідомлення
        test_message = f"{message}{number}"
        test_hash = get_hash(test_message)[-4:]  # Хеш нового повідомлення
        if test_hash == original_hash:  # Перевірка збігу хешів
            return number  # Кількість ітерацій до знаходження збігу
        number += 1
    

# Основний код
if __name__ == "__main__":
    base_message = "KutsaienkoDmytroOlegovuch"
    cut_length = 4
    target_length = 100

    # Генерація повідомлень
    char_dict = {}
    char_dict = generate_char(char_dict, base_message, cut_length, target_length)

    # Аналіз атаки
    attack_analysis(example_attack, iterations=20000, messages=list(char_dict.keys()))