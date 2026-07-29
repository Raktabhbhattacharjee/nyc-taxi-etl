from fastapi import FastAPI

from api.routes.analytics import (
    get_hourly_demand,
    get_top_dropoff_locations,
    get_top_pickup_locations,
    get_trips_by_payment_type,
    get_trips_by_vendor,
    get_trips_per_day,
)
from api.routes.health import health_check
from api.routes.trips import get_trips
from api.schemas import (
    HealthResponse,
    HourlyDemandResponse,
    TopDropoffLocationResponse,
    TopPickupLocationResponse,
    TripResponse,
    TripsByPaymentTypeResponse,
    TripsByVendorResponse,
    TripsPerDayResponse,
)


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
app.add_api_route(
    "/analytics/trips-per-day",
    get_trips_per_day,
    methods=["GET"],
    response_model=list[TripsPerDayResponse],
    tags=["analytics"],
)
app.add_api_route(
    "/analytics/trips-by-payment-type",
    get_trips_by_payment_type,
    methods=["GET"],
    response_model=list[TripsByPaymentTypeResponse],
    tags=["analytics"],
)
app.add_api_route(
    "/analytics/trips-by-vendor",
    get_trips_by_vendor,
    methods=["GET"],
    response_model=list[TripsByVendorResponse],
    tags=["analytics"],
)
app.add_api_route(
    "/analytics/hourly-demand",
    get_hourly_demand,
    methods=["GET"],
    response_model=list[HourlyDemandResponse],
    tags=["analytics"],
)
app.add_api_route(
    "/analytics/top-pickup-locations",
    get_top_pickup_locations,
    methods=["GET"],
    response_model=list[TopPickupLocationResponse],
    tags=["analytics"],
)
app.add_api_route(
    "/analytics/top-dropoff-locations",
    get_top_dropoff_locations,
    methods=["GET"],
    response_model=list[TopDropoffLocationResponse],
    tags=["analytics"],
)
