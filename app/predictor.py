from pathlib import Path
import joblib
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = BASE_DIR / "models" / "estateai_pipeline.pkl"


pipeline = joblib.load(MODEL_PATH)



# Features used during training
TRAIN_FEATURES = pipeline.named_steps["preprocessor"].feature_names_in_



def predict_house_price(house_data):

    df = pd.DataFrame([house_data])


    # Add missing training columns
    for col in TRAIN_FEATURES:

        if col not in df.columns:

            df[col] = 0



    # Keep same order as training
    df = df[TRAIN_FEATURES]


    prediction = pipeline.predict(df)


    return float(prediction[0])