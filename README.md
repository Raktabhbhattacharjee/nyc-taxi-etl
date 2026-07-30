# Public Taxi Trip Data Platform

Analytics platform for exploring taxi mobility patterns and operational insights.

This project transforms NYC TLC Yellow Taxi trip data into an analytics-ready PostgreSQL table, exposes the processed data through a read-only FastAPI backend, and visualizes the results in a Streamlit dashboard.

## Architecture

```text
NYC TLC Yellow Taxi CSV
        |
        v
ETL Pipeline
Extract -> Validate -> Clean -> Transform -> Load
        |
        v
PostgreSQL
yellow_taxi_trips
        |
        v
FastAPI Read-Only Analytics API
        |
        v
Streamlit Dashboard
```

```mermaid
flowchart LR
    dataset["NYC TLC Yellow Taxi CSV<br/>January 2026"] --> etl["ETL Pipeline<br/>Extract -> Validate -> Clean -> Transform -> Load"]
    etl --> db["PostgreSQL<br/>yellow_taxi_trips"]
    db --> api["FastAPI<br/>Read-only analytics API"]
    api --> dashboard["Streamlit Dashboard<br/>Overview, Demand, Location, Trip Details"]
```

## ETL Flow

```mermaid
flowchart TB
    raw["Raw CSV<br/>data/raw/"] --> extract["Extract<br/>etl/extract.py"]
    extract --> validate["Validate<br/>etl/validate.py"]
    validate --> trusted["Trusted rows"]
    validate --> quarantine["Quarantined rows"]
    trusted --> clean["Clean<br/>etl/clean.py"]
    clean --> transform["Transform<br/>etl/transform.py"]
    transform --> load["Load<br/>etl/load.py"]
    load --> postgres["PostgreSQL<br/>yellow_taxi_trips"]
```

## Application Request Flow

```mermaid
sequenceDiagram
    participant User
    participant Streamlit
    participant FastAPI
    participant PostgreSQL

    User->>Streamlit: Open dashboard page
    Streamlit->>FastAPI: HTTP GET analytics endpoint
    FastAPI->>PostgreSQL: Read-only SQLAlchemy query
    PostgreSQL-->>FastAPI: Query results
    FastAPI-->>Streamlit: JSON response
    Streamlit-->>User: KPI cards, charts, and tables
```

## Database Model

The project stores processed taxi trips in a single PostgreSQL table: `yellow_taxi_trips`.

Each row represents one completed NYC Yellow Taxi trip. Most fields come directly from the NYC TLC source dataset, including pickup/dropoff timestamps, location IDs, fare amounts, payment type, and trip distance. The ETL pipeline also adds derived analytics fields such as `pickup_date`, `pickup_hour`, `trip_duration_minutes`, and `fare_per_mile`.

```mermaid
erDiagram
    YELLOW_TAXI_TRIPS {
        int id PK
        int vendor_id
        datetime tpep_pickup_datetime
        datetime tpep_dropoff_datetime
        date pickup_date
        int pickup_hour
        varchar pickup_day_name
        numeric trip_duration_minutes
        int passenger_count
        numeric trip_distance
        numeric fare_per_mile
        int ratecode_id
        varchar store_and_fwd_flag
        int pu_location_id
        int do_location_id
        int payment_type
        numeric fare_amount
        numeric tip_amount
        numeric total_amount
    }
```

### Important Fields

- `vendor_id` identifies the TLC TPEP technology provider that recorded the trip. It does not represent the taxi company, driver, or fleet operator.
- `ratecode_id` describes the fare rate category used for the trip, such as standard rate, airport rate, or negotiated fare.
- `payment_type` indicates how the passenger paid, such as credit card, cash, or another TLC-coded payment method.
- `pu_location_id` identifies the taxi zone where the trip started.
- `do_location_id` identifies the taxi zone where the trip ended.
- `trip_distance` is the recorded trip distance in miles.
- `fare_amount` is the base metered fare before tips, tolls, taxes, and surcharges.
- `total_amount` is the final charged amount including fare, tips, tolls, taxes, and applicable surcharges.

## Key Engineering Decisions

- The ETL pipeline is separate from the dashboard so validation, cleaning, transformation, and loading happen once in a controlled stage instead of being repeated in the UI.
- The FastAPI backend is read-only so the dashboard can explore processed data without mutating PostgreSQL.
- Chart types match the business question: bar charts compare discrete categories, area/line charts show demand over time, and horizontal bars rank pickup/dropoff locations.
- `VendorID` is treated as a TLC TPEP technology provider identifier, not as a taxi company, fleet operator, or driver.

## Tech Stack

### Data / ETL

- Python
- pandas
- PostgreSQL
- SQLAlchemy 2.0
- psycopg
- Alembic

### Backend

- FastAPI
- Pydantic
- Uvicorn

### Frontend

- Streamlit
- requests
- Plotly Express

## Project Structure

```text
nyc_taxi_etl/
|-- alembic/
|   `-- versions/
|       `-- 70630161b925_create_yellow_taxi_trips_table.py
|-- api/
|   |-- deps.py
|   |-- main.py
|   |-- schemas.py
|   `-- routes/
|       |-- analytics.py
|       |-- health.py
|       `-- trips.py
|-- dashboard/
|   |-- api.py
|   |-- app.py
|   |-- utils.py
|   `-- pages/
|       |-- 1_Overview.py
|       |-- 2_Demand_Analytics.py
|       |-- 3_Location_Analytics.py
|       `-- 4_Trip_Details.py
|-- data/
|   `-- raw/
|-- etl/
|   |-- extract.py
|   |-- validate.py
|   |-- clean.py
|   |-- transform.py
|   |-- load.py
|   |-- pipeline.py
|   |-- database.py
|   |-- models.py
|   `-- config.py
|-- notebooks/
|   `-- 01_data_profiling.ipynb
|-- main.py
|-- pyproject.toml
`-- README.md
```

## Dashboard Pages

- **Overview** - summarizes overall trip volume and payment behavior.
- **Demand Analytics** - shows when demand peaks by date and pickup hour.
- **Location Analytics** - ranks the busiest pickup and dropoff areas.
- **Trip Details** - displays processed trip-level records with basic filters and fare metrics.

## API Endpoints

| Method | Endpoint |
| --- | --- |
| GET | `/health` |
| GET | `/trips` |
| GET | `/analytics/trips-per-day` |
| GET | `/analytics/trips-by-vendor` |
| GET | `/analytics/trips-by-payment-type` |
| GET | `/analytics/hourly-demand` |
| GET | `/analytics/top-pickup-locations` |
| GET | `/analytics/top-dropoff-locations` |

## Screenshots

![Overview page - KPI summary and payment distribution](docs/screenshots/overview.png)

![Demand Analytics page - daily volume and hourly demand](docs/screenshots/demand-analytics.png)

![Location Analytics page - top pickup and dropoff locations](docs/screenshots/location-analytics.png)

![Trip Details page - processed trip records and fare metrics](docs/screenshots/trip-details.png)

## Setup / How to Run

Install dependencies:

```bash
uv sync
```

Create a `.env` file in the project root:

```env
DATABASE_URL=postgresql+psycopg://postgres:password@localhost:5432/nyc_taxi
```

Run the Alembic migration:

```bash
uv run alembic upgrade head
```

Run the ETL pipeline:

```bash
uv run python main.py
```

Start the FastAPI backend:

```bash
uv run uvicorn api.main:app --reload
```

Open the FastAPI docs:

```text
http://127.0.0.1:8000/docs
```

Start the Streamlit dashboard in a second terminal:

```bash
uv run streamlit run dashboard/app.py
```

Streamlit usually opens at:

```text
http://localhost:8501
```

## Local Testing Checklist

1. Confirm PostgreSQL is running.
2. Confirm `.env` contains `DATABASE_URL`.
3. Run `uv run alembic upgrade head`.
4. Run `uv run python main.py` to load the sample dataset.
5. Run `uv run uvicorn api.main:app --reload`.
6. Check `http://127.0.0.1:8000/health`.
7. Run `uv run streamlit run dashboard/app.py`.
8. Open each dashboard page and confirm charts load.

## Scope & Limitations

This project currently focuses on NYC TLC Yellow Taxi data for January 2026. The architecture can be extended to additional months, taxi datasets, or lookup tables, but the current implementation is limited to the available January 2026 Yellow Taxi CSV and the analytics endpoints already defined in the FastAPI backend.
