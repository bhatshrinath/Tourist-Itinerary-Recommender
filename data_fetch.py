from config import TimeGoogleDataFetch, CostTripAdvisorDataFetch


def fetch_google_travel_time(min_distance, max_distance):
    """
    Fetch travel time from Google Maps API for a between
    `min_distance` and `max_distance` kilometers.

    Parameters:
        min_distance (int): The minimum distance in kilometers.

        max_distance (int): The maximum distance in kilometers.

    Returns:

        int: Travel time in minutes.
    """
    config = TimeGoogleDataFetch(min_distance, max_distance)
    return config.time_google_data_fetch


def fetch_trip_advisor_cost():
    """
    Fetch cost from TripAdvisor API for a given trip.

    Parameters:
        None

    Returns:
        int: Cost in dollars.
    """
    config = CostTripAdvisorDataFetch()
    return config.cost_trip_advisor_data_fetch
