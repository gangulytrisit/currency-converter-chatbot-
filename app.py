# from flask import Flask,request,jsonify
# import requests
#
# app = Flask(__name__)
#
# @app.route('/', methods=['POST'])
# def index():
#      data = request.get_json()
#      source_currency = data['queryResult']['parameters']['unit-currency']['currency']
#      amount = data['queryResult']['parameters']['unit-currency']['amount']
#      target_currancy = data['queryResult']['parameters']['currency-name'][0]
#      print (str(source_currency))
#      print (str(amount))
#      print(str(target_currancy))
#      return "Hello"
# if __name__ == "__main__":
#     app.run(debug=True)


from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

API_KEY = 'f13008bf5d79fe85474d0e18'
BASE_URL = f'https://v6.exchangerate-api.com/v6/{API_KEY}/latest/'


@app.route('/', methods=['POST'])
def index():
    data = request.get_json()
    source_currency = data['queryResult']['parameters']['unit-currency']['currency']
    amount = data['queryResult']['parameters']['unit-currency']['amount']
    target_currency = data['queryResult']['parameters']['currency-name'][0]  # Target currency is the first item in the list

    cf = fetch_conversion_factor(source_currency, target_currency)
    final_amount = amount * cf
    final_amount = round(final_amount, 2)
    print(final_amount)

    response = {
        'fulfillmentText': "{} {} is {} {}".format(amount, source_currency, final_amount, target_currency)
    }
    return jsonify(response)


def fetch_conversion_factor(source, target):
    # Fetch exchange rate for the source currency
    url = f'{BASE_URL}{source}'
    response = requests.get(url)
    data = response.json()

    # Extract conversion rate for the target currency
    conversion_rate = data['conversion_rates'].get(target)

    if conversion_rate:
        return conversion_rate
    else:
        raise ValueError(f"Exchange rate for {target} not found.")


if __name__ == "__main__":
    app.run(debug=True)