from Soil import Soil
from Weather import Weather
import pandas as pd
import matplotlib.pyplot as plt


if __name__ == '__main__':
    print('simulation starts')
    soil = Soil()
    weather = Weather()
    
    data = list()
    for hr in range(4*7*24):
        # one hour per loop
        weather.update(hr)
        if hr%5 == 0:
            soil.intake(25)
        soil.evaporate_mock(weather.F, weather.H, 1)
        data.append((weather.F, weather.H, soil.moisture))

    _df = pd.DataFrame(data, columns=['F','H','M'])
    plt.plot(_df.index, _df.M, label='M')
    plt.plot(_df.index, _df.H, label='H')
    plt.plot(_df.index, _df.F, label='F')
    plt.legend()
    plt.show()