import openmeteo_requests

import pandas as pd
import requests_cache
from retry_requests import retry
from geopy.geocoders import Nominatim


def get_weather_data(state,lat,lon,start="2022-12-31",stop="2025-06-01"):
    # Setup the Open-Meteo API client with cache and retry on error
    cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
    retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
    openmeteo = openmeteo_requests.Client(session = retry_session)

    
    # Make sure all desired weather variables are listed here
    url = "https://historical-forecast-api.open-meteo.com/v1/forecast"
    params = {
    	"latitude": lat,
    	"longitude": lon,
    	"start_date": start,
    	"end_date": stop,
    	"hourly": ["rain", "snowfall", "relative_humidity_2m", "dew_point_2m", "apparent_temperature", "wind_speed_10m", "wind_direction_10m"],
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
    hourly_rain = hourly.Variables(0).ValuesAsNumpy()
    hourly_snowfall = hourly.Variables(1).ValuesAsNumpy()
    hourly_relative_humidity_2m = hourly.Variables(2).ValuesAsNumpy()
    hourly_apparent_temperature = hourly.Variables(4).ValuesAsNumpy()
    hourly_wind_speed_10m = hourly.Variables(5).ValuesAsNumpy()
    hourly_wind_direction_10m = hourly.Variables(6).ValuesAsNumpy()
    
    hourly_data = {"date": pd.date_range(
    	start = pd.to_datetime(hourly.Time(), unit = "s"),
    	end = pd.to_datetime(hourly.TimeEnd(), unit = "s"),
    	freq = pd.Timedelta(seconds = hourly.Interval()),
    	inclusive = "left"
    )}

    hourly_data["state"] = state
    hourly_data["rain"] = hourly_rain
    hourly_data["snowfall"] = hourly_snowfall
    hourly_data["relative_humidity_2m"] = hourly_relative_humidity_2m
    hourly_data["apparent_temperature"] = hourly_apparent_temperature
    hourly_data["wind_speed_10m"] = hourly_wind_speed_10m
    hourly_data["wind_direction_10m"] = hourly_wind_direction_10m
    
    df_hourly = pd.DataFrame(data = hourly_data)
    df_hourly['date'] = pd.to_datetime(df_hourly['date'])
    df_hourly.set_index('date', inplace=True)

    # Separate columns
    rain_snow_cols = ['rain', 'snowfall']
    other_numeric_cols = [col for col in df_hourly.select_dtypes(include='number').columns if col not in rain_snow_cols]
    non_numeric_daily = df_hourly.drop(columns=rain_snow_cols + other_numeric_cols).resample('D').first()

    # Aggregate
    rain_snow_daily = df_hourly[rain_snow_cols].resample('D').agg(['sum', 'max'])
    rain_snow_daily.columns = ['_'.join([col, stat]) for col, stat in rain_snow_daily.columns]

    other_daily = df_hourly[other_numeric_cols].resample('D').agg(['min', 'max', 'mean'])
    other_daily.columns = ['_'.join([col, stat]) for col, stat in other_daily.columns]

    # Combine
    df_daily = pd.concat([non_numeric_daily, rain_snow_daily, other_daily], axis=1).reset_index()
    df_daily = df_daily.drop(['apparent_temperature_mean'], axis=1)

    # Lag feature for min/max temp
    for col in ['apparent_temperature_min', 'apparent_temperature_max']:
        df_daily[f'{col}_lag'] = df_daily[col].shift(1)
    df_daily = df_daily.iloc[1:]
    return df_daily

def get_aqi_data(state,lat,lon,start="2022-12-31",stop="2025-06-01"):
    # Setup the Open-Meteo API client with cache and retry on error
    cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
    retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
    openmeteo = openmeteo_requests.Client(session = retry_session)

    
    # Make sure all required weather variables are listed here
    # The order of variables in hourly or daily is important to assign them correctly below
    url = "https://air-quality-api.open-meteo.com/v1/air-quality"
    params = {
    	"latitude": lat,
    	"longitude": lon,
    	"hourly": ["us_aqi_pm2_5", "us_aqi", "us_aqi_pm10", "us_aqi_nitrogen_dioxide", "us_aqi_carbon_monoxide", "us_aqi_ozone", "us_aqi_sulphur_dioxide"],
        "timezone": "auto",
    	"start_date": start,
    	"end_date": stop
    }
    responses = openmeteo.weather_api(url, params=params)
    
    # Process first location. Add a for-loop for multiple locations or weather models
    response = responses[0]
    
    # Process hourly data. The order of variables needs to be the same as requested.
    hourly = response.Hourly()
    hourly_us_aqi_pm2_5 = hourly.Variables(0).ValuesAsNumpy()
    hourly_us_aqi = hourly.Variables(1).ValuesAsNumpy()
    hourly_us_aqi_pm10 = hourly.Variables(2).ValuesAsNumpy()
    hourly_us_aqi_nitrogen_dioxide = hourly.Variables(3).ValuesAsNumpy()
    hourly_us_aqi_carbon_monoxide = hourly.Variables(4).ValuesAsNumpy()
    hourly_us_aqi_ozone = hourly.Variables(5).ValuesAsNumpy()
    hourly_us_aqi_sulphur_dioxide = hourly.Variables(6).ValuesAsNumpy()
    
    hourly_data = {"date": pd.date_range(
    	start = pd.to_datetime(hourly.Time(), unit = "s"),
    	end = pd.to_datetime(hourly.TimeEnd(), unit = "s"),
    	freq = pd.Timedelta(seconds = hourly.Interval()),
    	inclusive = "left"
    )}


    hourly_data["state"] = state
    hourly_data["us_aqi_pm2_5"] = hourly_us_aqi_pm2_5
    hourly_data["us_aqi"] = hourly_us_aqi
    hourly_data["us_aqi_pm10"] = hourly_us_aqi_pm10
    hourly_data["us_aqi_nitrogen_dioxide"] = hourly_us_aqi_nitrogen_dioxide
    hourly_data["us_aqi_carbon_monoxide"] = hourly_us_aqi_carbon_monoxide
    hourly_data["us_aqi_ozone"] = hourly_us_aqi_ozone
    hourly_data["us_aqi_sulphur_dioxide"] = hourly_us_aqi_sulphur_dioxide
        
    df_hourly = pd.DataFrame(data = hourly_data)
    df_hourly['date'] = pd.to_datetime(df_hourly['date'])
    df_hourly.set_index('date', inplace=True)

    # Separate columns
    numeric_cols = df_hourly.select_dtypes(include='number').columns.tolist()
    non_numeric_daily = df_hourly.drop(columns=numeric_cols).resample('D').first()

    # Aggregate
    daily = df_hourly[numeric_cols].resample('D').agg(['min', 'max', 'mean'])
    daily.columns = ['_'.join([col, stat]) for col, stat in daily.columns]

    # Combine
    df_daily = pd.concat([non_numeric_daily,daily], axis=1).reset_index()

    #Bin AQI and create lag feature
    bins = [0, 50, 100, 150, 200, 300, 500]
    labels = [1, 2, 3, 4, 5, 6]  # Increasing severity
    for col in ['us_aqi_min', 'us_aqi_max', 'us_aqi_mean']:
        bin_col = f"{col}_bin"
        df_daily[bin_col] = pd.cut(df_daily[col], bins=bins, labels=labels, right=True).astype('int')
        df_daily[f'{bin_col}_lag'] = df_daily[bin_col].shift(1)
        df_daily[f'{col}_lag'] = df_daily[col].shift(1)
    df_daily = df_daily.iloc[1:]
    return df_daily

