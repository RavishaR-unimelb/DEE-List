import json
import subprocess
from datetime import datetime

# === Replace with your actual model code ===
def predict():
    return [
        {"label": "cat", "confidence": 0.91},
        {"label": "dog", "confidence": 0.88}
    ]

def update_predictions():
    predictions = {
        "predictions": predict(),
        "updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    with open("prediction_output.json", "w") as f:
        json.dump(predictions, f, indent=2)

    subprocess.run(["git", "add", "prediction_output.json"])
    subprocess.run(["git", "commit", "-m", "Update predictions"])
    subprocess.run(["git", "push"])

if __name__ == "__main__":
    update_predictions()
