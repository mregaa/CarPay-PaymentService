from flask import Flask, render_template, request, redirect, url_for, flash
import requests

app = Flask(__name__)
app.secret_key = 'frontend-secret-key'  # for flash messages

GRAPHQL_ENDPOINT = "http://backend:8000/graphql"  # ganti dengan URL kamu

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        order_id = request.form['order_id']
        user_id = request.form['user_id']
        amount = request.form['amount']
        method = request.form['method']

        query = """
        mutation {
            createPayment(orderId: "%s", userId: "%s", amount: %s, method: "%s") {
                paymentId
                status
            }
        }
        """ % (order_id, user_id, amount, method)

        response = requests.post(GRAPHQL_ENDPOINT, json={'query': query})
        data = response.json()

        if 'errors' in data:
            flash('Gagal membuat pembayaran: ' + data['errors'][0]['message'], 'danger')
        else:
            flash('Pembayaran berhasil dibuat dengan status: ' + data['data']['createPayment']['status'], 'success')

        return redirect(url_for('index'))

    # Ambil semua pembayaran
    query = """
    query {
        getAllPayments {
            paymentId
            orderId
            userId
            amount
            paymentMethod
            status
            createdAt
            paidAt
        }
    }
    """
    response = requests.post(GRAPHQL_ENDPOINT, json={'query': query})
    payments = response.json().get('data', {}).get('getAllPayments', [])
    return render_template('index.html', payments=payments)
