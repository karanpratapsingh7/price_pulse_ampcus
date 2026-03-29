# Price Pulse — Intelligent Pricing Engine

An AI-powered pricing system that tracks product prices, analyzes competitor pricing, and recommends optimal pricing strategies using machine learning.

![Price Pulse](https://img.shields.io/badge/Price_Pulse-v1.0-blue?style=for-the-badge) ![Python](https://img.shields.io/badge/Python-3.11+-green?style=flat-square) ![React](https://img.shields.io/badge/React-19-61DAFB?style=flat-square) ![Flask](https://img.shields.io/badge/Flask-3.1-black?style=flat-square)

---

## 📋 Table of Contents

- [Project Overview](#project-overview)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Setup Instructions](#setup-instructions)
- [API Documentation](#api-documentation)
- [ML Model Documentation](#ml-model-documentation)
- [Environment Variables](#environment-variables)
- [Docker Setup](#docker-setup)
- [Architecture Decision Records](#architecture-decision-records)

---

## Project Overview

Price Pulse is a modular, production-ready system consisting of:

1. **React Frontend** — Dashboard for viewing products, price trends, competitor comparisons, and AI-driven recommendations
2. **Flask Backend API** — RESTful API with business logic, data ingestion, and ML integration
3. **ML Engine** — Hybrid Gradient Boosting + rule-based pricing with demand elasticity
4. **SQLite/PostgreSQL Database** — Persistent storage with optimized indexes for time-series queries

### Key Features

- 📊 **Product Dashboard** — Interactive product cards with sparkline charts and competitor price indicators
- 📈 **Historical Price Trends** — Multi-line charts showing our prices vs 5 competitors over 6 months
- 🤖 **AI Price Recommendations** — ML-predicted prices with hybrid rule-based adjustments
- 🎯 **Demand-based Dynamic Pricing** — Automatic price adjustments based on demand signals
- 🔍 **Competitor Analysis** — Real-time comparison table with competitive positioning indicators
- 📊 **Model Transparency** — Feature importance, confidence scores, and reasoning explanations

---

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    FRONTEND (React + Vite)               │
│  ┌───────────┐  ┌──────────────┐  ┌──────────────────┐  │
│  │ Dashboard  │  │Product Detail│  │ Recommendations  │  │
│  │  (Grid)    │  │  (Charts)    │  │   (ML Table)     │  │
│  └─────┬─────┘  └──────┬───────┘  └────────┬─────────┘  │
│        └───────────────┼────────────────────┘            │
│                        │ Axios HTTP                      │
└────────────────────────┼─────────────────────────────────┘
                         │
         ┌───────────────▼───────────────┐
         │      BACKEND (Flask API)       │
         │  ┌─────────────────────────┐  │
         │  │     REST API Routes     │  │
         │  │  /products  /prices     │  │
         │  │  /predict   /recommend  │  │
         │  └──────────┬──────────────┘  │
         │             │                 │
         │  ┌──────────▼──────────────┐  │
         │  │    Business Logic       │  │
         │  │  ┌────────┐ ┌────────┐  │  │
         │  │  │Pricing │ │  Data  │  │  │
         │  │  │Engine  │ │Ingest  │  │  │
         │  │  └───┬────┘ └────────┘  │  │
         │  │      │                  │  │
         │  │  ┌───▼────────────────┐ │  │
         │  │  │   ML Model (GBR)   │ │  │
         │  │  │  + Rule Engine     │ │  │
         │  │  └────────────────────┘ │  │
         │  └─────────────────────────┘  │
         └───────────────┬───────────────┘
                         │
              ┌──────────▼──────────┐
              │  DATABASE (SQLite)   │
              │  ┌────────────────┐  │
              │  │   Products     │  │
              │  │   PriceHistory │  │
              │  │   Competitor   │  │
              │  │   Prices       │  │
              │  └────────────────┘  │
              └─────────────────────┘
```

---

##  Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Frontend | React 19 + Vite | UI framework & build tool |
| Styling | Tailwind CSS v3 | Utility-first CSS |
| Charts | Recharts | Interactive data visualization |
| Icons | Lucide React | Modern icon library |
| Backend | Flask 3.1 | REST API server |
| ORM | SQLAlchemy 2.0 | Database abstraction |
| Database | SQLite (dev) / PostgreSQL (prod) | Persistent storage |
| ML | scikit-learn 1.6 | Gradient Boosting Regressor |
| Data | pandas / numpy | Data manipulation & feature engineering |
| Container | Docker + Docker Compose | Deployment |

---

## Setup Instructions

### Prerequisites

- Python 3.10+
- Node.js 18+
- npm or yarn

### Backend Setup

```bash
# Navigate to backend
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Generate synthetic dataset
python data/generate_dataset.py

# Train ML model
python -m app.ml.train

# Start the Flask server
python run.py
```

The API will be available at `http://localhost:5000`

### Frontend Setup

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

The app will be available at `http://localhost:5173`

---

## 📡 API Documentation

### Base URL: `http://localhost:5000/api`

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| GET | `/products` | List all products |
| GET | `/products/:id` | Get product details |
| GET | `/categories` | List product categories |
| GET | `/price-history/:id` | Get price history |
| POST | `/predict-price` | ML price prediction |
| GET | `/recommend-price/:id` | Get price recommendation |
| GET | `/recommend-all` | Get all recommendations |
| GET | `/model-info` | ML model info & metrics |

### Example Requests

#### GET /api/products
```json
// Response
{
  "products": [
    {
      "id": 1,
      "name": "Wireless Bluetooth Headphones",
      "category": "Electronics",
      "brand": "SoundMax",
      "current_price": 79.99,
      "cost_price": 35.00,
      "competitor_avg_price": 82.50,
      "price_trend": [
        {"price": 78.50, "date": "2026-03-20"},
        {"price": 79.99, "date": "2026-03-26"}
      ]
    }
  ],
  "total": 20
}
```

#### POST /api/predict-price
```json
// Request
{ "product_id": 1 }

// Response
{
  "predicted_price": 81.45,
  "features_used": { ... },
  "model_metrics": {
    "mae": 2.34,
    "rmse": 3.12,
    "r2": 0.987
  }
}
```

#### GET /api/recommend-price/1
```json
// Response
{
  "recommended_price": 83.20,
  "ml_predicted_price": 81.45,
  "current_price": 79.99,
  "price_change_pct": 4.01,
  "margin_pct": 57.93,
  "confidence": 0.85,
  "adjustments": [
    {
      "rule": "high_demand_boost",
      "adjustment": 6.52,
      "reason": "Demand index (0.82) is high → +8% boost"
    }
  ],
  "reasoning": "ML model predicted $81.45. 1 rule(s) applied..."
}
```

---

## 🤖 ML Model Documentation

### Model: Gradient Boosting Regressor

**Algorithm:** Ensemble of decision trees trained sequentially, where each tree corrects residual errors from the previous trees.

### Features (12 total)

| Feature | Description |
|---------|-------------|
| historical_avg_price | 30-day rolling average of our price |
| competitor_avg_price | Mean of all competitor prices |
| competitor_min_price | Lowest competitor price |
| competitor_max_price | Highest competitor price |
| price_volatility | Std deviation of recent 30 prices |
| demand_index | Demand signal (0.0 to 1.0) |
| cost_price | Product cost / acquisition price |
| price_gap | Our price minus competitor average |
| category_encoded | Label-encoded product category |
| day_of_year | Day number for seasonality |
| days_since_start | Product age in days |
| margin | Current profit margin percentage |

### Training Pipeline

1. **Data loading**: CSV files with synthetic pricing data
2. **Missing data handling**: Forward-fill → median imputation
3. **Feature engineering**: Rolling averages, price gaps, volatility
4. **Train/test split**: 80/20 time-aware split
5. **Hyperparameter tuning**: GridSearchCV (n_estimators, max_depth, learning_rate, subsample)
6. **Evaluation**: MAE, RMSE, R², MAPE
7. **Model persistence**: Saved via joblib

### Hybrid Pricing Rules

Post-ML adjustments enforce business constraints:
- **Margin floor**: Never below cost × 1.10
- **Competitor band**: Stay within ±7% of competitor average
- **Demand boost**: +8% when demand > 0.8
- **Demand discount**: -5% when demand < 0.3

---

## ⚙️ Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `FLASK_ENV` | `development` | Environment mode |
| `FLASK_DEBUG` | `1` | Debug mode |
| `SECRET_KEY` | `...` | Flask secret key |
| `DATABASE_URL` | `sqlite:///price_pulse.db` | Database connection string |
| `ML_MODEL_PATH` | `app/ml/trained_model.pkl` | Path to trained model |
| `LOG_LEVEL` | `INFO` | Logging level |
| `CORS_ORIGINS` | `http://localhost:5173` | Allowed CORS origins |

---

## 🐳 Docker Setup

```bash
# Build and run with Docker Compose
docker-compose up --build

# Frontend: http://localhost:3000
# Backend:  http://localhost:5000
```

---

## 📚 Architecture Decision Records

See the `docs/ADR/` directory for detailed decision records:

- [ADR-001: Tech Stack Selection](docs/ADR/001-tech-stack.md) — Why Flask over Express, React over Vue
- [ADR-002: Database Choice](docs/ADR/002-database-choice.md) — SQLite vs PostgreSQL, schema design
- [ADR-003: ML Approach](docs/ADR/003-ml-approach.md) — Hybrid GBR + rules, why not deep learning

---

## 📁 Project Structure

```
price_pulse/
├── frontend/                   # React + Vite + Tailwind
│   ├── src/
│   │   ├── components/         # Navbar, Layout, ProductCard, StatsBar
│   │   ├── pages/              # Dashboard, ProductDetail, Recommendations
│   │   ├── services/           # API client (axios)
│   │   └── hooks/              # Custom React hooks
│   └── ...
├── backend/                    # Flask API + ML
│   ├── app/
│   │   ├── models.py           # SQLAlchemy models
│   │   ├── routes/             # API endpoints
│   │   ├── services/           # Business logic
│   │   └── ml/                 # ML model, training, evaluation
│   ├── data/                   # Dataset generation & CSV files
│   └── config.py               # Environment configuration
├── docs/ADR/                   # Architecture Decision Records
├── docker-compose.yml          # Docker orchestration
├── Dockerfile.backend          # Backend container
├── Dockerfile.frontend         # Frontend container
└── README.md                   # This file
```

---

## 📄 License

MIT License. Built for educational and demonstration purposes.
