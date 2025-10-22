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



def simula(ral: float, versamento_lavoratore: float):
    contributi = utils.calcola_contributi(ral)
    versato_nel_fondo = utils.versato_nel_fondo(ral, versamento_lavoratore)
    quota_fondo_azienda = versato_nel_fondo - versamento_lavoratore
    imponibile = utils.calcola_imponibile(ral, versamento_lavoratore)
    irpef_netta = utils.calcola_irpef_netta(imponibile)
    addizionale_comunale = utils.calcola_addizionale_comunale(imponibile)
    addizionale_regionale = utils.calcola_addizionale_regionale(imponibile)
    netto_annuo = utils.calcola_netto_annuo(ral, versamento_lavoratore)
    return {
        'contributi': contributi,
        'versamento_lavoratore': versamento_lavoratore,
        'versato_nel_fondo': versato_nel_fondo,
        'quota_fondo_azienda': quota_fondo_azienda,
        'imponibile': imponibile,
        'irpef_netta': irpef_netta,
        'addizionale_regionale': addizionale_regionale,
        'addizionale_comunale': addizionale_comunale,
        'netto_annuo': netto_annuo
    }

versamenti_fondo = np.linspace(0, 6000, 101)
simulazioni = [simula(RAL, v) for v in versamenti_fondo]

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