# extensions.py
import requests


class APIException(Exception):
    pass


class CurrencyConverter:
    @staticmethod
    def get_price(base, quote, amount):
        if not base.isalpha() or not quote.isalpha():
            raise APIException("Invalid currency name.")

        if not isinstance(amount, (int, float)) or amount <= 0:
            raise APIException("Invalid amount. Please enter a valid number.")

        url = f'https://api.exchangerate-api.com/v4/latest/{base}'
        response = requests.get(url)
        data = response.json()

        if 'error' in data:
            raise APIException("Currency not found.")

        if quote not in data['rates']:
            raise APIException("Quote currency not found.")

        exchange_rate = data['rates'][quote]
        result = amount * exchange_rate
        return result


class BotHandler:
    @staticmethod
    def handle_command(command):
        command_parts = command.split()
        if len(command_parts) != 3:
            return "Invalid command format. Please use: <base_currency> <quote_currency> <amount>."

        base_currency, quote_currency, amount = command_parts
        try:
            amount = float(amount)
            result = CurrencyConverter.get_price(base_currency, quote_currency, amount)
            return f"{amount} {base_currency} = {result} {quote_currency}"
        except ValueError:
            return "Invalid amount. Please enter a valid number."
        except APIException as e:
            return str(e)

    @staticmethod
    def handle_help():
        return "To use this bot, enter a command in the format: <base_currency> <quote_currency> <amount>.\n" \
               "Example: EUR USD 100\n" \
               "Use /values to see available currencies."

    @staticmethod
    def handle_values():
        return "Available currencies: USD, EUR, RUB"

    @staticmethod
    def handle_message(message):
        if message.startswith('/start') or message.startswith('/help'):
            return BotHandler.handle_help()
        elif message.startswith('/values'):
            return BotHandler.handle_values()
        else:
            return BotHandler.handle_command(message)



