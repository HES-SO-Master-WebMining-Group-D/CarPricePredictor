# 🚗 Car Price Predictor
![Car Price Predictor](UI.png "User Interface")

## **Overview**
Car Price Predictor allows users to estimate vehicle prices using a machine learning model trained on web data, helping buyers and sellers make informed decisions.
It is a simple end-to-end data science project consisting of:
- **Data Collection**: Scraping data from autoscout24.com using Scrapy
- **Data Cleaning**: Cleaning the scraped data to remove missing values and outliers
- **Data Exploration**: Exploring the cleaned data using statistics and visualizations
- **Model Building**: Comparing different regression models to predict car prices and selecting the best one, then tuning the hyperparameters
- **Model Deployment**: Deploying the model using FastAPI
- **User Interface**: Creating a simple user interface using Dash to interact with the deployed model and access autoscoot24.com without having to re-enter the car details

## Installation and Usage
1. Install the required packages using the following command:
```bash
pip install -r requirements.txt
```
2. Run the following command to start the FastAPI server:
```bash
python -m uvicorn src.app:app --host 0.0.0.0 --port 8000
```
3. Launch the Dash app by running the following command:
```bash
python src/main_ui.py
```
4. Open the following URL in your browser to access the user interface: [//http://127.0.0.1:8050]

## Collect new data
1. Run the following command to scrape new data from autoscout24.com:
```bash
cd AutoscootScraper/autoscout24
````

```bash
scrapy crawl autoscout
```
2. Experiment with the notebooks to clean and explore the new data, then retrain the model using the updated data.