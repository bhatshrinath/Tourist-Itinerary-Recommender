from data_fetch import fetch_google_travel_time


# Function to fetch travel time based on distance
def calculate_travel_time(distance_km):
    """
    Calculate the travel time based on the distance in kilometers.

    This function uses google maps API to fetch the travel time for different
    distances and modes of transport. The estimated travel time is then returned
    as a string in hours and minutes.

    Logic:
    - Time fetched from Google Maps API for different distances and modes of transport.
    - Walking for distances less than 1 km.
    - Bicycle or Taxi for distances less than 3 km.
    - Taxi or Public Transport for distances less than 10 km.
    - Intercity Bus/Train for longer distances.

    Parameters:
        distance_km (float): The distance in kilometers.

    Returns:
        str: A string representing the estimated travel time.
    """
    if distance_km < 1:
        return fetch_google_travel_time(
            min_distance=5, max_distance=15
        )  # Walking time in minutes
    elif distance_km < 3:
        return fetch_google_travel_time(
            min_distance=10, max_distance=30
        )  # Short taxi/bike rides in minutes
    elif distance_km < 10:
        return fetch_google_travel_time(
            min_distance=20, max_distance=60
        )  # Longer taxi/public transport times
    elif distance_km < 30:
        return fetch_google_travel_time(
            min_distance=60, max_distance=120
        )  # Public transport or intercity travel in minutes
    elif distance_km < 100:
        return fetch_google_travel_time(min_distance=120, max_distance=180)
    # Longer intercity travel times in minutes
    elif distance_km < 200:
        return fetch_google_travel_time(min_distance=180, max_distance=240)
    else:  # Very long distances, consider flying or long-distance trains
        # This is a placeholder; actual implementation may vary based on the API used.
        # For example, you might want to fetch flight times or long-distance train times.
        # Here we assume a long-distance travel time of 240 minutes (4 hours).
        # You can adjust this based on your requirements or API capabilities.
        return fetch_google_travel_time(min_distance=240, max_distance=300)


# Function to determine transport mode
def determine_transport_mode(distance_km):
    """
    Determine the recommended mode of transport based on the distance in kilometers.

    Logic:
    - Walking for distances less than 1 km.
    - Bicycle or Taxi for distances less than 3 km.
    - Taxi or Public Transport for distances less than 10 km.
    - Intercity Bus/Train for longer distances.

    Parameters:
        distance_km (float): The distance in kilometers.

    Returns:
        str: A string representing the recommended mode of transport.
    """
    if distance_km < 1:
        return "Walking"
    elif distance_km < 3:
        return "Bicycle or Taxi"
    elif distance_km < 10:
        return "Taxi or Public Transport"
    elif distance_km < 30:
        return "Public Transport or Intercity Travel"
    elif distance_km < 100:
        return "Intercity Bus/Train"
    elif distance_km < 200:
        return "Intercity Bus/Train"
    else:  # Very long distances, consider flying or long-distance trains
        # This is a placeholder; actual implementation may vary based on the API used.
        # For example, you might want to fetch flight times or long-distance train times.
        # Here we assume a long-distance travel time of 240 minutes (4 hours).
        # You can adjust this based on your requirements or API capabilities.
        return "Long-Distance Travel Mode (Flight)"
