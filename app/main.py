from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from app.predictor import predict_house_price


app = FastAPI(
    title="EstateAI House Price Predictor"
)


# Static files (CSS)
app.mount(
    "/static",
    StaticFiles(directory="app/static"),
    name="static"
)


# HTML templates
templates = Jinja2Templates(
    directory="app/templates"
)


# Home page
@app.get("/")
def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "prediction": None
        }
    )


# Prediction route
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

    # Create input dictionary
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


    # Run ML pipeline
    price = predict_house_price(house_data)


    formatted_price = f"{price:,.2f}"


    return templates.TemplateResponse(
    request=request,
    name="index.html",
    context={
        "price": formatted_price
    }
)