import streamlit as st
import requests
import pandas as pd
import folium
from streamlit_folium import st_folium
from datetime import timedelta, date
from config import poi_types, tourist_categories_dict, email, train
from user_interface import add_custom_css
from utils import determine_transport_mode, calculate_travel_time
from data_fetch import fetch_google_travel_time, fetch_trip_advisor_cost
from recommender import train_models

# add custom CSS to the app
add_custom_css()


# Title and Intro
st.title("🌍 Travel Planner for Tourists")

# Info Section with Expander
with st.expander("ℹ️ About This App", expanded=True):
    st.markdown(
        """
        Welcome to the **Travel Planner for Tourists App**! 🌍  

        **What do you do when you need a break from your mundane life?**  
        You go on a Vacation! Everybody loves going on vacations, but planning one can be tedious.  
        Our motivation is to reduce the time spent planning vacations and help travelers spend more time enjoying them.

        **Why Use This Tool?**
        This app generates a *Tailor-Made Travel Plan* based on:  
        - Your destination, travel dates, and budget.  
        - Personalized recommendations for **places to stay**, **things to do**, and **places to eat**.

        With this tool, you’ll have everything you need to make your vacation truly memorable, without the hassle of browsing hundreds of websites.
        """
    )

st.markdown("")
st.markdown("---")

# Sidebar for user inputs
st.sidebar.header("Customize Your Search")
destination = st.sidebar.text_input("Destination (e.g., Paris):", "Paris")
radius = st.sidebar.slider("Search Radius (kms):", 1, 20, 1) * 1000  # Convert to meters

# Button to Filter by Category
st.sidebar.header("Filter by Points of Interest Categories")

# Main categories Food, Accommodation, Attractions
main_categories = list(tourist_categories_dict.keys())

# Subcategories in Accommodation main category
available_subcategories_accommodation = tourist_categories_dict["Accommodation"]
selected_subcategories_accommodation = st.sidebar.multiselect(
    "Choose Accommodation Options:",
    options=["Select All"] + available_subcategories_accommodation,
    default=["Select All"],
)
if "Select All" in selected_subcategories_accommodation:
    selected_subcategories_accommodation = available_subcategories_accommodation
selected_subcategories_accommodation = [
    selected_subcategories_accommodation[i]
    for i in range(len(selected_subcategories_accommodation))
]

# Subcategories in Food main category
available_subcategories_food = tourist_categories_dict["Food"]
selected_subcategories_food = st.sidebar.multiselect(
    "Choose Food Options:",
    options=["Select All"] + available_subcategories_food,
    default=["Select All"],
)
if "Select All" in selected_subcategories_food:
    selected_subcategories_food = available_subcategories_food
selected_subcategories_food = [
    selected_subcategories_food[i] for i in range(len(selected_subcategories_food))
]

# Subcategories in Attractions main category
available_subcategories_attractions = tourist_categories_dict["Attractions"]
selected_subcategories_attractions = st.sidebar.multiselect(
    "Choose Attractions Options:",
    options=["Select All"] + available_subcategories_attractions,
    default=["Select All"],
)
if "Select All" in selected_subcategories_attractions:
    selected_subcategories_attractions = available_subcategories_attractions
selected_subcategories_attractions = [
    selected_subcategories_attractions[i]
    for i in range(len(selected_subcategories_attractions))
]

fetch_button = st.sidebar.button("Get Recommendations")

# Initialize session state
if "places_df" not in st.session_state:
    st.session_state.places_df = None
if "lat" not in st.session_state or "lon" not in st.session_state:
    st.session_state.lat = None
    st.session_state.lon = None

# Step 3: Fetch Coordinates with Nominatim API
if fetch_button:
    with st.spinner("Fetching Location..."):
        nominatim_url = "https://nominatim.openstreetmap.org/search"
        params = {"q": destination, "format": "json", "limit": 1}
        headers = {"User-Agent": f"ItineraryPlanner/1.0 ({email})"}

        try:
            response = requests.get(
                nominatim_url, params=params, headers=headers, timeout=100
            )
            if response.status_code == 200:
                results = response.json()
                if results:
                    location = results[0]
                    st.session_state.lat = float(location["lat"])
                    st.session_state.lon = float(location["lon"])
                    st.write(
                        f"Found {destination} at Latitude: {round(st.session_state.lat, 3)} and Longitude: {round(st.session_state.lon, 3)}"
                    )
                    st.success("Location Fetched Successfully!")
                else:
                    st.error(
                        "No results returned from Nominatim. Please check your input."
                    )
            else:
                st.error(
                    f"Failed to fetch location data. HTTP Status: {response.status_code}"
                )
        except requests.exceptions.RequestException as e:
            st.error(f"An error occurred while fetching location data: {e}")

    # Fetch Points of Interest with Overpass API
    if st.session_state.lat is not None and st.session_state.lon is not None:
        with st.spinner("Fetching Points of Interests..."):
            overpass_url = "https://overpass-api.de/api/interpreter"

            # Construct query for all POI types
            query = f"""
            [out:json];
            (
            """
            for poi_type in poi_types:
                query += f'node["{poi_type}"](around:{radius},{st.session_state.lat},{st.session_state.lon});'
                query += f'way["{poi_type}"](around:{radius},{st.session_state.lat},{st.session_state.lon});'
                query += f'relation["{poi_type}"](around:{radius},{st.session_state.lat},{st.session_state.lon});'
            query += """
            );
            out center;
            """

            try:
                response = requests.get(
                    overpass_url, params={"data": query}, timeout=30
                )
                if response.status_code == 200:
                    data = response.json().get("elements", [])
                    if data:
                        places = []
                        for element in data:
                            tags = element.get("tags", {})
                            name = tags.get("name", "Unnamed Location")
                            category = (
                                tags.get("tourism")
                                or tags.get("amenity")
                                or tags.get("leisure")
                                or tags.get("shop")
                                or tags.get("natural")
                                or tags.get("transport")
                                or tags.get("cultural")
                                or "Unknown Category"
                            )
                            lat = element.get(
                                "lat", element.get("center", {}).get("lat")
                            )
                            lon = element.get(
                                "lon", element.get("center", {}).get("lon")
                            )

                            if name and lat and lon:
                                places.append(
                                    {
                                        "Name": name,
                                        "Category": category,
                                        "Latitude": lat,
                                        "Longitude": lon,
                                    }
                                )

                        places_data = pd.DataFrame(places)
                        st.session_state.places_df = places_data.dropna(
                            subset=["Latitude", "Longitude"]
                        )

                        # remove ""Unknown Category" from the category column, "Unknown Location" from the name column
                        st.session_state.places_df = st.session_state.places_df[
                            st.session_state.places_df["Category"] != "Unknown Category"
                        ]
                        st.session_state.places_df = st.session_state.places_df[
                            st.session_state.places_df["Name"] != "Unnamed Location"
                        ]

                        # Maximum of 20 in each category
                        st.session_state.places_df = (
                            st.session_state.places_df.groupby("Category")
                            .head(10)
                            .reset_index(drop=True)
                        )
                        st.success("Points of Interests Fetched Successfully!")
                    else:
                        st.error(
                            "No points of interest found for the given type and radius."
                        )
                else:
                    st.error(
                        f"Failed to fetch POI data from Overpass API. HTTP Status: {response.status_code}"
                    )
            except requests.exceptions.RequestException as e:
                st.error(f"An error occurred while fetching POI data: {e}")

if st.session_state.places_df is not None:

    st.write("## Recommendations")
    # Filter the DataFrame based on selected categories
    filtered_df = st.session_state.places_df
    filtered_df = filtered_df[
        filtered_df["Category"].isin(
            selected_subcategories_food
            + selected_subcategories_accommodation
            + selected_subcategories_attractions
        )
    ].reset_index(drop=True)
    filtered_df["Place Category"] = (
        filtered_df["Category"].str.replace("_", " ").str.title()
    )
    st.dataframe(filtered_df.drop(columns={"Category"}))
    filtered_df = filtered_df.drop(columns={"Place Category"})

    # Display filtered data
    if not filtered_df.empty:

        # Update the session state with the filtered DataFrame
        st.session_state.places_df = filtered_df
        sorted_places = filtered_df.copy()

        st.markdown("")
        st.markdown("---")

        # Display insights about the data
        st.markdown("## Insights from Recommendations")

        # Display selected categories (remove "_" and make it capital)
        selected_categories = st.session_state.places_df["Category"].unique()
        selected_categories = [
            cat.replace("_", " ").title() for cat in selected_categories
        ]
        st.markdown("#### Selected Categories")
        st.write(", ".join(selected_categories))

        # Display total number of places found
        st.markdown("#### Total Number of Places Found")
        st.write(len(st.session_state.places_df))

        st.markdown("")
        st.markdown("---")

        # Map Visualization
        st.header("Explore Places on the Map")
        map_center = [filtered_df["Latitude"].mean(), filtered_df["Longitude"].mean()]
        location_map = folium.Map(location=map_center, zoom_start=13)

        for _, row in filtered_df.iterrows():
            folium.Marker(
                location=[row["Latitude"], row["Longitude"]],
                popup=f"{row['Name']} ({row['Category']})",
            ).add_to(location_map)

        st_folium(location_map, width=700, height=500)

        st.markdown("")
        st.markdown("---")

        # Start itinerary planning
        st.header("🗓️ Detailed Trip Itinerary Planning")

        # Validate location data
        if st.session_state.lat is None or st.session_state.lon is None:
            st.warning("Please fetch location data before planning your itinerary.")
        else:
            st.sidebar.header("Itinerary Configuration")

            # User Inputs
            budget = st.sidebar.number_input(
                "Budget (in Rupees):",
                min_value=10000,
                max_value=300000,
                value=50000,
                step=10000,
            )
            travel_dates = st.sidebar.date_input(
                "Travel Dates:",
                [],
                min_value=date.today(),  # Restrict to dates starting from today
            )

            itinerary_button = st.sidebar.button("Get Recommended Itinerary")

            if itinerary_button:
                # Validate travel dates
                if len(travel_dates) != 2:
                    st.error("Please select a start and end date for your trip.")
                else:
                    trip_start, trip_end = travel_dates
                    days = (trip_end - trip_start).days
                    if days < 1:
                        st.error("Travel dates must span at least one full day.")
                    else:
                        # Display trip information at the start
                        st.write("")
                        st.write("#### Trip Details")
                        st.info(f"🗓️ **Trip Start Date**: {trip_start}")
                        st.info(f"🗓️ **Trip End Date**: {trip_end}")
                        st.info(f"📆 **Number of Days**: {days}")
                        st.info(f"💰 **Budget**: ₹{budget}")
                        st.markdown("---")

                        # training models in recommender.py to get the most popular, highly rated and
                        # recommended places considering the user's preferences (especially budget and travel dates)
                        # 1. Autoencoder Model, 2. ALS Model, 3. K-Means Clustering Model
                        train_models(
                            rbm_units=(5, 3),
                            als_params=(10, 10, 0.1),
                            kmeans_clusters=3,
                            knn_neighbors=5,
                            train=train,
                        )

                        # Add distance calculation
                        sorted_places["Distance"] = sorted_places.apply(
                            lambda row: (
                                (row["Latitude"] - st.session_state.lat) ** 2
                                + (row["Longitude"] - st.session_state.lon) ** 2
                            )
                            ** 0.5,
                            axis=1,
                        )

                        sorted_places["Distance_km"] = (
                            sorted_places["Distance"] * 111
                        )  # Approx conversion to km
                        sorted_places = sorted_places.sort_values("Distance_km")

                        # Select place to stay
                        try:
                            stay_place = sorted_places[
                                sorted_places["Category"].str.contains(
                                    "hotel|guest_house|hostel|apartment|motel|resort|stay",
                                    case=False,
                                    na=False,
                                )
                            ].iloc[0]

                            # Display stay details
                            st.write(
                                f"🏨 **Stay**: {stay_place['Name']} ({stay_place['Category'].replace('_', ' ').title()})"
                            )
                            st.write(
                                f"📍 Location: {round(stay_place['Latitude'], 3)}, {round(stay_place['Longitude'], 3)}"
                            )
                            st.write(f"📆 Number Of Days: {days}")
                            st.write(
                                f"💵 Cost Per Day: ₹{round(budget*(fetch_trip_advisor_cost()/(days*100)),0)}"
                            )
                            st.markdown("---")
                        except:
                            # Display a warning or handle gracefully
                            st.warning(
                                "No suitable stay places found for the given filters."
                            )
                            pass

                try:
                    # Generate itinerary for the trip
                    places_per_day = min(
                        5, max(1, len(sorted_places) // days)
                    )  # 5 places/day max

                    visited_indices = set()  # Track visited places

                    for day in range(1, days + 1):
                        st.write(
                            f"#### Day {day}: {trip_start + timedelta(days=day - 1)}"
                        )

                        # Filter out places already visited
                        available_places = sorted_places[
                            ~sorted_places.index.isin(visited_indices)
                        ]

                        # Select attractions for the day
                        attractions = available_places[
                            (
                                available_places["Category"].str.contains(
                                    "beach|attraction|library|art|aquarium|theatre|events_venue|museum|park|golf_course|theme_park|nature_reserve|garden|escape_game|amusement_arcade|place_of_worship|monastery|handicraft|artwork|pottery|antiques|grassland|dog_park|horse_riding",
                                    case=False,
                                    na=False,
                                )
                            )
                            & (
                                ~available_places["Category"].str.contains(
                                    "apartment", case=False, na=False
                                )
                            )
                        ].head(places_per_day)

                        if attractions.empty:
                            st.write("⚠️ Not enough attractions for this day.")
                            break

                        # Add the selected attractions to the visited set
                        visited_indices.update(attractions.index)

                        # Display places for the day
                        for _, attraction in attractions.iterrows():
                            distance_km = attraction["Distance_km"]
                            travel_time = calculate_travel_time(distance_km)
                            transport_mode = determine_transport_mode(distance_km)

                            st.write(
                                f"🎯 **Attraction**: {attraction['Name']} ({attraction['Category'].replace('_', ' ').title()})"
                            )
                            st.write(
                                f"📍 Location: {round(attraction['Latitude'], 3)}, {round(attraction['Longitude'], 3)}"
                            )
                            st.write(f"🛤️ Distance: {distance_km:.2f} km")
                            st.write(f"⏳ Travel Time: {travel_time} minutes")
                            st.write(f"🚶 Recommended Mode: {transport_mode}")
                            st.write(
                                f"🕒 Estimated Visit Duration: {fetch_google_travel_time(min_distance=30, max_distance=120)} minutes"
                            )
                            st.markdown("---")

                        # Select additional POIs
                        extra_places = available_places[
                            ~available_places.index.isin(visited_indices)
                        ].head(
                            3
                        )  # 3 extra places max
                        if not extra_places.empty:
                            st.markdown(
                                "##### 📌 Additional Places of Interest You Can Visit on the Way"
                            )
                            for _, extra in extra_places.iterrows():
                                st.write(
                                    f"🗺️ **{extra['Name']}** ({extra['Category'].replace('_', ' ').title()})"
                                )
                                st.write(
                                    f"📍 Location: {round(extra['Latitude'], 3)}, {round(extra['Longitude'], 3)}"
                                )
                                st.write(
                                    f"🛤️ Distance: {round(extra['Distance_km']/2, 2)} km"
                                )
                                st.markdown("---")

                            visited_indices.update(extra_places.index)

                        # Filter meal locations
                        meal_places = available_places[
                            available_places["Category"].str.contains(
                                "bakery|fast_food|restaurant|cafe|food_court|food|bar|pub|club",
                                case=False,
                                na=False,
                            )
                        ]

                        # Ensure there are enough meal places to avoid index errors
                        if len(meal_places) >= 3:
                            # Assign meal places
                            breakfast_place = meal_places.iloc[0]
                            lunch_place = meal_places.iloc[1]
                            dinner_place = meal_places.iloc[2]

                            # Display meal locations in tabs
                            tabs = st.tabs(["🍳 Breakfast", "🍴 Lunch", "🍽️ Dinner"])

                            with tabs[0]:  # Breakfast
                                st.write(
                                    f"🍽️ **Breakfast**: {breakfast_place['Name']} ({breakfast_place['Category'].replace('_', ' ').title()})"
                                )
                                st.write(
                                    f"📍 Location: {round(breakfast_place['Latitude'], 3)}, {round(breakfast_place['Longitude'], 3)}"
                                )
                                st.write(
                                    f"🛤️ Distance: {round(breakfast_place['Distance_km'], 2)} km"
                                )
                                st.write(
                                    f"⏳ Travel Time: {calculate_travel_time(breakfast_place['Distance_km'])} minutes"
                                )
                                st.markdown("---")

                            with tabs[1]:  # Lunch
                                st.write(
                                    f"🍽️ **Lunch**: {lunch_place['Name']} ({lunch_place['Category'].replace('_', ' ').title()})"
                                )
                                st.write(
                                    f"📍 Location: {round(lunch_place['Latitude'], 3)}, {round(lunch_place['Longitude'], 3)}"
                                )
                                st.write(
                                    f"🛤️ Distance: {round(lunch_place['Distance_km'], 2)} km"
                                )
                                st.write(
                                    f"⏳ Travel Time: {calculate_travel_time(lunch_place['Distance_km'])} minutes"
                                )
                                st.markdown("---")

                            with tabs[2]:  # Dinner
                                st.write(
                                    f"🍽️ **Dinner**: {dinner_place['Name']} ({dinner_place['Category'].replace('_', ' ').title()})"
                                )
                                st.write(
                                    f"📍 Location: {round(dinner_place['Latitude'], 3)}, {round(dinner_place['Longitude'], 3)}"
                                )
                                st.write(
                                    f"🛤️ Distance: {round(dinner_place['Distance_km'], 2)} km"
                                )
                                st.write(
                                    f"⏳ Travel Time: {calculate_travel_time(dinner_place['Distance_km'])} minutes"
                                )
                                st.markdown("---")

                            # Mark the meal places as visited
                            visited_indices.update(
                                [
                                    breakfast_place.name,
                                    lunch_place.name,
                                    dinner_place.name,
                                ]
                            )

                        elif len(meal_places) > 0:
                            # Fallback: Only one or two meal places available
                            st.warning(
                                "Not enough meal locations for breakfast, lunch, and dinner. Showing available meal options below!"
                            )

                            for i, place in enumerate(meal_places.itertuples()):
                                meal_type = ["Breakfast", "Lunch", "Dinner"][i]
                                st.write(
                                    f"🍽️ **{meal_type}**: {place.Name} ({place.Category.replace('_', ' ').title()})"
                                )
                                st.write(
                                    f"📍 Location: {round(place.Latitude, 3)}, {round(place.Longitude, 3)}"
                                )
                                st.write(
                                    f"🛤️ Distance: {round(place.Distance_km, 2)} km"
                                )
                                st.write(
                                    f"⏳ Travel Time: {calculate_travel_time(place.Distance_km)} minutes"
                                )
                                st.markdown("")

                                # Mark this place as visited
                                visited_indices.add(place.Index)

                            st.markdown("---")

                        else:
                            st.error(
                                "Not enough meal locations available to recommend breakfast, lunch, or dinner."
                            )

                except IndexError as e:
                    st.error(
                        f"Not enough data to plan the trip for {days} days. Please adjust your filters or data."
                    )
                except Exception as e:
                    st.error(f"An error occurred while generating the itinerary: {e}")
            else:
                st.warning(
                    "No itinerary to show yet. Start by entering budget, travel dates and 'Get Recommended Itinerary'."
                )

    # Download Recommendations Section
    st.header("Download All Places Of Interest")

    # Final Data Display
    with st.expander("ℹ️ All Places Of Interest", expanded=False):
        st.markdown("##### Detailed List")
        if "Distance" in sorted_places.columns:
            sorted_places = sorted_places.drop(columns=["Distance"])
        sorted_places["Place Category"] = (
            sorted_places["Category"].str.replace("_", " ").str.title()
        )
        st.dataframe(sorted_places.drop(columns={"Category"}).reset_index(drop=True))
        sorted_places = sorted_places.drop(columns={"Place Category"})

    csv = filtered_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download as CSV",
        data=csv,
        file_name="trip_recommendations.csv",
        mime="text/csv",
    )

else:
    st.warning(
        "No places to show yet. Start by entering a destination and clicking 'Get Recommendations'."
    )
