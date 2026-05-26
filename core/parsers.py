import pandas as pd
import struct

def parse_excel(file_path):
    try:
        settings_df = pd.read_excel(file_path, 'Ustawienia')
        measure_df = pd.read_excel(file_path, 'Pomiary')
    except Exception as e:
        print(f"problem with reading excel file {file_path} - {e}")

    settings_dict = {}

    for row in settings_df.itertuples():
        settings_dict[row.Parametr] =  row.Wartosc
    
    measure_df = measure_df.where(pd.notnull(measure_df), None)

    return settings_dict, measure_df

def parse_binary(file_path):
    binary_data = ""
    rows = []
    try:
        with open(file_path, 'rb') as f:
            header_data = f.read(64)
            nazwa1_b, nazwa2_b = struct.unpack('32s32s', header_data)
            
            param1 = nazwa1_b.decode('utf-8').strip('\x00')
            param2 = nazwa2_b.decode('utf-8').strip('\x00')

            binary_data = f.read()
    except Exception as e:
        print(f"problem with reading binary file {file_path} - {e}")
    
    for record in struct.iter_unpack('<dffi', binary_data):
        rows.append({'czas':record[0], param1:record[1], param2:record[2], 
                'flaga_walidacji': record[3]})

    df = pd.DataFrame(rows)
    return df


if __name__ == "__main__":
    ustawienia, pomiary = parse_excel("test_data/symulacja_wezla_01.xlsx") 
    wynik = parse_binary("test_data/wyniki_turbiny_01.bin")
    print(wynik)
    # print("Ustawienia:", ustawienia)
    # print("Pomiary (pierwsze 5 wierszy):")
    # print(pomiary)

    