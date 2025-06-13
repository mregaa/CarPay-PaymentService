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

@app.route('/edit/<payment_id>', methods=['POST', 'GET'])
def edit_payment(payment_id):
    if request.method == 'POST':
        new_status = request.form['status']
        query = """
        mutation {
            updatePaymentStatus(paymentId: "%s", status: "%s") {
                paymentId
                status
            }
        }
        """ % (payment_id, new_status)
        response = requests.post(GRAPHQL_ENDPOINT, json={'query': query})
        data = response.json()
        if 'errors' in data:
            flash('Gagal update status: ' + data['errors'][0]['message'], 'danger')
        else:
            flash('Status pembayaran berhasil diupdate menjadi: ' + data['data']['updatePaymentStatus']['status'], 'success')
        return redirect(url_for('index'))
    else:
        # Ambil data payment untuk form edit
        query = """
        query {
            getPaymentById(paymentId: "%s") {
                paymentId
                status
            }
        }
        """ % payment_id
        response = requests.post(GRAPHQL_ENDPOINT, json={'query': query})
        payment = response.json().get('data', {}).get('getPaymentById', {})
        return render_template('edit_payment.html', payment=payment)

@app.route('/delete/<payment_id>', methods=['POST'])
def delete_payment(payment_id):
    query = """
    mutation {
        deletePayment(paymentId: "%s") {
            success
            message
        }
    }
    """ % payment_id
    response = requests.post(GRAPHQL_ENDPOINT, json={'query': query})
    data = response.json()
    if 'errors' in data:
        flash('Gagal menghapus pembayaran: ' + data['errors'][0]['message'], 'danger')
    else:
        flash('Pembayaran berhasil dihapus.', 'success')
    return redirect(url_for('index'))