import h5py
import numpy as np
import pandas as pd

def get_matlab_string(f, ref):
    """
    Rozkodowuje ciąg znaków (string) z Matlaba zapisany w HDF5 przez referencję.
    """
    obj = f[ref]
    # Matlab zapisuje stringi jako pionowe wektory znaków ASCII
    return ''.join(chr(c[0]) for c in obj)

def parse_mat_dspace(file_path):
    try:
        with h5py.File(file_path, 'r') as f:
            # 1. Znajdź główną strukturę w pliku (omijamy folder techniczny '#refs#')
            root_keys = [k for k in f.keys() if k != '#refs#']
            if not root_keys:
                raise ValueError("Brak głównej struktury symulacji w pliku.")
            
            root_name = root_keys[0] # To będzie np. 'Wiatr20_Stac_Wyrz40'

            # 2. Pobierz Czas (on zawsze jest płaskim wektorem pod X/Data)
            time_data = np.array(f[root_name]['X']['Data']).flatten()

            # 3. Odpakuj wszystkie sygnały ze struktury Y
            y_names_refs = f[root_name]['Y']['Name']
            y_data_refs = f[root_name]['Y']['Data']

            signals = {}
            for i in range(len(y_names_refs)):
                # Odczytujemy prawdziwą nazwę sygnału (ukrytą pod wskaźnikiem)
                signal_name = get_matlab_string(f, y_names_refs[i, 0])
                # Odczytujemy wektor z danymi (ukryty pod wskaźnikiem)
                signal_data = np.array(f[y_data_refs[i, 0]]).flatten()
                
                signals[signal_name] = signal_data

            # --- 4. ZNAJDOWANIE WSPÓŁRZĘDNYCH ---
            dspace_keys = list(signals.keys())
            x_data, y_data, z_data = None, None, None

            # Sprawdzamy dokładnie to, o czym mówił prowadzący ("XYZ[0]", "XYZ[1]" itd.)
            if 'XYZ[0]' in signals and 'XYZ[1]' in signals and 'XYZ[2]' in signals:
                x_data, y_data, z_data = signals['XYZ[0]'], signals['XYZ[1]'], signals['XYZ[2]']
            
            # Może być też zapisane ze zwykłymi indeksami lub podkreślnikami
            else:
                # Wyłapujemy wszystkie sygnały, które mają "XYZ" w nazwie i sortujemy je alfabetycznie
                xyz_candidates = sorted([k for k in dspace_keys if 'XYZ' in k.upper()])
                
                if len(xyz_candidates) >= 3:
                    x_data = signals[xyz_candidates[0]]
                    y_data = signals[xyz_candidates[1]]
                    z_data = signals[xyz_candidates[2]]
                else:
                    # Jeśli z jakiegoś powodu dSPACE nazwało je zupełnie inaczej (np. 'Pos_X')
                    # Wypiszemy wszystkie dostępne nazwy sygnałów w pliku, żeby łatwo to zmienić!
                    print(f"\nBŁĄD ZNALEZIENIA KLUCZY XYZ! Dostępne nazwy sygnałów to:\n{dspace_keys}")
                    return pd.DataFrame()

            # 5. Tworzenie DataFramu (obcinamy do najkrótszej listy na wypadek błędów dSPACE)
            min_len = min(len(time_data), len(x_data), len(y_data), len(z_data))

            df = pd.DataFrame({
                'time': time_data[:min_len],
                'x': x_data[:min_len],
                'y': y_data[:min_len],
                'z': z_data[:min_len]
            })

            return df

    except Exception as e:
        print(f"KRYTYCZNY BŁĄD PARSERA: {e}")
        return pd.DataFrame()