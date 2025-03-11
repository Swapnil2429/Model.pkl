import streamlit as st
import requests
import joblib
from io import BytesIO

# Replace this with the raw URL you copied
model_url = "https://raw.githubusercontent.com/Swapnil2429/Model.pkl/main/your_model.pkl"

# Function to download and load the model
def load_model(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Will raise an exception for bad responses (4xx, 5xx)
        
        # Load the model from the downloaded content
        model = joblib.load(BytesIO(response.content))
        return model
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to download the model. Error: {e}")
        return None
    except Exception as e:
        st.error(f"Failed to load the model. Error: {e}")
        return None

# Load the model from GitHub
model = load_model(model_url)

# Check if the model is loaded successfully
if model:
    st.title("IMDb Rating Prediction")
    st.write("Enter the movie details to predict the average IMDb rating.")

    # Input fields for features (adjust according to your model's features)
    genre = st.selectbox("Genre", ["Action", "Comedy", "Drama", "Horror", "Romance"])
    budget = st.number_input("Budget (in millions)", min_value=0, max_value=1000, value=50)
    runtime = st.number_input("Runtime (in minutes)", min_value=0, max_value=300, value=120)

    # Example of how to encode the input features, adjust according to your model
    genre_dict = {"Action": 0, "Comedy": 1, "Drama": 2, "Horror": 3, "Romance": 4}
    genre_value = genre_dict[genre]

    # Prepare the input data for prediction
    input_data = [[genre_value, budget, runtime]]

    # Button to make the prediction
    if st.button("Predict Rating"):
        # Make the prediction using the loaded model
        prediction = model.predict(input_data)
        
        # Display the result
        st.write(f"Predicted IMDb Rating: {prediction[0]:.2f}")
