from pathlib import Path

from fastapi import FastAPI, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.predictor import predict_house_price

app = FastAPI(
    title="EstateAI House Price Predictor"
)

# Static Files
app.mount(
    "/static",
    StaticFiles(directory="app/static"),
    name="static"
)

# Templates
BASE_DIR = Path(__file__).resolve().parent

templates = Jinja2Templates(
    directory=str(BASE_DIR / "templates")
)


# ---------------- HOME ---------------- #

@app.get("/")
def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "price": None,
            "model": None,
            "accuracy": None
        }
    )


# ---------------- PREDICT ---------------- #

@app.post("/predict")
def predict(
    request: Request,

    OverallQual: int = Form(...),
    GrLivArea: int = Form(...),
    YearBuilt: int = Form(...),
    BedroomAbvGr: int = Form(...),
    FullBath: int = Form(...),
    GarageCars: int = Form(...),
    TotalBsmtSF: int = Form(...),
    Fireplaces: int = Form(...),
    Neighborhood: str = Form(...)
):

    house_data = {
        "OverallQual": OverallQual,
        "GrLivArea": GrLivArea,
        "YearBuilt": YearBuilt,
        "BedroomAbvGr": BedroomAbvGr,
        "FullBath": FullBath,
        "GarageCars": GarageCars,
        "TotalBsmtSF": TotalBsmtSF,
        "Fireplaces": Fireplaces,
        "Neighborhood": Neighborhood
    }

    # Predict house price
    price = predict_house_price(house_data)

    # Format result
    formatted_price = f"${price:,.2f}"

    model_name = "Random Forest Regressor"
    accuracy = "R² Score: 0.89"

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "price": formatted_price,
            "model": model_name,
            "accuracy": accuracy
        }
    )