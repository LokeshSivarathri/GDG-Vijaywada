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
    bowler_type = data.get('bowler_type', 'pace')
    prediction = predict_best_ball(field_setup, bowler_type=bowler_type)
    
    # Reasonings based on ml_model.py heuristics
    reasoning = ""
    
    if bowler_type == 'pace':
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
    else: # Spin
        if prediction == 'Leg Break':
            reasoning = "With a Slip and Point, a leg break turning away from the right-hander perfectly invites an outside edge or a cut straight to point."
        elif prediction == 'Googly':
            reasoning = "Mid Wicket and Square Leg are in place. A googly turning back into the right-hander will tempt them to play across the line, risking a catch in the leg side."
        elif prediction == 'Flighted Delivery':
            reasoning = "Cover and Mid Off are waiting for the drive. Tossing it up and giving it flight deceives the batsman in the air, creating a catching opportunity."
        elif prediction == 'Arm Ball':
            reasoning = "With Fine Leg and Third Man set, an arm ball that skids straight on can cramp the batsman for room and catch them off guard, potentially leading to a bowled or LBW."
        else:
            reasoning = "A standard off-break hitting the good length area provides a solid mix of economy and wicket-taking threat with this balanced field."
        
    return jsonify({
        'prediction': prediction,
        'reasoning': reasoning
    })

if __name__ == '__main__':
    app.run(debug=True, port=5001)
