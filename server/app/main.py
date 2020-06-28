from flask import Flask, send_file, request, jsonify
from catboost import CatBoostRegressor, CatBoostError, CatBoost
import os

app = Flask(__name__)

model = CatBoost().load_model('car_price_predict')


@app.route("/help")
def main():
	index_path = os.path.join(app.static_folder, "index.html")
	return send_file(index_path)

@app.route("/predict_car_price", methods=['POST'])
def predict_car_price():
	if not request.is_json:
		return 
	content = request.get_json()
	try:
		event_dict = {
			'event_manufacturer_name': content['manufacturer_name'].lower(),
			'event_model_name': content['model_name'].lower(),
			'event_body_type': content['body_type'].lower(),
			'event_transmission': content['transmission'].lower(),
			'event_engine_fuel': content['engine_fuel'].lower(),
			'event_drivetrain': content['drivetrain'].lower(),
			'event_color': content['color'].lower(),
			'event_year_produced': content['year_produced'],
			'event_engine_capacity': content['engine_capacity'],
			'event_engine_power': content['engine_power'],
			'event_odometer_value': content['odometer_value']
		}
	except KeyError as e:
		print(e)
		return jsonify({
			'error': 'Please provide correct JSON as shown in description (GET /help)'
			}), 422
	try:
		event_prediction = model.predict([
			event_dict['event_manufacturer_name'],
			event_dict['event_model_name'],
			event_dict['event_body_type'],
			event_dict['event_transmission'],
			event_dict['event_engine_fuel'],
			event_dict['event_drivetrain'],
			event_dict['event_color'],
			event_dict['event_year_produced'],
			event_dict['event_engine_capacity'],
			event_dict['event_engine_power'],
			event_dict['event_odometer_value']
		])
		return jsonify({
						'predicted_price': round(event_prediction**2)
					}), 200
	except CatBoostError as e:
		print(e)
		return jsonify({
						'error': 'Something wrong with your data values. Please check method description (GET /help).'
					}), 422

	return jsonify({
					'error': 'Something went wrong plese try again'
				}), 418


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=80)

