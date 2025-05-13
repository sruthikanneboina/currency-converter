import requests
from flask import Flask, render_template, request

app = Flask(__name__)

API_KEY = 'your_api_key'  # Replace with your API key if necessary

def get_exchange_rate(from_currency, to_currency):
    url = f"https://api.exchangerate-api.com/v4/latest/{from_currency}"  # Example API
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        print(f"API Response: {data}")  # Debugging: Print the API response

        if to_currency in data['rates']:
            return data['rates'][to_currency]
        else:
            return None
    else:
        return None

@app.route('/', methods=['GET', 'POST'])
def index():
    amount = request.form.get('amount', type=float)
    from_currency = request.form.get('from_currency', 'USD')
    to_currency = request.form.get('to_currency', 'INR')
    
    converted_amount = None
    exchange_rate = None
    error_message = None

    if amount:
        exchange_rate = get_exchange_rate(from_currency, to_currency)
        
        if exchange_rate:
            converted_amount = amount * exchange_rate
        else:
            error_message = "Conversion failed. Please try again."

    return render_template('index.html', amount=amount, from_currency=from_currency, to_currency=to_currency, 
                           converted_amount=converted_amount, exchange_rate=exchange_rate, error_message=error_message)

if __name__ == '__main__':
    app.run(debug=True)
