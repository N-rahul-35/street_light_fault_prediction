
import pickle
from flask import Flask, render_template, request

app = Flask(__name__, template_folder='template')
model = pickle.load(open('model.pkl', 'rb'))

label_mappings = {'environmental_conditions': {
    'Clear': 0, 'Cloudy': 1, 'Rainy': 2}}
mappings = label_mappings.get('environmental_conditions')


reverse_mapings = {
    0: 'Type-0 (No Fault)',
    1: 'Type-1 (Short Circuit)',
    2: 'Type-2 (Voltage Surge)',
    3: 'Type-3 (Bulb Failure)',
    4: 'Type-4 (Light Flickering)'
}
reverse_text = {
    0: '!!Congratulations Bulb is running well!!',
    1: '!!Sorry need to replace wiring!!',
    2: '!!Turn off Power Supply till voltage stablilizes!!',
    3: '!!Sorry, Please Replace Bulb!!',
    4: '!!Sorry, Please Replace Bulb!!'
}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    y1 = (float(request.form.get('bulb_number')))**0.5
    y2 = (float(request.form.get('power_consumption')))**0.5
    y3 = (float(request.form.get('voltage_levels')))**0.5
    y4 = (float(request.form.get('current_fluctuations')))**0.5
    y5 = (float(request.form.get('temperature')))**0.5
    y7 = (float(request.form.get('current_fluctuations_env')))**0.5
    y6 = (float(mappings[request.form.get('environmental_conditions')]))**0.5
    y_test = [y1, y2, y3, y4, y5, y6, y7]
    print(y_test)
    prediction = model.predict([y_test])
    output = reverse_mapings[prediction[0]]
    return render_template('result.html', prediction_text=f'The case evaluated is of {output} fault in street light', img_link=f'../static/{output}.jpg', warning_text=f'{reverse_text[prediction[0]]}')


if __name__ == '__main__':
    app.run(debug=True)
