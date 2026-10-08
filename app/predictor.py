import pickle
import pandas as pd


# Load pipeline
with open("app/estateai_pipeline.pkl", "rb") as f:
    pipeline = pickle.load(f)


def predict_house_price(input_data):

    # convert input to dataframe
    df = pd.DataFrame([input_data])


    # columns required by pipeline
    required_columns = pipeline.feature_names_in_


    # add missing columns
    for col in required_columns:
        if col not in df.columns:
            df[col] = 0


    # keep correct order
    df = df[required_columns]


    # prediction
    prediction = pipeline.predict(df)


    return round(float(prediction[0]), 2)