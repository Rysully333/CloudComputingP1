from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()

    print("Received data: ", data)

    return jsonify({"message": "Data received"}), 200

if __name__ == '__main__':
    app.run(host="192.168.5.247", port=5000, debug=True)