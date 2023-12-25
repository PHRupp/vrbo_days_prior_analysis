from dataclasses import dataclass
from typing import Any, List

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from scipy.stats import halfnorm

NUM_BINS: int = 12

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
nrows=3
ncols=4
months = [
    'Jan',
    'Feb',
    'Mar',
    'Apr',
    'May',
    'Jun',
    'Jul',
    'Aug',
    'Sep',
    'Oct',
    'Nov',
    'Dec',
]

fig, axs = plt.subplots(
    nrows=nrows,
    ncols=ncols,
)
maxDaysPrior = data['DaysPrior'].max()
max_count = 0
#fig.title('Days booked prior to Check-In')
plt.tight_layout()

@dataclass
class DataStruct:
    ax: Any  # should not be Any, rather a specific type
    bins: List[float]
    counts: List[float]
    month: str
    widths: float
    x: np.array

datastructs: List[DataStruct] = []
m = 0
for i in range(nrows):
    for j in range(ncols):
        month = months[m]
        ind = (data['Month'] == month) & data['DaysPrior'].notnull()
        x = data.loc[ind, 'DaysPrior']
        counts, bins = np.histogram(
            x,
            bins=NUM_BINS,
            range=(0, maxDaysPrior),
        )
        datastructs.append(
            DataStruct(
                axs[i, j],
                bins,
                counts,
                month,
                .95 * (bins[1] - bins[0]),
                x,
            )
        )
        if np.max(counts) > max_count:
            max_count = np.max(counts)
        m += 1

m = 0
for i in range(nrows):
    for j in range(ncols):
        d = datastructs[m]
        ax = d.ax
        ax.set_title(f'{d.month}')
        
        # Fit a half-normal distribution to the data:
        mu, std = halfnorm.fit(d.x)
        
        ax.bar(
            d.bins[:-1],
            d.counts,
            align='edge',
            width=d.widths,
        )
        ax.set_xlim(0, maxDaysPrior)
        ax.set_ylim(0, max_count)
        
        xlin = np.linspace(1, maxDaysPrior)
        ylin = halfnorm.pdf(xlin, loc=mu, scale=std) * maxDaysPrior
        ax.plot(xlin, ylin, color='red')
        m += 1
"""
data.hist(
    'DaysPrior', 
    by='Month',
    xrot=0,
    figsize=(12,8),
    range=[0, data['DaysPrior'].max()],
)
"""
#plt.savefig('daysout_hist.png')
plt.show()







