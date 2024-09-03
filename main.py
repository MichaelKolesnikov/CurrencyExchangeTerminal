import random
from tabulate import tabulate

currencies = [
    'RUB',
    'USD',
    'EUR',
    'USDT',
    'BTC'
]

user_funds = {
    'RUB': 1000000,
    'USD': 0,
    'EUR': 0,
    'USDT': 0,
    'BTC': 0
}

terminal_funds = {
    'RUB': 10000,
    'USD': 1000,
    'EUR': 1000,
    'USDT': 1000,
    'BTC': 1.5
}

exchange_rates = {
    'RUB': {
        'USD': 1 / 90,
        'EUR': 1 / 100
    },
    'USD': {
        'RUB': 90.0,
        'EUR': 0.9,
        'USDT': 1,
        'BTC': 1 / 59111.76
    },
    'EUR': {
        'RUB': 100.0,
        'USD': 1 / 0.9
    },
    'USDT': {
        'USD': 1
    },
    'BTC': {
        'USD': 59111.76
    }
}


def update_exchange_rates():
    for currency_num1 in range(len(currencies)):
        for currency_num2 in range(currency_num1 + 1, len(currencies)):
            cur1 = currencies[currency_num1]
            cur2 = currencies[currency_num2]
            if cur2 not in exchange_rates[cur1]:
                continue
            change = random.uniform(-0.05, 0.05)
            exchange_rates[cur1][cur2] *= (1 + change)
            exchange_rates[cur2][cur1] = 1 / exchange_rates[cur1][cur2]


def display_funds():
    user_data = [[currency, amount] for currency, amount in user_funds.items()]
    terminal_data = [[currency, amount] for currency, amount in terminal_funds.items()]

    table = []
    for u_row, t_row in zip(user_data, terminal_data):
        table.append([u_row[0], u_row[1], t_row[1]])

    headers = ["Currency", "User", "Terminal"]
    print(tabulate(table, headers, tablefmt="grid"))


def display_exchange_rates():
    table_data = []
    for from_currency in currencies:
        row = [from_currency]
        for to_currency in currencies:
            if from_currency == to_currency:
                row.append('-')
            else:
                rate = exchange_rates[from_currency].get(to_currency, '-')
                row.append(rate)
        table_data.append(row)

    headers = [" "] + currencies

    print(tabulate(table_data, headers, tablefmt="grid"))


def exchange(from_currency, to_currency, amount):
    if from_currency == to_currency:
        print("Cannot exchange the same currency.")
        return

    if from_currency not in exchange_rates or to_currency not in exchange_rates[from_currency]:
        print("Invalid currency pair.")
        return
    else:
        rate = exchange_rates[from_currency][to_currency]

    if user_funds[from_currency] < amount:
        print("Insufficient funds.")
        return

    converted_amount = amount * rate

    if terminal_funds[to_currency] < converted_amount:
        print("Terminal does not have enough funds to complete the transaction.")
        return

    user_funds[from_currency] -= amount
    user_funds[to_currency] += converted_amount
    terminal_funds[from_currency] += amount
    terminal_funds[to_currency] -= converted_amount

    update_exchange_rates()
    print(f"Exchanged {amount} {from_currency} to {converted_amount} {to_currency}.")


def main():
    while True:
        print("\nOptions:")
        print("1. Display funds")
        print("2. Display exchange rates")
        print("3. Exchange currency")
        print("4. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            display_funds()
        elif choice == '2':
            display_exchange_rates()
        elif choice == '3':
            from_currency = input("Enter from currency: ").upper()
            to_currency = input("Enter to currency: ").upper()
            try:
                amount = float(input("Enter amount: "))
            except (Exception, ):
                print("Wrong amount")
                continue
            exchange(from_currency, to_currency, amount)
        elif choice == '4':
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
