import os
import struct
import pandas as pd
import random

# Ustawienia ścieżek
OUTPUT_DIR = "test_data"
EXCEL_FILENAME = "symulacja_wezla_01.xlsx"
BINARY_FILENAME = "wyniki_turbiny_01.bin"

def create_excel_data(filepath):
    print(f"Generowanie pliku Excel: {filepath}...")
    
    # 1. Arkusz: Ustawienia (Metadane)
    ustawienia_data = {
        'Parametr': ['tryb_pracy', 'temp_zadana', 'cisnienie_max', 'ID_wezla'],
        'Wartosc': ['Eko', 65.0, 4.5, 104]
    }
    df_ustawienia = pd.DataFrame(ustawienia_data)

    # 2. Arkusz: Pomiary (Seria czasowa)
    pomiary_data = {
        'Czas_symulacji': [],
        'Temperatura': [],
        'Cisnienie': [],
        'Przeplyw': []
    }

    # Generujemy 50 poprawnych wierszy
    
    for i in range(50):
        czas = i * 0.5
        temp = 20.0 + (i * 0.5) + random.uniform(-1, 1) # Rosnąca temperatura
        cisn = 1.0 + (i * 0.05) + random.uniform(-0.1, 0.1)
        przeplyw = 3.0 + random.uniform(-0.5, 0.5)

        pomiary_data['Czas_symulacji'].append(czas)
        pomiary_data['Temperatura'].append(round(temp, 2))
        pomiary_data['Cisnienie'].append(round(cisn, 2))
        pomiary_data['Przeplyw'].append(round(przeplyw, 2))

    # --- WSTRZYKIWANIE BŁĘDÓW (Anomalie dla ETL) ---
    # Błąd 1: Ujemna temperatura (fizycznie niemożliwe w tym układzie)
    pomiary_data['Temperatura'][10] = -99.0 
    
    # Błąd 2: Krytyczne ciśnienie (powyżej zakresu 10.0 bar)
    pomiary_data['Cisnienie'][25] = 99.9 
    
    # Błąd 3: Brakujące dane (NaN) w przepływie
    pomiary_data['Przeplyw'][40] = None

    df_pomiary = pd.DataFrame(pomiary_data)

    # Zapis do pliku Excel z wieloma arkuszami
    with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
        df_ustawienia.to_excel(writer, sheet_name='Ustawienia', index=False)
        df_pomiary.to_excel(writer, sheet_name='Pomiary', index=False)
    
    print(" Zakończono generowanie Excela.")

def create_binary_data(filepath):
    print(f"Generowanie pliku binarnego: {filepath}...")
    
    # Format struct: 'd' (float64, 8 bajtów), 'f' (float32, 4 bajty), 'f', 'i' (int32, 4 bajty)
    # Znak '<' oznacza Little-Endian (standard zapisu pamięci w PC)
    record_format = '<dffi' 
    
    with open(filepath, 'wb') as bin_file:
        param1_name = "Moc_generatora".encode('utf-8')
        param2_name = "Obroty_wirnika".encode('utf-8')
    
        header = struct.pack('32s32s', param1_name, param2_name)
        bin_file.write(header)
        for i in range(50):
            sim_time = float(i * 0.5)
            power = 1500.0 + random.uniform(-50, 50)
            rpm = 3000.0 + random.uniform(-10, 10)
            status_flag = 1  # 1 = OK
            
            # --- WSTRZYKIWANIE BŁĘDÓW ---
            if i == 15:
                status_flag = 0  # Błąd czujnika
            if i == 30:
                power = 9999.0   # Kosmiczna moc układu

            # Pakowanie zmiennych Pythona do surowych bajtów
            packed_data = struct.pack(record_format, sim_time, power, rpm, status_flag)
            bin_file.write(packed_data)
            
    print(" Zakończono generowanie pliku binarnego.")

if __name__ == '__main__':
    # Upewniamy się, że folder docelowy istnieje
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        
    excel_path = os.path.join(OUTPUT_DIR, EXCEL_FILENAME)
    binary_path = os.path.join(OUTPUT_DIR, BINARY_FILENAME)
    
    create_excel_data(excel_path)
    create_binary_data(binary_path)
    
    print(f"\nSukces! Pliki testowe znajdują się w folderze '{OUTPUT_DIR}'.")