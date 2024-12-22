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


def attack_analysis(attack_function, iterations, messages):
    # Збирання кількості ітерацій для кожного повідомлення
    iteration_counts = []

    #for msg in messages
    #   count, _ = attack_function(msg, 1000)
    for msg in messages:
        count, _ = attack_function(msg, 100000)  # Отримуємо кількість ітерацій
        iteration_counts.append(count)  # Додаємо тільки кількість ітерацій

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
def example_attack(message, max_iterations):
    original_hash = sha3_224(message.encode()).hexdigest()[-8:]  # Останні 8 символів хешу
    hashes = {}
    collision_found = False
    i = 1

    while not collision_found and i <= max_iterations:
        modified_message = f"{message}{i}"
        modified_hash = sha3_224(modified_message.encode()).hexdigest()[-8:]
        #print(f"hash {modified_hash} for message: {modified_message}")
        if modified_hash in hashes:
            collision_found = True
            return i, (hashes[modified_hash], modified_message, modified_hash)  # Повертаємо кількість ітерацій та знайдені повідомлення
        else:
            hashes[modified_hash] = modified_message
        i += 1
    
    return i, None  # Якщо колізія не знайдена


# Основний код
if __name__ == "__main__":
    base_message = "KutsaienkoOlegovuchDmytro"
    cut_length = 4
    target_length = 100

    # Генерація повідомлень
    char_dict = {}
    char_dict = list(generate_char(char_dict, base_message, cut_length, target_length).keys())

    # Виведення інформації про повідомлення
    print(f"Загальна кількість повідомлень: {len(char_dict)}")
    # Виведення перших 30 повідомлень разом із їхніми хеш-значеннями
    print(f"Перші 30 повідомлень разом із хеш-значеннями:")
    for i, message in enumerate(char_dict[:30], start=1):
        hash_value = sha3_224(message.encode()).hexdigest()  # Останні 8 символів хешу
        print(f"{i}. Повідомлення: {message} | Хеш: {hash_value}")

    # Аналіз атаки
    num_runs = 200000  # Максимальна кількість ітерацій
    count, collision_data = example_attack(base_message, num_runs)

    # Виведення результатів атаки
    if collision_data:
        print("\nКолізія знайдена!")
        print(f"Кількість ітерацій до колізії: {count}")
        print("Повідомлення, які утворюють колізію:")
        print(f"Повідомлення 1: {collision_data[0]}, Хеш: {sha3_224(collision_data[0].encode()).hexdigest()}")
        print(f"Повідомлення 2: {collision_data[1]}, Хеш: {sha3_224(collision_data[1].encode()).hexdigest()}")
    else:
        print("\nКолізія не знайдена в межах максимальних ітерацій.")

    # Запуск аналізу
    attack_analysis(example_attack, iterations=num_runs, messages=[*char_dict])

