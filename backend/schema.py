
from datetime import datetime

from sqlalchemy import DateTime, Integer, Float, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import mapped_column

from backend.database import Base


class PredictionRecord(Base):
    __tablename__ = "prediction_history"

    id = mapped_column(Integer, primary_key=True, index=True)
    features = mapped_column(JSONB, nullable=False)
    prediction = mapped_column(Integer, nullable=False)
    churn_probability = mapped_column(Float, nullable=False)
    created_at = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
