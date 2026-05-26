import pandas as pd 
from pydantic import BaseModel, model_validator, ValidationError
from typing import Dict, Optional
import math

class UniversalRecord(BaseModel):
    time: float
    value: Dict[str, float] 
    validation_flag: Optional[int] = 1 

    @model_validator(mode='after')
    def check_universal_rules(self):
        if self.validation_flag == 0:
            raise ValueError("system error - validation flag is 0")

        for key, val in self.value.items():
            if math.isnan(val) or (val > 10000 or val < -10000):
                raise ValueError(f"anomaly in column {key} : {val}")
        return self
    
def validate_dataframe(df):
    valid_rows = []
    invalid_rows = []

    for row in df.itertuples():
        row_data = row._asdict()
        
        row_data.pop('Index', None)
        
        time = row_data.pop('Czas_symulacji', row_data.pop('czas', 0.0))
        validation_flag = row_data.pop('flaga_walidacji', 1) 

        try:
            rekord = UniversalRecord(time=time, value=row_data, validation_flag=validation_flag)
            
            valid_rows.append(rekord.model_dump())
            
        except ValidationError as e:
            invalid_rows.append({
                'czas': time,
                'szczegoly_bledu': e.errors()[0]['msg'],
                'oryginalne_dane': str(row_data)
            })

    return valid_rows, invalid_rows

if __name__ == "__main__":
    # Importujemy parsery z naszego drugiego pliku
    from parsers import parse_excel, parse_binary

    print("=== TEST EXCEL ===")
    ustawienia, pomiary_df = parse_excel("test_data/symulacja_wezla_01.xlsx")
    
    valid_excel, invalid_excel = validate_dataframe(pomiary_df)
    
    print(f"✅ Poprawne wiersze: {len(valid_excel)}")
    print(f"❌ Od rzucone wiersze: {len(invalid_excel)}")
    for err in invalid_excel:
        print(" -> SZCZEGÓŁY BŁĘDU:", err)


    print("\n=== TEST BINARNY ===")
    binary_df = parse_binary("test_data/wyniki_turbiny_01.bin")
    
    valid_bin, invalid_bin = validate_dataframe(binary_df)
    
    print(f"✅ Poprawne wiersze: {len(valid_bin)}")
    print(f"❌ Odrzucone wiersze: {len(invalid_bin)}")
    for err in invalid_bin:
        print(" -> SZCZEGÓŁY BŁĘDU:", err)