from datetime import datetime, timedelta
from meteostat import Hourly

class Weather:
    def __init__(self,):
        # Set time period
        self.time = datetime(2020, 5, 1)
        self.location = '72681'
        self.T = None
        self.F = None
        self.H = None
    
    def update(self, t):
        self.time = self.time+timedelta(hours=1)
        data = Hourly(self.location, self.time, self.time).fetch().iloc[0]
        self.T = data.temp
        self.F = data.wspd
        self.H = data.rhum