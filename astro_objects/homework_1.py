from functools import reduce

students = [
    {"name": "Alice", "age": 20, "grades": [85, 90, 88, 92]},
    {"name": "Bob", "age": 22, "grades": [78, 89, 76, 85]},
    {"name": "Charlie", "age": 21, "grades": [92, 95, 88, 94]},
    {"name": "David", "age": 23, "grades": [80, 85, 78, 88]},
    {"name": "Eve", "age": 20, "grades": [90, 87, 93, 89]},
    {"name": "Frank", "age": 22, "grades": [75, 80, 85, 79]},
    {"name": "Grace", "age": 21, "grades": [91, 88, 85, 92]},
    {"name": "Hannah", "age": 20, "grades": [82, 77, 89, 84]},
    {"name": "Ian", "age": 22, "grades": [84, 90, 85, 87]},
    {"name": "Jack", "age": 23, "grades": [79, 82, 75, 80]},
    {"name": "Karen", "age": 21, "grades": [90, 91, 89, 92]},
    {"name": "Leo", "age": 20, "grades": [86, 80, 82, 84]},
    {"name": "Megan", "age": 22, "grades": [91, 92, 88, 89]},
    {"name": "Nathan", "age": 21, "grades": [78, 84, 80, 82]},
    {"name": "Olivia", "age": 23, "grades": [95, 93, 94, 96]},
    {"name": "Paul", "age": 20, "grades": [83, 80, 82, 85]},
    {"name": "Quincy", "age": 22, "grades": [79, 85, 87, 81]},
    {"name": "Rachel", "age": 21, "grades": [92, 94, 90, 91]},
    {"name": "Sam", "age": 23, "grades": [77, 80, 76, 81]},
    {"name": "Tina", "age": 20, "grades": [88, 90, 85, 87]},
    {"name": "Umar", "age": 22, "grades": [82, 79, 84, 86]},
    {"name": "Vera", "age": 21, "grades": [91, 88, 87, 89]},
    {"name": "Wendy", "age": 23, "grades": [85, 83, 82, 80]},
    {"name": "Xavier", "age": 20, "grades": [80, 85, 78,84]},
    {"name": "Yara", "age": 22, "grades": [88, 91, 90, 87]},
    {"name": "Zach", "age": 21, "grades": [79, 80, 83, 85]},
    {"name": "Aiden", "age": 23, "grades": [90, 89, 85, 92]},
    {"name": "Bella", "age": 20, "grades": [83, 87, 85, 88]},
    {"name": "Carter", "age": 22, "grades": [78, 82, 80, 85]},
    {"name": "Daisy", "age": 21, "grades": [92, 91, 90, 93]}
]
print("1 ЗАДАЧА:")
#фильтрация по возрасту
print(list(filter(lambda person: person["age"] == 21, students)))
#средний балл каждого студента
print(list(reduce(lambda x, y: x+y, students[i]["grades"])/len(students[i]["grades"]) for i in range(len(students))))
#общий средний балл
print(reduce(lambda x,y: x+y, (reduce(lambda a, b: a+b, student["grades"]) / len(student["grades"]) for student in students)) / len(students))



users = [
    {"name": "Alice", "expenses": [100, 50, 75, 200]},
    {"name": "Bob", "expenses": [50, 75, 80, 100]},
    {"name": "Charlie", "expenses": [200, 300, 50, 150]},
    {"name": "David", "expenses": [100, 200, 300, 400]},
    {"name": "Eve", "expenses": [120, 80, 60, 140]},
    {"name": "Frank", "expenses": [90, 130, 120, 150]},
    {"name": "Grace", "expenses": [110, 70, 95, 85]},
    {"name": "Hannah", "expenses": [200, 150, 180, 130]},
    {"name": "Ian", "expenses": [60, 90, 70, 110]},
    {"name": "Jack", "expenses": [140, 160, 180, 200]},
    {"name": "Karen", "expenses": [70, 80, 100, 90]},
    {"name": "Leo", "expenses": [95, 110, 85, 100]},
    {"name": "Megan", "expenses": [140, 120, 160, 180]},
    {"name": "Nathan", "expenses": [80, 100, 120, 150]},
    {"name": "Olivia", "expenses": [300, 250, 200, 150]},
    {"name": "Paul", "expenses": [85, 95, 90, 100]},
    {"name": "Quincy", "expenses": [150, 170, 130, 120]},
    {"name": "Rachel", "expenses": [120, 110, 105, 115]},
    {"name": "Sam", "expenses": [100, 110, 90, 130]},
    {"name": "Tina", "expenses": [160, 140, 150, 130]},
    {"name": "Umar", "expenses": [100, 90, 80, 110]},
    {"name": "Vera", "expenses": [110, 130, 120, 150]},
    {"name": "Wendy", "expenses": [85, 75, 80, 95]},
    {"name": "Xavier", "expenses": [150, 160, 170, 140]},
    {"name": "Yara", "expenses": [180, 200, 220, 210]},
    {"name": "Zach", "expenses": [90, 95, 85, 100]},
    {"name": "Aiden", "expenses": [130, 120, 110, 150]},
    {"name": "Bella", "expenses": [140, 130, 120, 110]},
    {"name": "Carter", "expenses": [160, 170, 150, 180]},
    {"name": "Daisy", "expenses": [170, 160, 180, 190]}
]
print("2 ЗАДАЧА:")
# Фильтрация по расходам
filtered_users = list(filter(lambda price: (reduce(lambda x, y: x + y, price["expenses"])) > 500, users))
print("Отфильтрованные пользователи:", filtered_users)

# Общая сумма расходов
total_expenses = reduce(lambda x, y: x + y, map(lambda user: reduce(lambda a, b: a + b, user["expenses"]), users))
print("Общая сумма расходов всех пользователей:", total_expenses)

# Общая сумма расходов отфильтрованных пользователей
total_expenses_filtered = reduce(lambda x, y: x + y, map(lambda user: reduce(lambda a, b: a + b, user["expenses"]), filtered_users))
print("Общая сумма расходов отфильтрованных пользователей:", total_expenses_filtered)



print("3 ЗАДАЧА:")

orders = [
    {"order_id": 1, "customer_id": 101, "amount": 150.0},
    {"order_id": 2, "customer_id": 102, "amount": 200.0},
    {"order_id": 3, "customer_id": 101, "amount": 75.0},
    {"order_id": 4, "customer_id": 103, "amount": 100.0},
    {"order_id": 5, "customer_id": 101, "amount": 50.0},
    {"order_id": 6, "customer_id": 104, "amount": 120.0},
    {"order_id": 7, "customer_id": 105, "amount": 90.0},
    {"order_id": 8, "customer_id": 106, "amount": 300.0},
    {"order_id": 9, "customer_id": 107, "amount": 250.0},
    {"order_id": 10, "customer_id": 104, "amount": 110.0},
    {"order_id": 11, "customer_id": 108, "amount": 130.0},
    {"order_id": 12, "customer_id": 109, "amount": 75.0},
    {"order_id": 13, "customer_id": 110, "amount": 220.0},
    {"order_id": 14, "customer_id": 105, "amount": 85.0},
    {"order_id": 15, "customer_id": 102, "amount": 90.0},
    {"order_id": 16, "customer_id": 101, "amount": 130.0},
    {"order_id": 17, "customer_id": 111, "amount": 95.0},
    {"order_id": 18, "customer_id": 103, "amount": 80.0},
    {"order_id": 19, "customer_id": 106, "amount": 150.0},
    {"order_id": 20, "customer_id": 110, "amount": 175.0},
    {"order_id": 21, "customer_id": 101, "amount": 50.0},
    {"order_id": 22, "customer_id": 112, "amount": 250.0},
    {"order_id": 23, "customer_id": 113, "amount": 180.0},
    {"order_id": 24, "customer_id": 114, "amount": 70.0},
    {"order_id": 25, "customer_id": 115, "amount": 90.0},
    {"order_id": 26, "customer_id": 116, "amount": 130.0},
    {"order_id": 27, "customer_id": 112, "amount": 120.0},
    {"order_id": 28, "customer_id": 117, "amount": 95.0},
    {"order_id": 29, "customer_id": 105, "amount": 160.0},
    {"order_id": 30, "customer_id": 107, "amount": 220.0},
    {"order_id": 31, "customer_id": 108, "amount": 70.0},
    {"order_id": 32, "customer_id": 103, "amount": 110.0},
    {"order_id": 33, "customer_id": 106, "amount": 80.0},
    {"order_id": 34, "customer_id": 109, "amount": 200.0},
    {"order_id": 35, "customer_id": 101, "amount": 90.0},
    {"order_id": 36, "customer_id": 113, "amount": 130.0},
    {"order_id": 37, "customer_id": 115, "amount": 50.0},
    {"order_id": 38, "customer_id": 118, "amount": 140.0},
    {"order_id": 39, "customer_id": 104, "amount": 110.0},
    {"order_id": 40, "customer_id": 102, "amount": 60.0},
    {"order_id": 41, "customer_id": 101, "amount": 120.0},
    {"order_id": 42, "customer_id": 110, "amount": 90.0},
    {"order_id": 43, "customer_id": 119, "amount": 180.0},
    {"order_id": 44, "customer_id": 105, "amount": 70.0},
    {"order_id": 45, "customer_id": 101, "amount": 130.0},
    {"order_id": 46, "customer_id": 112, "amount": 160.0},
    {"order_id": 47, "customer_id": 114, "amount": 90.0},
    {"order_id": 48, "customer_id": 116, "amount": 85.0},
    {"order_id": 49, "customer_id": 120, "amount": 300.0},
    {"order_id": 50, "customer_id": 121, "amount": 230.0}
]

#фильтрация заказов
filtered_orders = list(filter(lambda customer: customer["customer_id"] == 101, orders))
print("Отфильтрованные заказы:", filtered_orders)
#подсчёт общей суммы всех заказов для данного клиента
total_amount = reduce(lambda x,y: x+y, map(lambda order: order["amount"], filtered_orders))
print("Общая сумма заказов для данного клиента", total_amount)
#подсчёт средней стоимости заказа для данного клиента
average_amount = total_amount / len(filtered_orders)
print("Средняя стоимость заказов для данного клиента:", average_amount)