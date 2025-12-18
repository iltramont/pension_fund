import utils
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

plt.style.use('ggplot')

RAL = 25000
"""
VERSAMENTO_MAX_FONDO = 5000

versamenti = np.linspace(0, VERSAMENTO_MAX_FONDO, 101)

stipendi_netti = []

for v in versamenti:
    stipendi_netti.append(utils.calcola_netto_annuo(RAL, v))

fig, ax = plt.subplots()

ax.plot(versamenti, stipendi_netti)

plt.show()
"""





versamenti_fondo = np.linspace(0, 6000, 101)
simulazioni = [utils.simula(RAL, v) for v in versamenti_fondo]

df = pd.DataFrame.from_records(simulazioni)
fig, ax = plt.subplots()
x = df['versamento_lavoratore']
da_plottare = ['versato_nel_fondo', 'imponibile', 'irpef_netta', 'netto_annuo']
for l in da_plottare:
    ax.plot(x, df[l], label=l)

ax.plot(x, df['versato_nel_fondo'] + df['netto_annuo'], label='versato + netto')
ax.set_xlabel('Quota lavoratore')
ax.axvline(utils.DETRAZIONE_MASSIMA_FONDO - 0.0155*RAL)
ax.legend()
plt.show()

print(utils.DETRAZIONE_MASSIMA_FONDO - 0.0155*RAL)