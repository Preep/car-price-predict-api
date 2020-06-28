from flask import Flask, send_file, request, jsonify
from catboost import CatBoostRegressor
import os

app = Flask(__name__)

model = CatBoostRegressor()
model.load_model('car_price_predict')


@app.route("/")
def main():
    index_path = os.path.join(app.static_folder, "index.html")
    return send_file(index_path)

@app.route("/predict_car_price", methods=['POST'])
def predict_car_price():
	if not request.is_json():
		return 
	content = request.get_json()
	print(content)
	return 'True'



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=80)

