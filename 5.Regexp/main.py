from pprint import pprint
import csv
import re


def parse_phone(phone):
    # Извлекаем все цифры из номера
    digits = re.sub(r"\D", "", phone)
    # Проверяем наличие добавочного номера
    extension = re.search(r"(доб\.?\s*\d+)", phone, flags=re.IGNORECASE)
    # Базовый формат номера
    formatted = re.sub(r"(\d{3})(\d{3})(\d{2})(\d{2})", r"+7(\1)\2-\3-\4", digits[1:11])
    # Добавляем добавочный номер при наличии
    if extension:
        ext_digits = re.sub(r"\D", "", extension.group(0))
        formatted += f" доб.{ext_digits}"
    return formatted


# читаем адресную книгу в формате CSV в список contacts_list

with open("phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

# TODO 1: выполните пункты 1-3 ДЗ

# Обработка ФИО и телефонов
for contact in contacts_list[1:]:
    # Разбиваем первые три поля на составляющие
    parts = " ".join(contact[:3]).split()
    contact[:3] = parts + [""] * (3 - len(parts))
    # Нормализуем телефон
    if contact[5]:
        contact[5] = parse_phone(contact[5])

# Объединение дубликатов
unique_contacts = {}
for contact in contacts_list[1:]:
    key = (contact[0], contact[1])
    if key not in unique_contacts:
        unique_contacts[key] = contact
    else:
        # Объединяем информацию из дублирующихся записей
        for i in range(len(contact)):
            if contact[i] and not unique_contacts[key][i]:
                unique_contacts[key][i] = contact[i]

# Формируем итоговый список с заголовком
result = [contacts_list[0]] + list(unique_contacts.values())


# TODO 2: сохраните получившиеся данные в другой файл
# код для записи файла в формате CSV
with open("phonebook.csv", "w", encoding="utf-8") as f:
    datawriter = csv.writer(f, delimiter=",", lineterminator="\n")
    # Вместо contacts_list подставьте свой список
    datawriter.writerows(result)
