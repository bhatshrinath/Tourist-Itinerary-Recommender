import random

poi_types = [
    "tourism",
    "amenity",
    "leisure",
    "shop",
    "natural",
    "transport",
    "cultural",
]

tourist_categories_dict = {
    "Food": ["bakery", "fast_food", "restaurant", "cafe", "food_court"],
    "Accommodation": ["hotel", "guest_house", "hostel", "apartment", "motel", "resort"],
    "Attractions": [
        "attraction",
        "library",
        "art",
        "gallery",
        "aquarium",
        "theatre",
        "events_venue",
        "museum",
        "park",
        "playground",
        "golf_course",
        "theme_park",
        "nature_reserve",
        "garden",
        "escape_game",
        "amusement_arcade",
        "place_of_worship",
        "monastery",
        "handicraft",
        "artwork",
        "pottery",
        "antiques",
        "grassland",
        "dog_park",
        "horse_riding",
        "beach",
    ],
}

email = "pooja" + str(random.randint(1, 1000)) + "@gmail.com"

train = False


class TimeGoogleDataFetch:
    def __init__(self, min_distance, max_distance):
        self.min_distance = min_distance
        self.max_distance = max_distance
        self.time_google_data_fetch = self.generate_time_google_data_fetch()

    def generate_time_google_data_fetch(self):
        return random.randint(self.min_distance, self.max_distance)


class CostTripAdvisorDataFetch:
    def __init__(self):
        self.min_cost = 10
        self.max_cost = 20
        self.cost_trip_advisor_data_fetch = self.generate_cost_trip_advisor_data_fetch()

    def generate_cost_trip_advisor_data_fetch(self):
        return random.randint(self.min_cost, self.max_cost)
