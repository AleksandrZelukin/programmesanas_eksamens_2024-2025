import random
import string

# Общее количество выпеченных булочек
TOTAL_BUNS = 15

# Количество покупателей
BUYERS = 8

# Генерируем очередь булочек (случайные буквы латинского алфавита)
buns_queue = [random.choice(string.ascii_uppercase) for _ in range(TOTAL_BUNS)]

# Первые три булочки поступают в продажу
showcase = buns_queue[:3]
next_index = 3  # индекс следующей булочки в очереди

print("Очередь выпеченных булочек:", buns_queue)
print("-" * 50)

for buyer in range(1, BUYERS + 1):
    # Покупатель заранее выбирает букву
    desired = random.choice(string.ascii_uppercase)

    print(f"Покупатель {buyer} хочет булочку с буквой '{desired}'")
    print("В продаже:", showcase)

    if desired in showcase:
        print("✔ Покупка состоялась")
        showcase.remove(desired)

        # Добавляем следующую булочку, если она есть
        if next_index < len(buns_queue):
            showcase.append(buns_queue[next_index])
            next_index += 1
    else:
        print("✖ Такой булочки нет — покупка не состоялась")

    print("-" * 50)

print("Продажа окончена.")
