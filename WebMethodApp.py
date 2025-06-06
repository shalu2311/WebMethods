from flask import Flask, jsonify, request
import random
app = Flask(__name__)

# Mock database (simulating a banking system)
accounts = {
    "123456": {"balance": 5000, "currency": "USD"},
    "654321": {"balance": 3000, "currency": "USD"}
}

transactions = []

@app.route("/api/account/<account_id>", methods=["GET"])
def get_account(account_id):
    """Retrieve account balance and details."""
    account = accounts.get(account_id)
    if account:
        return jsonify({"account_id": account_id, "balance": account["balance"], "currency": account["currency"]})
    return jsonify({"error": "Account not found"}), 404

@app.route("/api/payment", methods=["POST"])
def process_payment():
    """Process a mock real-time payment between accounts."""
    data = request.json
    sender = data.get("sender")
    receiver = data.get("receiver")
    amount = data.get("amount")

    if sender not in accounts or receiver not in accounts:
        return jsonify({"error": "Invalid sender or receiver account"}), 400

    if accounts[sender]["balance"] < amount:
        return jsonify({"error": "Insufficient funds"}), 400

    transaction_id = random.randint(100000, 999999)
    transactions.append({"id": transaction_id, "sender": sender, "receiver": receiver, "amount": amount})

    accounts[sender]["balance"] -= amount
    accounts[receiver]["balance"] += amount

    return jsonify({"message": "Payment processed", "transaction_id": transaction_id})

@app.route("/api/transactions", methods=["GET"])
def get_transactions():
    """Retrieve all processed transactions."""
    return jsonify(transactions)
    
# GET /balance/<account_id>
@app.route('/balance/<account_id>', methods=['GET'])
def get_balance(account_id):
    account = accounts.get(account_id)
    if not account:
        return jsonify({"error": "Account not found"}), 404
    return jsonify({"account_id": account_id, "balance": account["balance"]})
# POST /transfer
@app.route('/transfer', methods=['POST'])    

def send_money():
    data = request.json
    from_acc = data.get("from_account")
    to_acc = data.get("to_account")
    amount = data.get("amount")
    if not all([from_acc, to_acc, amount]):
        return jsonify({"error": "Missing required fields"}), 400
    from_account = accounts.get(from_acc)
    to_account = accounts.get(to_acc)
    if not from_account or not to_account:
        return jsonify({"error": "Invalid account(s)"}), 404
    if from_account["balance"] < amount:
        return jsonify({"error": "Insufficient balance"}), 400
    from_account["balance"] -= amount
    to_account["balance"] += amount
    return jsonify({
        "message": "Transfer successful",
        "from_account": from_acc,
        "to_account": to_acc,
        "amount": amount
    })
    
# GET /creditcard/<account_id>
@app.route('/creditcard/<account_id>', methods=['GET'])
def get_credit_card(account_id):
    account = accounts.get(account_id)
    if not account:
        return jsonify({"error": "Account not found"}), 404
    return jsonify({"account_id": account_id, "credit_card": account["credit_card"]})

if __name__ == "__main__":
    app.run(debug=True, port=5001)

