from fastapi import FastAPI

from api.routes.health import health_check
from api.routes.trips import get_trips
from api.schemas import HealthResponse, TripResponse


app = FastAPI(
    title="NYC Yellow Taxi ETL API",
    description="Read-only API for processed NYC Yellow Taxi trip data.",
    version="0.1.0",
)

app.add_api_route(
    "/health",
    health_check,
    methods=["GET"],
    response_model=HealthResponse,
    tags=["health"],
)
app.add_api_route(
    "/trips",
    get_trips,
    methods=["GET"],
    response_model=list[TripResponse],
    tags=["trips"],
)
