import sys
import os
import argparse
from ml_model import predict_best_ball

# Field positions list based on standard cricket
POSITIONS = [
    'Slip', 'Third Man', 'Point', 'Cover', 'Mid Off', 
    'Mid On', 'Mid Wicket', 'Square Leg', 'Fine Leg'
]

def main():
    print("===========================================")
    print("🏏 IPL T20 Pace Bowler AI Agent 🏏")
    print("===========================================")
    print("Welcome! I am your AI assistant for IPL T20 bowling strategy.")
    print("Provide the fielding positions you have set up, and I will predict")
    print("the best ball for a pace bowler to bowl to get a wicket.")
    print("-" * 43)
    
    print("\nEnter '1' if the fielder is present in the position, else '0':\n")
    
    field_setup = {}
    
    # In a real scenario, this could be parsed from an image or a UI
    # For now, we take input from the user (or default to the image provided)
    
    # The image provided in the prompt shows:
    # Slip, Wicket Keeper (not needed for model), Point, Cover, Mid Off, 
    # Mid On, Mid Wicket, Square Leg, Fine Leg
    # We'll use this as a default option if no args provided
    
    if len(sys.argv) > 1 and sys.argv[1] == "--demo":
        print("Using demo mode with the field setup from the provided image...")
        field_setup = {
            'Slip': 1,
            'Third Man': 0,
            'Point': 1,
            'Cover': 1,
            'Mid Off': 1,
            'Mid On': 1,
            'Mid Wicket': 1,
            'Square Leg': 1,
            'Fine Leg': 1
        }
        for pos, val in field_setup.items():
            print(f"  {pos}: {'Present' if val == 1 else 'Empty'}")
    else:
        for pos in POSITIONS:
            while True:
                try:
                    val = input(f"Is there a fielder at {pos}? (1/0): ")
                    if val in ['0', '1']:
                        field_setup[pos] = int(val)
                        break
                    else:
                        print("Invalid input. Please enter 1 or 0.")
                except EOFError:
                    print("\nEOF encountered. Exiting...")
                    return

    print("\nAnalyzing field setup using our Machine Learning model...")
    prediction = predict_best_ball(field_setup)
    
    print("===========================================")
    print(f"🎯 RECOMMENDED BALL: {prediction.upper()} 🎯")
    print("===========================================")
    
    # Give some realistic reasoning based on the heuristics used to train the model
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
        
    print(f"\n💡 Agent Reasoning:\n{reasoning}\n")

if __name__ == "__main__":
    main()
