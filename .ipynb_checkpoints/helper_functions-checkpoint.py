import openmeteo_requests

import pandas as pd
import requests_cache
from retry_requests import retry
from geopy.geocoders import Nominatim


def get_hourly_weather_data(lat,lon):
    # Setup the Open-Meteo API client with cache and retry on error
    cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
    retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
    openmeteo = openmeteo_requests.Client(session = retry_session)

    city,state = get_city_state(lat,lon)
    
    # Make sure all desired weather variables are listed here
    url = "https://historical-forecast-api.open-meteo.com/v1/forecast"
    params = {
    	"latitude": lat,
    	"longitude": lon,
    	"start_date": "2023-01-01",
    	"end_date": "2025-05-12",
    	"hourly": ["relative_humidity_2m", "dew_point_2m", "precipitation_probability", "vapour_pressure_deficit", "wind_speed_10m", "wind_speed_80m", "wind_speed_120m", "wind_speed_180m", "precipitation", "temperature_2m", "apparent_temperature", "rain", "showers", "weather_code", "cloud_cover_low", "cloud_cover_mid", "cloud_cover_high", "evapotranspiration"],
    	"timezone": "auto",
    	"wind_speed_unit": "mph",
    	"temperature_unit": "fahrenheit",
    	"precipitation_unit": "inch"
    }
    responses = openmeteo.weather_api(url, params=params)
    
    # Process first location. Add a for-loop for multiple locations or weather models
    response = responses[0]
    
    # Process hourly data. The order of variables needs to be the same as requested.
    hourly = response.Hourly()
    hourly_relative_humidity_2m = hourly.Variables(0).ValuesAsNumpy()
    hourly_dew_point_2m = hourly.Variables(1).ValuesAsNumpy()
    hourly_precipitation_probability = hourly.Variables(2).ValuesAsNumpy()
    hourly_vapour_pressure_deficit = hourly.Variables(3).ValuesAsNumpy()
    hourly_wind_speed_10m = hourly.Variables(4).ValuesAsNumpy()
    hourly_wind_speed_80m = hourly.Variables(5).ValuesAsNumpy()
    hourly_wind_speed_120m = hourly.Variables(6).ValuesAsNumpy()
    hourly_wind_speed_180m = hourly.Variables(7).ValuesAsNumpy()
    hourly_precipitation = hourly.Variables(8).ValuesAsNumpy()
    hourly_temperature_2m = hourly.Variables(9).ValuesAsNumpy()
    hourly_apparent_temperature = hourly.Variables(10).ValuesAsNumpy()
    hourly_rain = hourly.Variables(11).ValuesAsNumpy()
    hourly_showers = hourly.Variables(12).ValuesAsNumpy()
    hourly_weather_code = hourly.Variables(13).ValuesAsNumpy()
    hourly_cloud_cover_low = hourly.Variables(14).ValuesAsNumpy()
    hourly_cloud_cover_mid = hourly.Variables(15).ValuesAsNumpy()
    hourly_cloud_cover_high = hourly.Variables(16).ValuesAsNumpy()
    hourly_evapotranspiration = hourly.Variables(17).ValuesAsNumpy()
    
    hourly_data = {"date": pd.date_range(
    	start = pd.to_datetime(hourly.Time(), unit = "s"),
    	end = pd.to_datetime(hourly.TimeEnd(), unit = "s"),
    	freq = pd.Timedelta(seconds = hourly.Interval()),
    	inclusive = "left"
    )}

    hourly_data["city"] = city
    hourly_data["state"] = state
    hourly_data["relative_humidity_2m"] = hourly_relative_humidity_2m
    hourly_data["dew_point_2m"] = hourly_dew_point_2m
    hourly_data["precipitation_probability"] = hourly_precipitation_probability
    hourly_data["vapour_pressure_deficit"] = hourly_vapour_pressure_deficit
    hourly_data["wind_speed_10m"] = hourly_wind_speed_10m
    hourly_data["wind_speed_80m"] = hourly_wind_speed_80m
    hourly_data["wind_speed_120m"] = hourly_wind_speed_120m
    hourly_data["wind_speed_180m"] = hourly_wind_speed_180m
    hourly_data["precipitation"] = hourly_precipitation
    hourly_data["temperature_2m"] = hourly_temperature_2m
    hourly_data["apparent_temperature"] = hourly_apparent_temperature
    hourly_data["rain"] = hourly_rain
    hourly_data["showers"] = hourly_showers
    hourly_data["weather_code"] = hourly_weather_code
    hourly_data["cloud_cover_low"] = hourly_cloud_cover_low
    hourly_data["cloud_cover_mid"] = hourly_cloud_cover_mid
    hourly_data["cloud_cover_high"] = hourly_cloud_cover_high
    hourly_data["evapotranspiration"] = hourly_evapotranspiration
    
    hourly_dataframe = pd.DataFrame(data = hourly_data)
    return hourly_dataframe

def get_hourly_aqi_data(lat,lon):
    # Setup the Open-Meteo API client with cache and retry on error
    cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
    retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
    openmeteo = openmeteo_requests.Client(session = retry_session)

    city,state = get_city_state(lat,lon)
    
    # Make sure all required weather variables are listed here
    # The order of variables in hourly or daily is important to assign them correctly below
    url = "https://air-quality-api.open-meteo.com/v1/air-quality"
    params = {
    	"latitude": lat,
    	"longitude": lon,
    	"hourly": ["pm10", "pm2_5", "carbon_monoxide", "carbon_dioxide", "nitrogen_dioxide", "sulphur_dioxide", "ozone", "uv_index", "ammonia", "methane", "us_aqi", "us_aqi_pm2_5", "us_aqi_pm10", "us_aqi_nitrogen_dioxide", "us_aqi_carbon_monoxide", "us_aqi_ozone", "us_aqi_sulphur_dioxide"],
        "timezone": "auto",
    	"start_date": "2023-01-01",
    	"end_date": "2025-05-12"
    }
    responses = openmeteo.weather_api(url, params=params)
    
    # Process first location. Add a for-loop for multiple locations or weather models
    response = responses[0]
    
    # Process hourly data. The order of variables needs to be the same as requested.
    hourly = response.Hourly()
    hourly_pm10 = hourly.Variables(0).ValuesAsNumpy()
    hourly_pm2_5 = hourly.Variables(1).ValuesAsNumpy()
    hourly_carbon_monoxide = hourly.Variables(2).ValuesAsNumpy()
    hourly_carbon_dioxide = hourly.Variables(3).ValuesAsNumpy()
    hourly_nitrogen_dioxide = hourly.Variables(4).ValuesAsNumpy()
    hourly_sulphur_dioxide = hourly.Variables(5).ValuesAsNumpy()
    hourly_ozone = hourly.Variables(6).ValuesAsNumpy()
    hourly_uv_index = hourly.Variables(7).ValuesAsNumpy()
    hourly_ammonia = hourly.Variables(8).ValuesAsNumpy()
    hourly_methane = hourly.Variables(9).ValuesAsNumpy()
    hourly_us_aqi = hourly.Variables(10).ValuesAsNumpy()
    hourly_us_aqi_pm2_5 = hourly.Variables(11).ValuesAsNumpy()
    hourly_us_aqi_pm10 = hourly.Variables(12).ValuesAsNumpy()
    hourly_us_aqi_nitrogen_dioxide = hourly.Variables(13).ValuesAsNumpy()
    hourly_us_aqi_carbon_monoxide = hourly.Variables(14).ValuesAsNumpy()
    hourly_us_aqi_ozone = hourly.Variables(15).ValuesAsNumpy()
    hourly_us_aqi_sulphur_dioxide = hourly.Variables(16).ValuesAsNumpy()
    
    hourly_data = {"date": pd.date_range(
    	start = pd.to_datetime(hourly.Time(), unit = "s"),
    	end = pd.to_datetime(hourly.TimeEnd(), unit = "s"),
    	freq = pd.Timedelta(seconds = hourly.Interval()),
    	inclusive = "left"
    )}

    hourly_data["city"] = city
    hourly_data["state"] = state
    hourly_data["pm10"] = hourly_pm10
    hourly_data["pm2_5"] = hourly_pm2_5
    hourly_data["carbon_monoxide"] = hourly_carbon_monoxide
    hourly_data["carbon_dioxide"] = hourly_carbon_dioxide
    hourly_data["nitrogen_dioxide"] = hourly_nitrogen_dioxide
    hourly_data["sulphur_dioxide"] = hourly_sulphur_dioxide
    hourly_data["ozone"] = hourly_ozone
    hourly_data["uv_index"] = hourly_uv_index
    hourly_data["ammonia"] = hourly_ammonia
    hourly_data["methane"] = hourly_methane
    hourly_data["us_aqi"] = hourly_us_aqi
    hourly_data["us_aqi_pm2_5"] = hourly_us_aqi_pm2_5
    hourly_data["us_aqi_pm10"] = hourly_us_aqi_pm10
    hourly_data["us_aqi_nitrogen_dioxide"] = hourly_us_aqi_nitrogen_dioxide
    hourly_data["us_aqi_carbon_monoxide"] = hourly_us_aqi_carbon_monoxide
    hourly_data["us_aqi_ozone"] = hourly_us_aqi_ozone
    hourly_data["us_aqi_sulphur_dioxide"] = hourly_us_aqi_sulphur_dioxide
    
    hourly_dataframe = pd.DataFrame(data = hourly_data)
    return hourly_dataframe


def hourly_to_daily(df):
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date',inplace=True)

    numeric_cols = df.select_dtypes(include='number').columns
    df_numeric = df[numeric_cols]
    
    agg_fcts = ['min','max','mean']
    
    daily_df = df_numeric.resample('D').agg(agg_fcts)
    daily_df.columns = ['_'.join([col,stat]) for col, stat in daily_df.columns]
    
    nonnum_cols = df.drop(columns=numeric_cols).resample('D').first()

    daily_df = pd.concat([daily_df, nonnum_cols], axis=1).reset_index()
    return daily_df

def get_city_state(lat,lon):
    # Initialize the geocoder
    geolocator = Nominatim(user_agent="geoapi")

    # Perform reverse geocoding
    location = geolocator.reverse((lat, lon), exactly_one=True)
    address = location.raw['address']
    
    # Extract city and state (falling back to other fields if needed)
    city = address.get('city') or address.get('town') or address.get('village')
    state = address.get('state')
    
    return city, state
    

