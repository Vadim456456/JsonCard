import json
import datetime

with open('operations.json', 'r', encoding='UTF-8') as config_file:
    data = json.load(config_file)
    operations = []
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

    def get_last_digits(data):
        return data[-4:]

    for group in data:
        state_field = group.get("state")

        if state_field == "EXECUTED":
            operations.append({
                'state': group["state"],
                'id': group["id"],
                'date': format_date(group["date"]),
                'description': group["description"],
                'from': group.get("from"),
                'to': f"**{get_last_digits(group['to'])}",
                'amount': group["operationAmount"]["amount"],
                'name': group["operationAmount"]["currency"]["name"],
            })

    operations.sort(key=lambda item: datetime.datetime.strptime(item['date'], '%d.%m.%Y'), reverse=True)

    for i in range(min(len(operations), 5)):
        operation = operations[i]
        money = (f" {operation['amount']}, {operation['name']}")
        money = money.replace(",","")

        time_is_money = (f"{operation['date']},{operation['description']}")
        time_is_money = time_is_money.replace(","," ")

        print(time_is_money)
        print(f" {(operation['from'])}  -> {operation['to']}")
        print(money)
        print()
