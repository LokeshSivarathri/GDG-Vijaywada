from flask import Flask, render_template, request, jsonify
from cricket_agent.ml_model import predict_best_ball

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    field_setup = data.get('field_setup', {})
    prediction = predict_best_ball(field_setup)
    
    # Reasonings based on ml_model.py heuristics
    reasoning = ""
    if prediction == 'Outswinger':
        reasoning = "With a Slip and Point in place, an outswinger tempts the batsman to play away from the body, increasing the chance of an outside edge to the slip or a catch at point."
    elif prediction == 'Bouncer':
        reasoning = "Fine Leg and Square Leg are perfectly positioned for a hook or pull shot. A well-directed bouncer can surprise the batsman and result in a top edge caught in the deep."
    elif prediction == 'Inswinger':
        reasoning = "Mid Wicket and Mid On are ready to intercept flick or drive shots. An inswinger aimed at the stumps cramps the batsman for room, increasing chances for LBW or bowled."
    elif prediction == 'Slower Ball':
        reasoning = "Cover and Mid Off are present to catch the ball if it is driven early. A slower ball deceives the batsman's timing, often resulting in a catch in the cover region."
    else:
        reasoning = "This field setup is quite balanced. A solid 'Good Length' ball hitting the top of off-stump remains the most consistent wicket-taking delivery."
        
    return jsonify({
        'prediction': prediction,
        'reasoning': reasoning
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
