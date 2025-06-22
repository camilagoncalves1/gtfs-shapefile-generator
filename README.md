# gtfs-shapefile-generator (QGIS)

Este projeto tem como objetivo automatizar a conversão de arquivos GTFS (`.txt` ou `.csv`) em shapefiles georreferenciados diretamente no QGIS. O script foi desenvolvido com Python utilizando a API do QGIS e permite integrar múltiplos arquivos GTFS (como `stops.txt`, `shapes.txt`, `trips.txt`, `routes.txt`, `fare_rules.txt`, `agency.txt`), gerando visualizações das rotas e paradas com atributos completos e já carregados no projeto do QGIS.

## ✨ Funcionalidades

- 📍 Gera shapefile de paradas (pontos) a partir do `stops.txt`
- 🧭 Gera shapefile de itinerários (linhas) a partir do `shapes.txt` e outros arquivos associados
- 🔗 Faz join automático de campos com base em `shape_id`, `route_id` e `agency_id`
- 🧾 Todos os atributos dos arquivos de entrada são incluídos no shapefile final
- 🗺️ Os arquivos são carregados automaticamente no QGIS após a execução

## 🗂️ Estrutura esperada de arquivos GTFS

gtfs_rio-de-janeiro/
├── stops.txt
├── shapes.txt
├── trips.txt
├── routes.txt
├── fare_rules.txt
└── agency.txt

## 🚀 Como usar

1. Abra o QGIS.
2. Vá até o console Python (`Ctrl+Alt+P`).
3. Cole e execute o script `generate_qgis_shapefiles.py` com os caminhos ajustados para seus dados.
4. Os shapefiles serão salvos em uma pasta local e adicionados automaticamente ao seu projeto do QGIS.

## 📦 Requisitos

- QGIS instalado
- Pacotes Python: `pandas`
- O script deve ser executado dentro do console Python do QGIS

## 📍 Exemplo de uso

Este exemplo usa os dados GTFS disponibilizados pela prefeitura do Rio de Janeiro, mas o script pode ser adaptado para qualquer cidade ou base GTFS.

👨‍💻 Autora

Script feito por Camila Gonçalves
Mestranda em Sensoriamento Remoto - INPE
GitHub: @camilagoncalves1
