import dash
import dash_html_components as html
import dash_leaflet as dl

import rasterio

app = dash.Dash()

filename = './data/raster/VHI/VHI_04_2019.tif'

raster = rasterio.open(filename)

bounds = list(raster.bounds)
image_bounds = [bounds[:2],bounds[2:]]

app.layout = html.Div([dl.Map([dl.ImageOverlay(opacity=0.5, url=filename, bounds=image_bounds), dl.TileLayer()],
                              bounds=image_bounds,
                              style={'width': '100%', 'height': '50vh', 'margin': "auto", "display": "block"})])




if __name__ == '__main__':
    app.run_server()