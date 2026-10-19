# Customer Churn Prediction

A machine-learning project that estimates whether a customer is likely to churn. The saved scikit-learn pipeline is served through a FastAPI backend, and prediction requests can be stored in PostgreSQL for later retrieval.

## Project Structure

```text
customer-churn-prediction/
├── backend/
│   ├── main.py          # FastAPI application and prediction endpoints
│   ├── database.py      # SQLAlchemy database connection/session
│   └── schema.py        # SQLAlchemy prediction-history model
├── Customer_churn_prediction.ipynb
├── customer_churn_dataset.csv
├── customer_churn_pipeline.pkl
├── churn_threshold.pkl
├── requirements.txt
├── .gitignore
└── README.md
```

> The structure above reflects the backend layout used in the project. If your local files differ, adjust the tree to match your repository.

## Features

- Loads a trained scikit-learn pipeline from `customer_churn_pipeline.pkl`.
- Uses the saved classification threshold in `churn_threshold.pkl` (currently `0.45`).
- Exposes a REST API with FastAPI.
- Accepts customer details as JSON and returns a churn prediction and probability.
- Stores prediction history in PostgreSQL through SQLAlchemy, when the database is configured and reachable.
- Provides endpoints to retrieve recent predictions and a prediction by ID.

## Tech Stack

- Python
- pandas
- scikit-learn
- FastAPI
- Uvicorn
- SQLAlchemy
- PostgreSQL
- Psycopg
- python-dotenv

## Requirements

- Python version compatible with the packages in `requirements.txt`
- PostgreSQL installed and running
- The trained model and threshold files present in the project root

Use the scikit-learn version specified in `requirements.txt` when loading the saved model artifact.

## Setup

### 1. Clone the repository

```bash
git clone <https://github.com/Nandankumarjv/customer-churn-prediction.git>
cd customer-churn-prediction
```

### 2. Create and activate a virtual environment

**Windows PowerShell**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, you can use the Python executable inside `.venv` directly or follow your system's approved execution-policy guidance.

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Create the PostgreSQL database

Open `psql` or a PostgreSQL client and create a database:

```sql
CREATE DATABASE churn_db;
```

Use a PostgreSQL account that has permission to connect to this database and create the application's table.

### 5. Configure environment variables

Create a `.env` file in the project root:

```env
DATABASE_URL=postgresql+psycopg://postgres:YOUR_PASSWORD@localhost:5432/churn_db
```

Replace `YOUR_PASSWORD` with your local PostgreSQL password. If your username, host, port, or database name differs, update the URL accordingly.

**Never commit `.env` or real database credentials to GitHub.** Ensure `.env` is listed in `.gitignore`.

## Run the API

Run the following command from the project root (the directory containing the `backend` folder):

```bash
python -m uvicorn backend.main:app --reload
```

The development server is normally available at:

- API root: `http://127.0.0.1:8000/`
- Interactive Swagger documentation: `http://127.0.0.1:8000/docs`
- Health endpoint: `http://127.0.0.1:8000/health`

Keep the terminal running while testing the API.

## API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/` | Basic API information |
| `GET` | `/health` | Health check |
| `POST` | `/predict` | Predict churn for one customer and save the result to PostgreSQL |
| `GET` | `/predictions?limit=20` | Retrieve recent prediction records |
| `GET` | `/predictions/{prediction_id}` | Retrieve one prediction by its ID |

The prediction-history endpoints require a working database connection. The exact response fields depend on the schemas implemented in `backend/main.py`.

## Example Prediction Request

Open `http://127.0.0.1:8000/docs`, expand **POST `/predict`**, choose **Try it out**, and submit a JSON body using the following field names:

```json
{
  "age": 40,
  "tenure_months": 5,
  "monthly_charges": 1000,
  "total_charges": 5000,
  "support_calls": 0,
  "contract_type": "Month-to-month",
  "payment_method": "Cash",
  "internet_service": "DSL",
  "streaming": "No",
  "auto_pay": "No",
  "tech_support": "No",
  "satisfaction_score": 5.0,
  "monthly_usage_gb": 20
}
```

This is an example payload, not a guarantee that every categorical value matches the dataset used to train the model. If the API reports a validation or feature-value error, use the exact categorical labels and data types present in your dataset and model pipeline.

The response should include a predicted class and churn probability according to the response schema implemented by the API. The application uses the saved threshold (`0.45`) to classify the positive churn class, if the backend code is configured to apply that threshold.

## Model Features

The saved pipeline expects these feature names:

- `age`
- `tenure_months`
- `monthly_charges`
- `total_charges`
- `support_calls`
- `contract_type`
- `payment_method`
- `internet_service`
- `streaming`
- `auto_pay`
- `tech_support`
- `satisfaction_score`
- `monthly_usage_gb`

Send all required features with names and types matching the `CustomerFeatures` schema in `backend/main.py`.

## Troubleshooting

- **Model loading/version warning:** install the scikit-learn version specified in `requirements.txt`, because serialized scikit-learn objects may not be compatible across versions.
- **Database connection error:** confirm PostgreSQL is running, `churn_db` exists, and `DATABASE_URL` contains the correct credentials and port.
- **Missing environment variable:** ensure `.env` is in the project root and that `backend/database.py` loads it before reading `DATABASE_URL`.
- **Import error for `backend`:** run Uvicorn from the project root using `python -m uvicorn backend.main:app --reload`.
- **Unexpected categorical value:** check the category labels used in the training dataset and the preprocessing pipeline.

## Git and Security

Before committing changes, check the staged files:

```bash
git status
git diff --cached
```

Do not commit `.env`, passwords, tokens, virtual environments, Python cache files, or other secrets. Commit the source code, notebook, dependency file, documentation, and model artifacts only if you intend to distribute them and your repository's size/licensing constraints permit it.

## Future Improvements

- Add automated tests for API validation and prediction behavior.
- Add database migrations for schema changes.
- Add structured logging and clearer error handling.
- Deploy the API with production settings rather than Uvicorn's development reload mode.
