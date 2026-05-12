import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import utils

plt.style.use('ggplot')

RAL = 30000

s = pd.Series(utils.simula(ral=RAL, versamento_lavoratore=0))

print(s['contributi'] + s['imponibile'])