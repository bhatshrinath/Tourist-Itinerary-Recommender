# Recommendation Systems for Tourists

## Overview
The "Recommendation Systems for Tourists" project simplifies vacation planning by providing personalized recommendations for accommodations, eateries, and attractions tailored to user preferences. Users can input travel details such as location, budget, dates, and preferred amenities, resulting in a detailed, customized itinerary that enhances the travel experience.

---

## Features
1. **Vacation Planning Time Reduction**
   - Offers tailor-made travel itineraries to minimize time spent on research.

2. **Personalized Recommendations**
   - Users can customize plans based on:
     - Location
     - Budget
     - Travel dates
     - Hotel amenities
     - Attraction categories
     - Restaurant cuisine preferences

3. **Comprehensive Itineraries**
   - **Hotels**: Suggests five hotels matching the user’s requirements.
   - **Attractions**: Recommends two attractions per day (morning and evening).
   - **Restaurants**: Suggests restaurants for breakfast, lunch, and dinner daily.

4. **Advanced Algorithms**
   - Utilizes three recommendation techniques:
     - **Restricted Boltzmann Machine (RBM)**: Deep learning-based collaborative filtering.
     - **Matrix Factorization with Alternating Least Squares (ALS)**: Scalable matrix factorization.
     - **Hybrid Model**: Combines K-Means clustering and K-Nearest Neighbors (KNN).

5. **Data-Driven Decision Making**
   - Recommendations based on data from TripAdvisor, Yelp, and other sources, ensuring relevance and accuracy.

6. **Interactive User Interface**
   - Allows effortless profile creation and parameter selection with results presented via interactive widgets.

---

## Data Pipeline
1. **Data Collection**
   - Scraped hotel and attraction data from TripAdvisor.
   - Utilized Yelp dataset for restaurant data.
   - Collected 35,000 hotels, 3,500 attractions, and 12,000 restaurants with millions of reviews.

2. **Data Cleaning and Integration**
   - Handled missing data using hierarchical averages and geolocation tools.
   - Extracted restaurant-specific data from Yelp.
   - Applied sentiment analysis using VADER and Google Translate for multilingual reviews.

3. **Exploratory Data Analysis (EDA)**
   - Analyzed data distributions to optimize user profiling and model features.

4. **Recommendation Models**
   - **RBM** for attractions.
   - **ALS** for hotels.
   - **Hybrid Model** for restaurants combining K-Means and KNN.

5. **Integration**
   - Merged recommendations into a cohesive travel plan delivered via a Jupyter Notebook interface.

---

## Technology Stack
- **Data Collection**: lxml, requests, GeoPy, Google API
- **Data Processing**: Pandas, Spark
- **Model Training**: TensorFlow, Spark MLlib, Scikit-learn
- **Sentiment Analysis**: NLTK, VADER, Google Translate API
- **Visualization**: Plotly, Tableau, Seaborn
- **User Interface**: IPython, ipywidgets, HTML/CSS

---

## Challenges
1. **Data Availability**
   - Lack of comprehensive datasets required extensive web scraping and cleaning.
2. **Integration**
   - Combining outputs from three recommendation models into a unified travel plan.
3. **Cold-Start Problem**
   - Addressed using user profiling techniques for new users.
4. **Scalability**
   - Models were optimized for performance and scalability to handle large datasets.

---

## Results
- Provided personalized travel plans with:
  - Hotel options matching user amenities.
  - Attraction recommendations based on time and proximity.
  - Restaurant recommendations tailored to cuisine preferences.
- Delivered user-friendly outputs through an interactive Jupyter Notebook.

---

## Future Work
1. **Global Expansion**
   - Extend recommendations to destinations worldwide.
2. **Improved UI/UX**
   - Develop a web application for better user interaction.
3. **User Segmentation**
   - Tailor plans based on group types (e.g., family, solo travelers).
4. **Enhanced Models**
   - Explore advanced algorithms like Deep Belief Networks and Auto-Encoders.

---

## How to Run
1. Clone the repository.
2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the Jupyter Notebook to input travel preferences and view recommendations:
   ```bash
   jupyter notebook
   ```

---
