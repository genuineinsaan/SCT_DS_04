# To run this code at first go to link "https://www.kaggle.com/code/harshalbhamare/us-accident-eda" and download the file "US_Accidents_Dec21_updated.csv"
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder
import folium
from folium.plugins import HeatMap

# Load the dataset
file_path = "US_Accidents_Dec21_updated.csv"  # Ensure this file is in your working directory
data = pd.read_csv(file_path)

# Display basic information about the dataset
print("Dataset Info:")
print(data.info())
print("\nDataset Summary:")
print(data.describe())

# Step 1: Data Preprocessing
print("\nChecking for missing values:")
print(data.isnull().sum())

# Drop rows with missing values in essential columns
required_columns = ["Severity", "Start_Time", "Weather_Condition", "Start_Lat", "Start_Lng"]
data = data.dropna(subset=required_columns)

# Encode categorical variables if necessary
label_encoder = LabelEncoder()
data["Weather_Condition_Encoded"] = label_encoder.fit_transform(data["Weather_Condition"])

# Step 2: Analyze Patterns
# Accidents by time of day
data["Start_Hour"] = pd.to_datetime(data["Start_Time"], errors='coerce').dt.hour
data = data.dropna(subset=["Start_Hour"])  # Drop invalid rows after datetime conversion
hourly_accidents = data["Start_Hour"].value_counts().sort_index()

# Accidents by weather condition
weather_accidents = data["Weather_Condition"].value_counts().head(10)

# Step 3: Visualizations
# Accidents by time of day
plt.figure(figsize=(10, 6))
sns.barplot(x=hourly_accidents.index, y=hourly_accidents.values, palette="viridis", hue=None)
plt.title("Number of Accidents by Hour of the Day")
plt.xlabel("Hour of the Day")
plt.ylabel("Number of Accidents")
plt.xticks(range(0, 24))
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.show()

# Top 10 weather conditions contributing to accidents
plt.figure(figsize=(12, 6))
sns.barplot(x=weather_accidents.values, y=weather_accidents.index, palette="plasma", hue=None)
plt.title("Top 10 Weather Conditions Contributing to Accidents")
plt.xlabel("Number of Accidents")
plt.ylabel("Weather Condition")
plt.show()

# Step 4: Accident Hotspots Visualization (Geospatial Analysis)
# Sample data for visualization (reduce size for performance)
sample_data = data.sample(n=5000)

# Create a map
map_center = [sample_data["Start_Lat"].mean(), sample_data["Start_Lng"].mean()]
accident_map = folium.Map(location=map_center, zoom_start=5)

# Add heatmap layer
heat_data = list(zip(sample_data["Start_Lat"], sample_data["Start_Lng"]))
HeatMap(heat_data).add_to(accident_map)

# Save and display the map
accident_map.save("accident_hotspots.html")
print("Heatmap saved as 'accident_hotspots.html'. Open it in your browser to view.")

# Step 5: Conclusions
print("\nAnalysis Complete!")
