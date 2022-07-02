from kivy_garden.mapview import MapMarkerPopup

class ObjectiveMarker(MapMarkerPopup):

    source = "imagenes/marker.png"

    def get_lat(self):
        return self.lat

    def get_lon(self):
        return self.lon

    def on_release():
        pass