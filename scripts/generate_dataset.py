import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Ustawienie ziarna losowości, aby dane były powtarzalne
np.random.seed(42)

n_records = 2000

# 1. Słowniki i bazy danych do losowania
dostawcy_cfg = {
    'Budimex Sp. z o.o.': {'waga': 0.25, 'min_kwota': 5000, 'max_kwota': 80000, 'akceptant': 'Jan Kowalski'},
    'Arrow Electronics': {'waga': 0.20, 'min_kwota': 10000, 'max_kwota': 50000, 'akceptant': 'Marek Wiśniewski'},
    'OfficeDepot': {'waga': 0.20, 'min_kwota': 300, 'max_kwota': 4000, 'akceptant': 'Anna Nowak'},
    'CleanCo': {'waga': 0.15, 'min_kwota': 600, 'max_kwota': 1500, 'akceptant': 'Anna Nowak'},
    'Deli Sp. z o.o.': {'waga': 0.20, 'min_kwota': 50, 'max_kwota': 495, 'akceptant': ''}
    # Dla małych kwot brak akceptanta (auto)
}

dostawcy_list = list(dostawcy_cfg.keys())
wag_list = [dostawcy_cfg[d]['waga'] for d in dostawcy_list]

# 2. Generowanie dat wpływu (Ostatnie 3 miesiące: marzec - maj 2026)
start_date = datetime(2026, 3, 1)
end_date = datetime(2026, 5, 31)
dni_zakresu = (end_date - start_date).days

# Generujemy losowe daty wpływu i sortujemy je chronologicznie
daty_wplywu = [start_date + timedelta(days=int(np.random.randint(0, dni_zakresu))) for _ in range(n_records)]
daty_wplywu.sort()

# 3. Główna pętla generująca dane
data = []
for i in range(n_records):
    id_doc = i + 1

    # Losowanie dostawcy na podstawie wag rynkowych
    dostawca = np.random.choice(dostawcy_list, p=wag_list)
    cfg = dostawcy_cfg[dostawca]

    nr_faktury = f"FV/2026/{daty_wplywu[i].strftime('%m')}/{1000 + id_doc}"
    wartosc_brutto = round(np.random.uniform(cfg['min_kwota'], cfg['max_kwota']), 2)
    data_wplywu = daty_wplywu[i]

    # Logika 3-Way Matching (Poltext generował błędy cenowe, zasymulujmy ogólny błąd dla ~12% faktur powyżej 500 zł)
    czy_przeszla_3wm = 'TAK'
    powod_3wm = ''

    if wartosc_brutto > 500 and np.random.rand() < 0.12:
        czy_przeszla_3wm = 'NIE'
        powod_3wm = np.random.choice(['Błąd cenowy ZZ vs FV', 'Brak dokumentu PZ'])

    # Określenie statusu bieżącego na podstawie daty wpływu (końcówka maja może wciąż wisieć w systemie)
    roznica_od_dzis = (datetime(2026, 6, 1) - data_wplywu).days

    biezacy_status = 'Zaksięgowana'
    akceptant = cfg['akceptant']
    data_zaksiegowania = None
    czas_akceptacji = None
    lead_time = None

    # Logika procesowa opóźnień:
    if biezacy_status == 'Zaksięgowana':
        # Jeśli faktura miała błąd 3WM, proces trwał dłużej
        dni_na_3wm = np.random.randint(5, 12) if czy_przeszla_3wm == 'NIE' else 1

        # Jeśli kwota <= 500, brak czasu akceptacji (automatyczne księgowanie)
        if wartosc_brutto <= 500:
            czas_akceptacji = 0
            lead_time = dni_na_3wm
        else:
            # Sztuczna anomalia: Marek Wiśniewski (Dyrektor IT) w maju (05) był na urlopie i generował opóźnienia
            if akceptant == 'Marek Wiśniewski' and data_wplywu.month == 5:
                czas_akceptacji = np.random.randint(14, 25)  # Urlopowe wąskie gardło
            else:
                czas_akceptacji = np.random.randint(1, 5)  # Normalny czas akceptacji

            lead_time = dni_na_3wm + czas_akceptacji

        data_zaksiegowania = data_wplywu + timedelta(days=int(lead_time))

    # Jeśli faktura wpłynęła na sam koniec maja, oznaczamy ją jako "w toku" (czyli jeszcze nie zaksięgowana na dzień 1 czerwca)
    if roznica_od_dzis <= 7 and np.random.rand() < 0.6:
        if czy_przeszla_3wm == 'NIE':
            biezacy_status = 'Wyjaśnienie błędu'
        else:
            biezacy_status = 'Oczekuje na akceptacje'
        data_zaksiegowania = ''
        czas_akceptacji = ''
        lead_time = ''
    else:
        # Formatowanie dat do zapisu tekstowego
        data_zaksiegowania = data_zaksiegowania.strftime('%Y-%m-%d')

    data_wplywu_str = data_wplywu.strftime('%Y-%m-%d')

    data.append([
        id_doc, nr_faktury, dostawca, wartosc_brutto, data_wplywu_str,
        czy_przeszla_3wm, powod_3wm, biezacy_status, akceptant,
        data_zaksiegowania, czas_akceptacji, lead_time
    ])

# 4. Tworzenie DataFrame i zapis do pliku CSV ze średnikiem
columns = [
    'ID', 'NR_FAKTURY', 'DOSTAWCA', 'WARTOSC_BRUTTO', 'DATA_WPLYWU',
    'CZY_PRZESZLA_3WM', 'POWOD_NIEPRZYJECIA_3WM', 'BIEZACY_STATUS', 'OSOBY_AKCEPTUJACE',
    'DATA_ZAKSIEGOWANIA', 'CZAS_AKCEPTACJI', 'CAKOWITY_CZAS_OBIEGU'
]

df = pd.DataFrame(data, columns=columns)
df.to_csv('faktury_wymiar_2000.csv', sep=';', index=False, encoding='utf-8')

print("Sukces! Plik 'faktury_wymiar_2000.csv' został pomyślnie wygenerowany i zawiera 2000 rekordów.")