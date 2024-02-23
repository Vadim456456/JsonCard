import json
import datetime
import re

with open('operations.json', 'r', encoding='UTF-8') as config_file:
    data = json.load(config_file)
    operations_by_client = {}
    PAYMENT_SYSTEMS = {
        "Visa Gold": ["9"],
        "MasterCard": ["10"],
        "Мир": ["3"],
        "Счет": ["4"],
        "Maestro": ["7"],
        "Visa Platinum": ["13"],
        "Visa Classic": ["12"]
    }
    def format_date(data):
        date_obj = datetime.datetime.strptime(data, '%Y-%m-%dT%H:%M:%S.%f')
        return date_obj.strftime('%d.%m.%Y')

    def format_card_number(card_number):
        payment_system = next((k for k, v in PAYMENT_SYSTEMS.items() if card_number.startswith(k)), None)

        if payment_system == "Visa Gold":
            masked_card_number = re.sub(r'(\d{4})(\d{2})\d{6}(\d{4})', r'\1 \2** **** \3', card_number)
        elif payment_system == "MasterCard":
            masked_card_number = re.sub(r'(\d{4})(\d{2})\d{6}(\d{4})', r'\1 \2** **** \3', card_number)
        elif payment_system == "Мир":
            masked_card_number = re.sub(r'(\d{4})(\d{2})\d{10}(\d{4})', r'\1 \2** **** \3', card_number)
        elif payment_system == "Счет":
            masked_card_number = re.sub(r'(\d{4})(\d{2})\d{10}(\d{4})', r'\1 \2** **** \3', card_number)
        elif payment_system == "Maestro":
            masked_card_number = re.sub(r'(\d{2})(\d{2})\d{8}(\d{4})', r'\1 \2** **** \3', card_number)
        elif payment_system == "Visa Platinum":
            masked_card_number = re.sub(r'(\d{4})(\d{2})\d{6}(\d{4})', r'\1 \2** **** \3', card_number)
        elif payment_system == "Visa Classic":
            masked_card_number = re.sub(r'(\d{4})(\d{2})\d{6}(\d{4})', r'\1 \2** **** \3', card_number)
        else:
            masked_card_number = card_number

        return masked_card_number

    def get_last_digits(data):
        return data[-4:]

    for group in data:
        from_field = group.get("from")
        state_field = group.get("state")
        if state_field == "EXECUTED" and from_field is not None:
            if from_field not in operations_by_client:
                operations_by_client[from_field] = []

            operations_by_client[from_field].append({
                'date': format_date(group["date"]),
                'description': group["description"],
                'from': format_card_number(from_field),
                'to': f"**{get_last_digits(group['to'])}",
                'amount': group["operationAmount"]["amount"],
                'name': group["operationAmount"]["currency"]["name"]
            })

    last_5_clients = sorted(operations_by_client.items(), key=lambda item: item[1][0]['date'], reverse=True)[:5]

    for client, operations in last_5_clients:
        for operation in operations:
            money = (f" {operation['amount']}, {operation['name']}")
            money = money.replace(",","")

            time_is_money = (f"{operation['date']},{operation['description']}")
            time_is_money = time_is_money.replace(","," ")

            print(time_is_money)
            print(f" {format_card_number(operation['from'])}  -> {operation['to']}")
            print(money)
            print()

