import pandas as pd
import os
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix

os.makedirs('models', exist_ok=True)

def train_ml_model():
    if not os.path.exists('data/network_traffic.csv'):
        print("Run generate_dataset.py first.")
        return
        
    df = pd.read_csv('data/network_traffic.csv')
    
    # Feature Engineering for ML
    df['bytes_per_second'] = df['byte_count'] / df['duration_seconds'].clip(lower=0.001)
    df['packets_per_second'] = df['packet_count'] / df['duration_seconds'].clip(lower=0.001)
    
    features = ['packet_count', 'byte_count', 'duration_seconds', 'bytes_per_second', 
                'packets_per_second', 'connection_count', 'failed_connection_count', 
                'syn_count', 'average_packet_size']
    
    X = df[features]
    y = df['label']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)
    
    y_pred = clf.predict(X_test)
    print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))
    print("\nClassification Report:\n", classification_report(y_test, y_pred))
    
    joblib.dump(clf, 'models/ids_rf_model.pkl')
    print("Model saved to models/ids_rf_model.pkl")

if __name__ == "__main__":
    train_ml_model()