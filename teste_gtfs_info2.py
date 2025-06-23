from qgis.core import (
    QgsApplication,
    QgsVectorLayer,
    QgsField,
    QgsPointXY,
    QgsFeature,
    QgsGeometry,
    QgsWkbTypes,
    QgsCoordinateReferenceSystem,
    QgsVectorFileWriter
)
from PyQt5.QtCore import QVariant
import pandas as pd
import os

# Definição do diretório de saída
output_dir = r"D:\teste_gtfs\shapes2"
os.makedirs(output_dir, exist_ok=True)

def create_stops_shapefile(input_csv, output_shp):
    stops = pd.read_csv(input_csv)
    crs = QgsCoordinateReferenceSystem("EPSG:4326")
    layer = QgsVectorLayer(f"Point?crs={crs.authid()}", "GTFS Stops", "memory")

    # Define campos dinamicamente
    layer_data_provider = layer.dataProvider()
    fields = [QgsField(col, QVariant.String) for col in stops.columns]
    layer_data_provider.addAttributes(fields)
    layer.updateFields()

    # Adiciona pontos
    features = []
    for _, row in stops.iterrows():
        point = QgsPointXY(row['stop_lon'], row['stop_lat'])
        feature = QgsFeature()
        feature.setGeometry(QgsGeometry.fromPointXY(point))
        feature.setAttributes([str(row[col]) for col in stops.columns])
        features.append(feature)
    layer_data_provider.addFeatures(features)

    # Salva o shapefile
    shapefile_path = os.path.join(output_dir, output_shp)
    QgsVectorFileWriter.writeAsVectorFormat(layer, shapefile_path, "UTF-8", layer.crs(), "ESRI Shapefile")
    print(f"Shapefile de paradas criado: {shapefile_path}")

    return shapefile_path  # Retorna o caminho do shapefile criado

def create_shapes_shapefile(shapes_csv, trips_csv, routes_csv, fare_rules_csv, agency_csv, output_shp):
    # Lê os arquivos CSV
    shapes = pd.read_csv(shapes_csv).sort_values(by=['shape_id', 'shape_pt_sequence'])
    trips = pd.read_csv(trips_csv)
    routes = pd.read_csv(routes_csv)
    fare = pd.read_csv(fare_rules_csv)
    agency = pd.read_csv(agency_csv)

    # Faz os joins para agregar informações
    trips_routes = trips.merge(routes, on='route_id', how='left')
    trips_routes_fare = trips_routes.merge(fare, on='route_id', how='left', suffixes=('', '_fare'))

    # Adiciona `agency_id` se não existir
    if 'agency_id' not in trips_routes_fare.columns:
        trips_routes_fare['agency_id'] = ""

    trips_routes_fare_agency = trips_routes_fare.merge(agency, on='agency_id', how='left', suffixes=('', '_agency'))

    # Faz merge final com `shapes.txt`
    shapes_with_info = shapes.merge(trips_routes_fare_agency, on='shape_id', how='left')

    crs = QgsCoordinateReferenceSystem("EPSG:4326")
    layer = QgsVectorLayer(f"LineString?crs={crs.authid()}", "GTFS Shapes", "memory")

    # Define dinamicamente os campos do shapefile com base nas colunas do CSV final
    layer_data_provider = layer.dataProvider()
    fields = [QgsField(col, QVariant.String) for col in shapes_with_info.columns]
    layer_data_provider.addAttributes(fields)
    layer.updateFields()

    # Adiciona as linhas
    features = []
    for shape_id, group in shapes_with_info.groupby('shape_id'):
        points = [QgsPointXY(row['shape_pt_lon'], row['shape_pt_lat']) for _, row in group.iterrows()]
        feature = QgsFeature()
        feature.setGeometry(QgsGeometry.fromPolylineXY(points))
        feature.setAttributes([str(group.iloc[0][col]) for col in shapes_with_info.columns])
        features.append(feature)

    layer_data_provider.addFeatures(features)

    # Salva o shapefile
    shapefile_path = os.path.join(output_dir, output_shp)
    QgsVectorFileWriter.writeAsVectorFormat(layer, shapefile_path, "UTF-8", layer.crs(), "ESRI Shapefile")
    print(f"Shapefile de formas criado: {shapefile_path}")

    return shapefile_path  # Retorna o caminho do shapefile criado

# Caminhos dos arquivos de entrada
stops_file = r"D:\teste_gtfs\gtfs_rio-de-janeiro\stops.txt"
shapes_file = r"D:\teste_gtfs\gtfs_rio-de-janeiro\shapes.txt"
trips_file = r"D:\teste_gtfs\gtfs_rio-de-janeiro\trips.txt"
routes_file = r"D:\teste_gtfs\gtfs_rio-de-janeiro\routes.txt"
fare_rules_file = r"D:\teste_gtfs\gtfs_rio-de-janeiro\fare_rules.txt"
agency_file = r"D:\teste_gtfs\gtfs_rio-de-janeiro\agency.txt"

# Criando os shapefiles e obtendo os caminhos
stops_shp_path = create_stops_shapefile(stops_file, "gtfs_stops.shp")
shapes_shp_path = create_shapes_shapefile(shapes_file, trips_file, routes_file, fare_rules_file, agency_file, "gtfs_shapes_with_info.shp")

# Adicionando os shapefiles gerados ao QGIS
iface.addVectorLayer(stops_shp_path, "GTFS Stops", "ogr")
iface.addVectorLayer(shapes_shp_path, "GTFS Shape", "ogr")
