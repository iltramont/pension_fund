import utils
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

plt.style.use('ggplot')

RAL = 100_000
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
    contributi = utils.calcola_contributi(RAL)

    versato_nel_fondo = utils.versato_nel_fondo(RAL, versamento_lavoratore)

    imponibile = utils.calcola_imponibile(RAL, versamento_lavoratore)

    irpef_netta = utils.calcola_irpef_netta(imponibile)

    addizionale_comunale = utils.calcola_addizionale_comunale(imponibile)

    addizionale_regionale = utils.calcola_addizionale_regionale(imponibile)

    netto_annuo = utils.calcola_netto_annuo(RAL, versamento_lavoratore)

print(f'{RAL = }')
print(f'{versamento_lavoratore = }')
print(f'{versato_nel_fondo = }')
print(f'{imponibile = }')
print(f'{irpef_netta = }')
print(f'{addizionale_comunale = }')
print(f'{addizionale_regionale = }')
print(f'{netto_annuo = }')
