import pandas as pd
import numpy as np

ALIQUOTA_CONTRIBUTIVA = 0.0919

SCAGLIONI_IRPEF = (0.0, 28_000.0, 50_000.0)
ALIQUOTE_IRPEF = (0.23, 0.35, 0.43)

SCAGLIONI_REGIONALI = (0.0, 15_000.0, 28_000.0, 50_000.0)
ALIQUOTE_REGIONALI = (0.0123, 0.0158, 0.0172, 0.0173)

SCAGLIONI_COMUNALI = (0.0, 15_000.0, 28_000.0)
ALIQUOTE_COMUNALI = (0.007, 0.0075, 0.0080)

MAX_BONUS_RENZI = 1200.0
SOGLIA_BONUS_RENZI = 28_000.0

SOGLIE_DET_LAV_DIP = (15_000.0, 28_000.0, 50_000.0)


def calcola_contributi(ral: float, aliquota_contributiva: float = ALIQUOTA_CONTRIBUTIVA) -> float:
    return ral * aliquota_contributiva


def calcola_irpef_lordo(imponibile: float, scaglioni: tuple[float] = SCAGLIONI_IRPEF, aliquote: tuple[float] = ALIQUOTE_IRPEF) -> float:
    result = 0.0
    for i, soglia in enumerate(scaglioni[1:]):
        aliquota = aliquote[i]
        if soglia > imponibile:
            result += (imponibile-scaglioni[i]) * aliquota
            return result
        else:
            result += (soglia - scaglioni[i]) * aliquota
    result += (imponibile - scaglioni[-1]) * aliquote[-1]
    return result


def calcola_addizionale_regionale(imponibile: float, scaglioni: tuple[float] = SCAGLIONI_REGIONALI, aliquote: tuple[float] = ALIQUOTE_REGIONALI) -> float:
    return calcola_irpef_lordo(imponibile, scaglioni, aliquote)


def calcola_addizionale_comunale(imponibile: float, scaglioni: tuple[float] = SCAGLIONI_COMUNALI, aliquote: tuple[float] = ALIQUOTE_COMUNALI) -> float:
    return calcola_irpef_lordo(imponibile, scaglioni, aliquote)


def detrazioni_irpef_lavoro_dipendente(imponibile: float) -> float:
    if imponibile > SOGLIE_DET_LAV_DIP[-1]:
        return 0.0
    elif imponibile < SOGLIE_DET_LAV_DIP[0]:
        return 1955.0
    elif SOGLIE_DET_LAV_DIP[0] < imponibile <= SOGLIE_DET_LAV_DIP[1]:
        return 1910.0 + 1190.0 * (SOGLIE_DET_LAV_DIP[1] - imponibile) / (SOGLIE_DET_LAV_DIP[1] - SOGLIE_DET_LAV_DIP[0])
    else:
        return 1910.0 * (SOGLIE_DET_LAV_DIP[2] - imponibile) / (SOGLIE_DET_LAV_DIP[2] - SOGLIE_DET_LAV_DIP[1])



if __name__ == '__main__':
    imponibile = 40000
    print(calcola_irpef_lordo(imponibile))
    print(calcola_addizionale_regionale(imponibile))
    print(calcola_addizionale_comunale(imponibile))
    print(detrazioni_irpef_lavoro_dipendente(imponibile))

