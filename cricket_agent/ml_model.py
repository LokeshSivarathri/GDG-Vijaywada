import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import pickle
import os

MODEL_PATH = "cricket_agent/model.pkl"
ENCODER_PATH = "cricket_agent/encoder.pkl"

def generate_synthetic_data(num_samples=1000):
    np.random.seed(42)
    
    # 9 fielding positions
    data = {
        'Slip': np.random.randint(0, 2, num_samples),
        'Third Man': np.random.randint(0, 2, num_samples),
        'Point': np.random.randint(0, 2, num_samples),
        'Cover': np.random.randint(0, 2, num_samples),
        'Mid Off': np.random.randint(0, 2, num_samples),
        'Mid On': np.random.randint(0, 2, num_samples),
        'Mid Wicket': np.random.randint(0, 2, num_samples),
        'Square Leg': np.random.randint(0, 2, num_samples),
        'Fine Leg': np.random.randint(0, 2, num_samples),
    }
    
    df = pd.DataFrame(data)
    
    # Logic to determine best ball based on field
    targets = []
    for _, row in df.iterrows():
        # Heuristics for synthetic data based on cricket logic for Pace Bowlers
        if row['Slip'] == 1 and row['Point'] == 1:
            targets.append('Outswinger') # Try to get caught behind or in slips/point
        elif row['Fine Leg'] == 1 and row['Square Leg'] == 1:
            targets.append('Bouncer') # Trap for the hook/pull shot
        elif row['Mid Wicket'] == 1 and row['Mid On'] == 1:
            targets.append('Inswinger') # Attack stumps, cramp room
        elif row['Mid Off'] == 1 and row['Cover'] == 1:
            targets.append('Slower Ball') # Tempting drive
        else:
            # Default or balanced
            targets.append('Good Length') # Standard wicket-taking delivery
            
    df['Target'] = targets
    return df

def train_model():
    print("Generating synthetic data...")
    df = generate_synthetic_data(5000)
    
    X = df.drop('Target', axis=1)
    y = df['Target']
    
    # Encode targets
    le = LabelEncoder()
    y_encoded = le.fit_transform(y)
    
    X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)
    
    print("Training Random Forest Classifier...")
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    print(f"Model accuracy on test set: {model.score(X_test, y_test):.2f}")
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    
    # Save model and encoder
    with open(MODEL_PATH, 'wb') as f:
        pickle.dump(model, f)
    with open(ENCODER_PATH, 'wb') as f:
        pickle.dump(le, f)
        
    print(f"Model saved to {MODEL_PATH}")

def predict_best_ball(field_setup):
    """
    field_setup: dict of fielder positions, e.g., {'Slip': 1, 'Point': 1, ...}
    Returns predicted ball type.
    """
    if not os.path.exists(MODEL_PATH):
        train_model()
        
    with open(MODEL_PATH, 'rb') as f:
        model = pickle.load(f)
    with open(ENCODER_PATH, 'rb') as f:
        le = pickle.load(f)
        
    # Default positions to 0 if not provided
    features = ['Slip', 'Third Man', 'Point', 'Cover', 'Mid Off', 'Mid On', 'Mid Wicket', 'Square Leg', 'Fine Leg']
    input_data = {f: 0 for f in features}
    
    for k, v in field_setup.items():
        if k in input_data:
            input_data[k] = v
            
    df_input = pd.DataFrame([input_data])
    prediction_encoded = model.predict(df_input)
    prediction = le.inverse_transform(prediction_encoded)[0]
    
    return prediction

if __name__ == "__main__":
    train_model()
