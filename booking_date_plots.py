from dataclasses import dataclass
from typing import Any, List

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from scipy.stats import halfnorm

file = 'reservations.xlsx'
data = pd.read_excel(file)
#print(data.shape)
#print(data.columns)
"""
Index(['Paid Cleaning', 'Status', 'Days Out', 'Reservation', 'Booking',
       'Check-In', 'Check-Out', 'Adult', 'Child', 'Nights', 'Gross Payout',
       'Cleaning Fee', 'DaysPrior', 'Year', 'Month', 'Net Payout'],
      dtype='object')
"""

ind = (data['Booking'].notnull())
data = data.loc[ind,:]
month_map = {
    1: 'Jan',
    2: 'Feb',
    3: 'Mar',
    4: 'Apr',
    5: 'May',
    6: 'Jun',
    7: 'Jul',
    8: 'Aug',
    9: 'Sep',
    10: 'Oct',
    11: 'Nov',
    12: 'Dec',
}

data.loc[:, 'BookingMonth'] = [d.month for d in data['Booking']]

df = data.groupby(['BookingMonth',])['BookingMonth',].count()
df.loc[:, 'Month'] = [month_map.get(i) for i in df.index]

df.plot.bar(x='Month', y='BookingMonth', rot=0)

plt.show()
