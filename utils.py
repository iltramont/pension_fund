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

DETRAZIONE_MASSIMA_FONDO = 5_164.57
SOGLIA_FONDO_LAVORATORE = 0.0055
QUOTA_FONDO_DATORE = 0.0155


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


def versato_nel_fondo(ral: float,
                      quota_lavoratore: float,
                      soglia_lavoratore: float = SOGLIA_FONDO_LAVORATORE,
                      quota_datore: float = QUOTA_FONDO_DATORE) -> float:
    if quota_lavoratore / ral < soglia_lavoratore:
        return quota_lavoratore
    else:
        return quota_lavoratore + ral * quota_datore


def calcola_imponibile(ral: float, versamento_fondo: float, deduzioni_extra: float = 0.0) -> float:
    result = ral
    # Togli contributi e deduzioni extra
    result = result - calcola_contributi(ral) - deduzioni_extra
    # Togli deduzioni del fondo pensione
    quota_datore = versato_nel_fondo(ral, versamento_fondo) - versamento_fondo
    result = result - min(versamento_fondo, DETRAZIONE_MASSIMA_FONDO-quota_datore)
    return result


def calcola_irpef_netta(imponibile: float, detrazioni_extra: float = 0.0) -> float:
    result = calcola_irpef_lordo(imponibile)
    # Togli detrazioni da lavoro dipendente
    result = result - detrazioni_irpef_lavoro_dipendente(imponibile)
    # Togli detrazioni extra (bisogna essere capienti)
    result = max(0.0, result - detrazioni_extra)
    # Togli il bonus Renzi
    if imponibile < SOGLIA_BONUS_RENZI:
        result = max(0.0, result - MAX_BONUS_RENZI)
    return result


def calcola_netto_annuo(ral: float,
                        versamenti_fondo: float,
                        deduzioni_extra: float = 0,
                        detrazioni_extra: float = 0,
                        ) -> float:
    imponibile = calcola_imponibile(ral, versamenti_fondo, deduzioni_extra)
    totale_irpef = (calcola_irpef_netta(imponibile, detrazioni_extra) +
                    calcola_addizionale_regionale(imponibile) +
                    calcola_addizionale_comunale(imponibile))
    netto = ral - calcola_contributi(ral) - versamenti_fondo - totale_irpef
    return netto


def simula(ral: float, versamento_lavoratore: float):
    contributi = calcola_contributi(ral)
    versato_nel_fondo_ = versato_nel_fondo(ral, versamento_lavoratore)
    quota_fondo_azienda = versato_nel_fondo_ - versamento_lavoratore
    imponibile = calcola_imponibile(ral, versamento_lavoratore)
    irpef_netta = calcola_irpef_netta(imponibile)
    addizionale_comunale = calcola_addizionale_comunale(imponibile)
    addizionale_regionale = calcola_addizionale_regionale(imponibile)
    netto_annuo = calcola_netto_annuo(ral, versamento_lavoratore)
    return {
        'contributi': contributi,
        'versamento_lavoratore': versamento_lavoratore,
        'versato_nel_fondo': versato_nel_fondo_,
        'quota_fondo_azienda': quota_fondo_azienda,
        'imponibile': imponibile,
        'irpef_netta': irpef_netta,
        'addizionale_regionale': addizionale_regionale,
        'addizionale_comunale': addizionale_comunale,
        'netto_annuo': netto_annuo
    }

if __name__ == '__main__':
    print(calcola_netto_annuo(25000, 4500))
    print(calcola_netto_annuo(25000, 5000))
    print(calcola_netto_annuo(25000, 10000))

