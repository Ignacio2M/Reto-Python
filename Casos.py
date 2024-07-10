import json
import math
import pandas as pd


def Caso1(path_data):
    df_car = pd.read_csv(path_data)
    df_car['Pos_date'] = pd.to_datetime(df_car['Pos_date'], unit='ms')
    return df_car


# --------------------------------------------------------
def Caso2(path_data):
    df_car = Caso1(path_data)
    return json.loads(df_car.to_json(orient='records', indent=4))


# --------------------------------------------------------
def Caso3(path_data):
    json_cars = Caso2(path_data)
    json_cars = sorted(json_cars, key=lambda k: k['Pos_date'])
    total_distance = {}
    for index, item in enumerate(json_cars):
        matricula = item.get('Matricula')
        if matricula is None:
            raise KeyError(f"Loss 'Matricula' field in index {index}")
        distance = total_distance.get(matricula, 0)
        distance_increment = item.get('Distance')
        if distance_increment is None:
            raise ValueError(f"Loss 'Distance' field in 'Matricula': {matricula}")
        distance += distance_increment
        total_distance.update({matricula: distance})
    return total_distance

# --------------------------------------------------------


def Caso4(path_data):
    json_cars = Caso2(path_data)
    json_cars = sorted(json_cars, key=lambda k: k['Pos_date'])
    total_distance_car = {}
    last_point_car = {}
    for index, item in enumerate(json_cars):
        matricula = item.get('Matricula')

        if matricula is None:
            raise KeyError(f"Loss 'Matricula' field in index {index}")

        lat = item.get('Latitud')
        lon = item.get('Longitud')

        if lat is None or lon is None:
            raise ValueError(f"Loss 'Latitud' and/or 'Longitud' field in 'Matricula': {matricula}")

        distance = total_distance_car.get(matricula, 0)
        last_point = last_point_car.get(matricula)
        if last_point is not None:
            distance += abs(_distanceJeo(last_point[0], last_point[1], lat, lon))

        last_point = (lat, lon)

        total_distance_car.update({matricula: distance})
        last_point_car.update({matricula: last_point})
    return total_distance_car


def _distanceJeo(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    d_lat = lat2 - lat1
    d_lon = lon2 - lon1
    a = math.sqrt(math.sin(d_lat / 2) ** 2) + math.cos(lat1) * math.cos(lat2) * (math.sin(d_lon / 2) ** 2)
    c = 2 * math.asin(a)

    # a = math.sin(d_lat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(d_lon / 2)**2
    # c = 2 * math.asin(math.sqrt(a))

    radio_earth_km = 6371

    distance_km = radio_earth_km * c
    return distance_km


# --------------------------------------------------------
def Caso5(path_data, out_file):
    df_car = Caso1(path_data)
    df_aux = df_car.groupby('Matricula')['Pos_date'].max().reset_index()
    df_aux = df_aux.sort_values(['Pos_date'], ascending=False)
    df_aux = pd.merge(df_aux, df_car, on=["Matricula", 'Pos_date'])
    df_aux.drop(columns=["Distance"], inplace=True)
    df_aux['Pos_date'] = df_aux['Pos_date'].dt.strftime('%d-%m-%Y %H:%M:%S')

    print(df_aux.dtypes)

    df_aux.to_csv(f'./{out_file}', index=False, sep='\t')
