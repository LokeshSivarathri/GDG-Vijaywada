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
    print("🏏 IPL T20 AI Strategy Agent 🏏")
    print("===========================================")
    print("Welcome! I am your AI assistant for IPL T20 bowling strategy.")
    print("Provide the fielding positions you have set up, and I will predict")
    print("the best ball for a bowler to bowl to get a wicket.")
    print("-" * 43)
    
    field_setup = {}
    bowler_type = 'pace'
    
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
        
        # If a second arg is provided for bowler type, use it, else default to pace
        if len(sys.argv) > 2 and sys.argv[2] in ['pace', 'spin']:
            bowler_type = sys.argv[2]
        print(f"Using bowler type: {bowler_type.capitalize()}")
            
    else:
        while True:
            try:
                b_type = input("Is the bowler Pace or Spin? (pace/spin): ").strip().lower()
                if b_type in ['pace', 'spin']:
                    bowler_type = b_type
                    break
                else:
                    print("Invalid input. Please enter 'pace' or 'spin'.")
            except EOFError:
                print("\nEOF encountered. Exiting...")
                return

        print("\nEnter '1' if the fielder is present in the position, else '0':\n")
        
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

    print(f"\nAnalyzing {bowler_type} bowler field setup using our Machine Learning model...")
    prediction = predict_best_ball(field_setup, bowler_type)
    
    print("===========================================")
    print(f"🎯 RECOMMENDED BALL: {prediction.upper()} 🎯")
    print("===========================================")
    
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
        
    print(f"\n💡 Agent Reasoning:\n{reasoning}\n")

if __name__ == "__main__":
    main()
