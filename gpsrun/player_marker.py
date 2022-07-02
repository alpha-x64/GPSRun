from kivy_garden.mapview import MapMarker

class PlayerMarker(MapMarker):

    lat = -38.746640
    lon = -72.615610
    radius = 0.00005
    step = 0.00001

    source = "imagenes/marker.png"

    def set_lat(self):
        self.lat = self.lat + self.step
        print("lat: " + str(self.lat))

    def set_lon(self):
        self.lon = self.lon + self.step
        print("lon: " + str(self.lon))

    def get_lat(self):
        return self.lat

    def get_lon(self):
        return self.lon

    def on_release(self):
        #self.set_lat()
        print(self.lat)
        pass