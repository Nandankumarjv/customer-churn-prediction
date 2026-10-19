
from pathlib import Path

import joblib
import pandas as pd
from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from backend.database import Base, engine, get_db
from backend.schema import PredictionRecord

BASE_DIR = Path(__file__).resolve().parent.parent

pipeline = joblib.load(BASE_DIR / "customer_churn_pipeline.pkl")
threshold = float(joblib.load(BASE_DIR / "churn_threshold.pkl"))

app = FastAPI(
    title="Customer Churn Prediction API",
    version="1.0.0",
)

# Create database tables if they do not already exist
Base.metadata.create_all(bind=engine)


class CustomerFeatures(BaseModel):
    age: float
    tenure_months: float
    monthly_charges: float
    total_charges: float
    support_calls: float
    contract_type: str
    payment_method: str
    internet_service: str
    streaming: str
    auto_pay: str
    tech_support: str
    satisfaction_score: float
    monthly_usage_gb: float


@app.get("/")
def home():
    return {"message": "Customer Churn Prediction API is running"}


@app.get("/health")
def health():
    return {
        "status": "ok",
        "model_loaded": True,
        "threshold": threshold,
    }


@app.post("/predict")
def predict_churn(
    customer: CustomerFeatures,
    db: Session = Depends(get_db),
):
    input_df = pd.DataFrame([customer.model_dump()])

    try:
        probabilities = pipeline.predict_proba(input_df)[0]
        classes = list(pipeline.classes_)
        churn_index = classes.index(1)
        churn_probability = float(probabilities[churn_index])
        prediction = int(churn_probability >= threshold)

        record = PredictionRecord(
            features=customer.model_dump(),
            prediction=prediction,
            churn_probability=churn_probability,
        )

        db.add(record)
        db.commit()
        db.refresh(record)

        return {
            "id": record.id,
            "prediction": prediction,
            "churn_probability": round(churn_probability, 4),
            "threshold": threshold,
            "message": (
                "Customer likely to churn"
                if prediction == 1
                else "Customer unlikely to churn"
            ),
            "created_at": record.created_at,
        }

    except Exception as exc:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Prediction or database save failed.",
        ) from exc


@app.get("/predictions")
def get_predictions(
    limit: int = 20,
    db: Session = Depends(get_db),
):
    if not 1 <= limit <= 100:
        raise HTTPException(
            status_code=400,
            detail="limit must be between 1 and 100",
        )

    records = (
        db.query(PredictionRecord)
        .order_by(PredictionRecord.id.desc())
        .limit(limit)
        .all()
    )

    return [
        {
            "id": record.id,
            "features": record.features,
            "prediction": record.prediction,
            "churn_probability": record.churn_probability,
            "created_at": record.created_at,
        }
        for record in records
    ]


@app.get("/predictions/{prediction_id}")
def get_prediction(
    prediction_id: int,
    db: Session = Depends(get_db),
):
    record = db.get(PredictionRecord, prediction_id)

    if record is None:
        raise HTTPException(
            status_code=404,
            detail="Prediction not found",
        )

    return {
        "id": record.id,
        "features": record.features,
        "prediction": record.prediction,
        "churn_probability": record.churn_probability,
        "created_at": record.created_at,
    }
