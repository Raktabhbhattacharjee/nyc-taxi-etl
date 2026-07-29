# Public Taxi Trip Data Platform

A production-oriented backend and data engineering project that converts raw NYC TLC Yellow Taxi trip records into an analytics-ready PostgreSQL dataset with a FastAPI REST API and Streamlit dashboard.

---

## Project Overview

This repository implements a full backend data pipeline for NYC Yellow Taxi trips. It is designed to:

- consume raw CSV trip records,
- validate and quarantine invalid inputs,
- clean and normalize trusted rows,
- enrich records with analytics-friendly features,
- persist data into PostgreSQL,
- expose analytics through FastAPI,
- visualize results in a Streamlit dashboard.

The project demonstrates real-world backend engineering patterns in ETL, relational database integration, API design, and dashboard delivery.

---

## Project Highlights

- End-to-End ETL Pipeline
- PostgreSQL Relational Database
- SQLAlchemy ORM Model
- Alembic Database Migration
- FastAPI REST API
- Pydantic Schema Validation
- Streamlit Dashboard
- Data Validation and Quarantine Logic
- Feature Engineering for Analytics

---

## System Architecture

The diagram below shows the actual end-to-end flow implemented in this repository.

```mermaid
flowchart TB
    raw["Raw NYC TLC CSV"]
    etl["ETL Pipeline\n(etl/)"]
    db["PostgreSQL"]
    api["FastAPI\n(api/)"]
    dashboard["Streamlit Dashboard\n(dashboard/)"]

    raw --> etl --> db --> api --> dashboard
```

---

## Technology Stack

| Layer                | Technology        |
| -------------------- | ----------------- |
| Programming Language | Python 3.13+      |
| Data Processing      | pandas            |
| API Framework        | FastAPI           |
| Dashboard            | Streamlit         |
| Database             | PostgreSQL        |
| ORM                  | SQLAlchemy 2.0    |
| Migrations           | Alembic           |
| Settings             | pydantic-settings |
| HTTP Server          | Uvicorn           |
| HTTP Client          | requests          |
| Version Control      | Git / GitHub      |

---

## Project Structure

```
├── alembic/
│   ├── env.py
│   ├── README
│   ├── script.py.mako
│   └── versions/
│       └── 70630161b925_create_yellow_taxi_trips_table.py
├── api/
│   ├── deps.py
│   ├── main.py
│   ├── routes/
│   │   ├── analytics.py
│   │   ├── health.py
│   │   └── trips.py
│   └── schemas.py
├── dashboard/
│   ├── api.py
│   ├── app.py
│   ├── pages/
│   │   ├── 1_Overview.py
│   │   ├── 2_Demand_Analytics.py
│   │   ├── 3_Location_Analytics.py
│   │   └── 4_Trip_Details.py
│   └── utils.py
├── data/
│   └── raw/
│       ├── yellow_tripdata_2026-01-sample-100.csv
│       └── yellow_tripdata_2026-01.csv
├── etl/
│   ├── clean.py
│   ├── config.py
│   ├── database.py
│   ├── extract.py
│   ├── load.py
│   ├── models.py
│   ├── pipeline.py
│   ├── transform.py
│   ├── validate.py
│   └── __init__.py
├── main.py
├── pyproject.toml
└── .env
```

### Project Folder Structure Diagram

The following Mermaid diagram documents the repository layout and the location of each major component.

```mermaid
flowchart TB
    root["nyc_taxi_etl/"]
    root --> alembic["alembic/"]
    root --> api["api/"]
    root --> dashboard["dashboard/"]
    root --> data["data/"]
    root --> etl["etl/"]
    root --> mainpy["main.py"]
    root --> pyproject["pyproject.toml"]
    root --> envfile[".env"]

    alembic --> envpy["env.py"]
    alembic --> alembicreadme["README"]
    alembic --> versions["versions/"]
    versions --> versionfile["70630161b925_create_yellow_taxi_trips_table.py"]

    api --> deps["deps.py"]
    api --> mainapp["main.py"]
    api --> routes["routes/"]
    api --> schemas["schemas.py"]
    routes --> analytics["analytics.py"]
    routes --> health["health.py"]
    routes --> trips["trips.py"]

    dashboard --> api_client["api.py"]
    dashboard --> app["app.py"]
    dashboard --> pages["pages/"]
    pages --> page1["1_Overview.py"]
    pages --> page2["2_Demand_Analytics.py"]
    pages --> page3["3_Location_Analytics.py"]
    pages --> page4["4_Trip_Details.py"]
    dashboard --> utils["utils.py"]

    data --> raw["raw/"]
    raw --> sample["yellow_tripdata_2026-01-sample-100.csv"]
    raw --> full["yellow_tripdata_2026-01.csv"]

    etl --> clean["clean.py"]
    etl --> config["config.py"]
    etl --> database["database.py"]
    etl --> extract["extract.py"]
    etl --> load["load.py"]
    etl --> models["models.py"]
    etl --> pipeline["pipeline.py"]
    etl --> transform["transform.py"]
    etl --> validate["validate.py"]
```

### Directory Purpose

- `alembic/` — migration runtime and schema versioning.
- `api/` — FastAPI app wiring, request handlers, and response schemas.
- `dashboard/` — Streamlit application pages and visualization utilities.
- `data/raw/` — input dataset files for development and full pipeline runs.
- `etl/` — extraction, validation, cleaning, transformation, and loading logic.
- `main.py` — CLI entrypoint for running the ETL pipeline.
- `.env` — environment configuration for `DATABASE_URL`.

---

## Database Design

### Tables

- `yellow_taxi_trips`

### Primary Key

- `id` — auto-increment integer primary key.

### Columns

- `vendor_id`
- `tpep_pickup_datetime`
- `tpep_dropoff_datetime`
- `pickup_date`
- `pickup_hour`
- `pickup_day_name`
- `trip_duration_minutes`
- `passenger_count`
- `trip_distance`
- `fare_per_mile`
- `ratecode_id`
- `store_and_fwd_flag`
- `pu_location_id`
- `do_location_id`
- `payment_type`
- `fare_amount`
- `extra`
- `mta_tax`
- `tip_amount`
- `tolls_amount`
- `improvement_surcharge`
- `total_amount`
- `congestion_surcharge`
- `airport_fee`
- `cbd_congestion_fee`

### Relationships

- No foreign key relationships are defined in the current schema.

### Database ER Diagram

The following ER diagram is generated from the SQLAlchemy model in `etl/models.py` and matches the current database schema.

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
        numeric extra
        numeric mta_tax
        numeric tip_amount
        numeric tolls_amount
        numeric improvement_surcharge
        numeric total_amount
        numeric congestion_surcharge
        numeric airport_fee
        numeric cbd_congestion_fee
    }
```

### UML Class Diagram

This UML class diagram represents the SQLAlchemy ORM model used for loading and querying processed trips.

```mermaid
classDiagram
    class YellowTaxiTrip {
        +int id
        +int vendor_id
        +datetime tpep_pickup_datetime
        +datetime tpep_dropoff_datetime
        +date pickup_date
        +int pickup_hour
        +string pickup_day_name
        +Decimal trip_duration_minutes
        +int? passenger_count
        +Decimal? trip_distance
        +Decimal? fare_per_mile
        +int? ratecode_id
        +string? store_and_fwd_flag
        +int pu_location_id
        +int do_location_id
        +int payment_type
        +Decimal? fare_amount
        +Decimal? extra
        +Decimal? mta_tax
        +Decimal? tip_amount
        +Decimal? tolls_amount
        +Decimal? improvement_surcharge
        +Decimal? total_amount
        +Decimal? congestion_surcharge
        +Decimal? airport_fee
        +Decimal? cbd_congestion_fee
    }
```

### Indexes

- Only the primary key index on `id` is implemented.

---

## ETL Pipeline

The ETL workflow is implemented in `etl/pipeline.py` and it runs through five explicit stages.

### ETL Workflow Diagram

The diagram below shows the exact stage sequence used by the ETL pipeline.

```mermaid
flowchart TB
    extraction["Extraction\n(etl/extract.py)"]
    validation["Validation\n(etl/validate.py)"]
    cleaning["Cleaning\n(etl/clean.py)"]
    transformation["Transformation\n(etl/transform.py)"]
    loading["Loading\n(etl/load.py)"]

    extraction --> validation --> cleaning --> transformation --> loading
```

### Data Lifecycle Diagram

Raw data is validated, cleaned, transformed, and loaded into PostgreSQL before being exposed via the API and dashboard.

```mermaid
flowchart TB
    raw["Raw CSV Data"]
    validation["Validation"]
    cleaning["Cleaning"]
    transformation["Transformation"]
    postgres["PostgreSQL"]
    rest["REST API"]
    dashboard["Streamlit Dashboard"]

    raw --> validation --> cleaning --> transformation --> postgres --> rest --> dashboard
```

### Application Workflow Diagram

A typical user request travels from the dashboard through the API to the database and back.

```mermaid
flowchart TB
    user["User"]
    dashboard["Streamlit Dashboard"]
    api["FastAPI Backend"]
    postgres["PostgreSQL"]

    user --> dashboard --> api --> postgres
    postgres --> api --> dashboard --> user
```

### Extraction

- Reads raw CSV data with `etl/extract.py`.
- Uses `pandas.read_csv()` to load the source dataset.
- Returns raw rows exactly as read from the CSV.

### Validation

- Implemented in `etl/validate.py`.
- Verifies required source columns exist.
- Applies discrete validations to detect invalid records.
- Separates trusted rows from quarantined rows.
- Preserves validation metadata for later review.

### Cleaning

- Implemented in `etl/clean.py`.
- Trims leading/trailing whitespace from string columns.
- Normalizes repeated internal whitespace.
- Uppercases safe categorical fields such as `store_and_fwd_flag`.
- Preserves missing values and does not remove duplicates.

### Transformation

- Implemented in `etl/transform.py`.
- Converts datetime and numeric columns.
- Adds time and fare features.
- Renames source columns to snake_case for the target schema.
- Drops ETL metadata before loading.

### Loading

- Implemented in `etl/load.py`.
- Converts each DataFrame row into a `YellowTaxiTrip` ORM object.
- Adds batches of rows to the SQLAlchemy session.
- Commits successful batches and rolls back failed ones.
- Returns the total number of inserted rows.

---

## Validation Rules

Implemented validation logic in `etl/validate.py`:

- **Required columns** — ensures all expected source fields are present.
- **Vendor validation** — accepts only allowed TLC vendor IDs.
- **Pickup datetime validation** — rejects missing pickup timestamps.
- **Dropoff datetime validation** — rejects missing dropoff timestamps.
- **Datetime order validation** — rejects records where dropoff is before pickup.
- **Rate code validation** — rejects invalid `RatecodeID` values.
- **Store-and-forward validation** — rejects values outside `Y`/`N`.
- **Trip distance validation** — rejects negative distances.
- **Location validation** — rejects missing `PULocationID` or `DOLocationID`.
- **Payment type validation** — rejects invalid payment method values.
- **Monetary numeric validation** — rejects non-numeric values in monetary columns.

### Quarantine Logic

- Rows failing validation are separated into `quarantined_df`.
- Trusted rows remain in `trusted_df`.
- Validation warnings are retained with trusted rows; only errors cause quarantine.
- Negative monetary values generate warnings, not automatic failures.

---

## Cleaning

Implemented cleaning behavior in `etl/clean.py`:

- **Missing values** are preserved rather than imputed.
- **Duplicate handling** is not performed in the current pipeline.
- **Standardization** applies consistent whitespace and uppercase normalization.
- **Business rule cleaning** is limited to formatting and text normalization.
- **Type conversion** is not performed in cleaning; it happens in transformation.

---

## Transformation

Implemented feature engineering in `etl/transform.py`:

- `pickup_date` — supports daily aggregations.
- `pickup_hour` — supports hourly demand analysis.
- `pickup_day_name` — supports weekday-based reporting.
- `trip_duration_minutes` — supports trip duration analysis.
- `fare_per_mile` — supports ride efficiency analysis.

These features are created after cleaning and before database loading.

---

## Database Loading

The loading logic in `etl/load.py` includes:

- **Batch loading** — rows are inserted in batches defined by `DEFAULT_BATCH_SIZE`.
- **SQLAlchemy ORM** — uses `YellowTaxiTrip` model instances.
- **Transaction handling** — each batch commit is wrapped in its own transaction.
- **Rollback behavior** — failed batches roll back without affecting previous commits.
- **Commit strategy** — commits after each batch and counts inserted rows.
- **Error handling** — exceptions are re-raised after rollback.

---

## REST API

### API Overview

The API exposes read-only analytics and health endpoints.

### Endpoints

| Method | Path                               | Description                           |
| ------ | ---------------------------------- | ------------------------------------- |
| GET    | `/health`                          | Health check and DB connectivity test |
| GET    | `/trips`                           | Fetch up to 200 processed trips       |
| GET    | `/analytics/trips-per-day`         | Daily trip count summary              |
| GET    | `/analytics/trips-by-payment-type` | Trip count by payment method          |
| GET    | `/analytics/trips-by-vendor`       | Trip count by vendor                  |
| GET    | `/analytics/hourly-demand`         | Trip count by pickup hour             |
| GET    | `/analytics/top-pickup-locations`  | Top pickup location counts            |
| GET    | `/analytics/top-dropoff-locations` | Top dropoff location counts           |

### Request and Response

- `GET /trips` uses `limit` query parameter constrained to `1 <= limit <= 200`.
- Responses are validated with Pydantic models defined in `api/schemas.py`.
- `TripResponse` includes all transformed columns returned by `/trips`.

### Swagger Documentation

- Available via FastAPI at `/docs`.
- Includes OpenAPI metadata for each endpoint and response model.

### FastAPI Request Flow

The FastAPI routes use the `get_db` dependency in `api/deps.py` and query PostgreSQL directly through SQLAlchemy.

```mermaid
sequenceDiagram
    participant Browser
    participant FastAPI
    participant Database

    Browser->>FastAPI: GET /trips or /analytics/*
    FastAPI->>Database: SQLAlchemy session query
    Database-->>FastAPI: query results
    FastAPI-->>Browser: JSON response
```

---

## Streamlit Dashboard

### Overview Page

- KPI cards for total trips, average daily trips, and date range.
- Bar chart for daily trip volume.
- Pie chart for payment method distribution.

### Demand Analytics Page

- Hourly demand area chart.
- Daily trip volume bar chart.
- Peak hour insight card.

### Location Analytics Page

- Top pickup/dropoff location metrics.
- Horizontal bar charts for busiest pickup and dropoff zones.
- Area labels derived from location lookup mappings.

### Trip Details Page

- Sample trip table with `limit=100` from backend.
- Interactive filters for pickup area and payment method.
- Summary KPIs for displayed trips.
- Vendor/provider breakdown chart.

---

## Installation Guide

### Clone repository

```bash
git clone <repository-url>
cd nyc_taxi_etl
```

### Create and activate a virtual environment

```bash
python -m venv .venv
.venv\Scripts\activate
```

### Install dependencies with pip

```bash
python -m pip install --upgrade pip
python -m pip install -e .
```

> Use `pip` for dependency installation and `uvicorn` for running the FastAPI app.

### Configure PostgreSQL

Create a PostgreSQL database and add the connection URL to `.env`:

```env
DATABASE_URL=postgresql+psycopg://postgres:password@localhost:5432/nyc_taxi
```

### Run Alembic migrations

```bash
alembic upgrade head
```

### Place dataset into `data/raw`

- Development dataset: `data/raw/yellow_tripdata_2026-01-sample-100.csv`
- Production dataset: `data/raw/yellow_tripdata_2026-01.csv`

### Run the ETL pipeline

```bash
python main.py
```

### Run the FastAPI backend with uvicorn

```bash
uvicorn api.main:app --reload
```

### Run the Streamlit dashboard

```bash
streamlit run dashboard/app.py
```

### Verify the services

- `http://127.0.0.1:8000/docs`
- `http://127.0.0.1:8000/health`
- Streamlit dashboard URL shown in terminal

---

## Development vs Production Mode

### Development mode

- Uses `data/raw/yellow_tripdata_2026-01-sample-100.csv`
- Purpose: fast debugging, quick validation, and lightweight dashboard testing.
- Benefits: reduces local runtime and supports iterative development.

### Production mode

- Uses `data/raw/yellow_tripdata_2026-01.csv`
- Purpose: full-scale ETL validation against the complete January 2026 dataset.
- Benefits: validates real dataset volume and production behavior.

The project supports both to balance developer productivity with realistic data scale testing.

---

## Running the Project

### ETL Pipeline

```bash
python main.py
```

Expected output includes:

- extraction, validation, cleaning, transformation, and loading stage logs
- raw row counts
- trusted and quarantined row counts
- inserted row count

### FastAPI Backend

```bash
uvicorn api.main:app --reload
```

Expected output includes:

- `Uvicorn running on http://127.0.0.1:8000`
- reload status messages

### Streamlit Dashboard

```bash
streamlit run dashboard/app.py
```

Expected output includes:

- local dashboard URL
- interactive dashboard with four pages and API-backed charts

### Verify endpoints

- `http://127.0.0.1:8000/health`
- `http://127.0.0.1:8000/trips?limit=20`
- `http://127.0.0.1:8000/docs`

---

## Engineering Decisions

- ETL separation creates clear responsibilities and makes debugging easier.
- PostgreSQL is chosen for structured, analytics-friendly relational storage.
- SQLAlchemy ORM provides a declarative model and clean database mapping.
- FastAPI provides lightweight API development and automatic documentation.
- Streamlit enables a fast analytics dashboard without a separate frontend framework.
- Alembic enables repeatable schema migrations.
- The sample dataset enables rapid local development before running the full dataset.

---

## Performance Considerations

The implementation currently prioritizes correctness and maintainability.

### Observations

- Loader uses ORM object instantiation for each row, which is simple but may be less efficient at scale.
- Batch commits are implemented, but raw bulk insert optimization is not yet present.
- The dashboard relies on synchronous HTTP calls to the FastAPI backend.

### Future optimizations

- Bulk insert optimization
- Additional database indexes for analytical query performance
- API caching
- Connection pooling tuning
- Query optimization

These are future opportunities, not current features.

---

## Future Improvements

- Authentication and authorization for API and dashboard access.
- Containerization with Docker for reproducible environments.
- Cloud deployment with managed PostgreSQL.
- CI/CD automation for tests, linting, and migrations.
- Caching and response optimization for analytics endpoints.
- Bulk insert and batch-size tuning.
- Additional analytics endpoints and dashboard features.
- Monitoring and observability.

---

## Lessons Learned

- Staged ETL pipelines improve debugging and make data processing easier to reason about.
- A sample dataset is essential for fast local iteration when working with large taxi data.
- SQLAlchemy ORM simplifies schema mapping but may require tuning for production throughput.
- FastAPI simplifies backend delivery and schema-driven API documentation.
- Streamlit integrates quickly with backend analytics data.
- Balancing development speed and production-scale validation is important for working with real datasets.

---

## License

This project is released under the MIT License.

> TODO: add LICENSE file if needed.

---

## Author

- GitHub: `TODO`
- LinkedIn: `TODO`
- Portfolio: `TODO`
- Email: `TODO`
