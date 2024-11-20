
import pandas as pd
import math

# Función utilizada para calcular la distancia de la carrera.
def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the great-circle distance between two points
    on the Earth's surface using the Haversine formula.

    Parameters:
        lat1, lon1 (float): Latitude and longitude of the first point (in degrees).
        lat2, lon2 (float): Latitude and longitude of the second point (in degrees).

    Returns:
        float: Distance between the two points in kilometers.
    """
    # Convert latitude and longitude from degrees to radians
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    # Haversine formula
    dlon = lon2_rad - lon1_rad
    dlat = lat2_rad - lat1_rad
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    radius_of_earth = 6371  # Radius of the Earth in kilometers
    distance = radius_of_earth * c

    return distance

# Función encagada de orquestar la limpieza de los datos.
def clean_data(df):
  """
  Limpia los datos de entrada, aplicando cambios de formato, eliminación de columnas y manejo de outliers.

  Parameters
  ----------
  df : dataframe pandas

  Returns
  -------
  train_data : dataframe pandas
  """

  day_map={
    'Monday':0,'Tuesday':1,'Wednesday':2,'Thursday':3,
    'Friday':4,'Saturday':5,'Sunday':6,
  }

  cp_df=df.copy()
  cp_df["pickup_datetime"] = pd.to_datetime(cp_df["pickup_datetime"])
  cp_df["pickup_day"] = cp_df["pickup_datetime"].dt.day_name()
  cp_df["pickup_time"]=cp_df["pickup_datetime"].dt.hour
  cp_df['distance_km'] = cp_df.apply(lambda row: haversine_distance(row['pickup_latitude'], row['pickup_longitude'], row['dropoff_latitude'], row['dropoff_longitude']), axis=1)
  cp_df.drop(["pickup_datetime"],axis=1,inplace=True)

  if "dropoff_datetime" in cp_df.columns:
    cp_df.drop(["dropoff_datetime"],axis=1,inplace=True)
    
  cp_df["store_and_fwd_flag"]=cp_df.store_and_fwd_flag.map({"N":0,"Y":1})
  cp_df['passenger_count'] = pd.Categorical(cp_df['passenger_count'])

  if "trip_duration" in cp_df.columns:
    outliers_in_trip_duration_in_seconds=cp_df[(cp_df["trip_duration"]>8000)&(cp_df["distance_km"]<25)]
    cp_df=cp_df.drop(outliers_in_trip_duration_in_seconds.index, axis=0)
    outliers_in_trip_duration_in_seconds_2=cp_df[(cp_df["trip_duration"]>30000)&(cp_df["distance_km"]<200)]
    cp_df= cp_df.drop(outliers_in_trip_duration_in_seconds_2.index, axis=0)
    outliers_in_trip_duration_in_seconds_3=cp_df[(cp_df["trip_duration"]<50000)&(cp_df["distance_km"]>200)]
    cp_df= cp_df.drop(outliers_in_trip_duration_in_seconds_3.index, axis=0)
    outliers_in_trip_duration_in_seconds_4=cp_df[(cp_df["trip_duration"]>0)&(cp_df["distance_km"]==0)]
    cp_df= cp_df.drop(outliers_in_trip_duration_in_seconds_4.index, axis=0)
    outliers_in_trip_duration_in_seconds_5=cp_df[(cp_df["passenger_count"]==0)&(cp_df["trip_duration"]>1500)]
    cp_df= cp_df.drop(outliers_in_trip_duration_in_seconds_5.index, axis=0)

  cp_df['ordinal_pick_up_day']=cp_df["pickup_day"].map(day_map)
  train_data=cp_df.drop(["id","pickup_longitude","pickup_latitude","dropoff_longitude","dropoff_latitude","pickup_day"],axis=1)

  train_data['passenger_count'] = train_data['passenger_count'].astype(int)

  return train_data

# Valida que el modelo tenga las columnas correctas
def dataValidation(data):
    columns = ('id', 'vendor_id', 'pickup_datetime', 'dropoff_datetime', 'passenger_count', 'pickup_longitude', 'pickup_latitude', 'dropoff_longitude', 'dropoff_latitude', 'store_and_fwd_flag', 'trip_duration')
   
    columnsLess = []

    for column in data.columns:
        if column not in columns:
            columnsLess.append(column)
    if len(columnsLess) > 0:
        return (False, columnsLess )
    return (True, None)
