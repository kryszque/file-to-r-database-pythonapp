import math
import pandas as pd
from pydantic import BaseModel, model_validator, ValidationError

class TrajectoryRecord(BaseModel):
    time: float
    x: float
    y: float
    z: float

    @model_validator(mode='after')
    def check_physics(self):
        # sprawdzenie osi X Y Z
        for val, axis in [(self.x, 'X'), (self.y, 'Y'), (self.z, 'Z')]:
            if math.isnan(val):
                raise ValueError(f"Brak danych (NaN) w osi {axis}")
            if abs(val) > 1e6:
                raise ValueError(f"Anomalia fizyczna: oś {axis} = {val} (przekroczono limit 1e6)")
        
        # sprawdzenie czasu
        if math.isnan(self.time) or self.time < 0:
            raise ValueError(f"Nieprawidłowy czas symulacji: {self.time}")
            
        return self

def validate_dataframe(df):
    valid_rows = []
    invalid_rows = []

    if df.empty:
        return valid_rows, invalid_rows

    for row in df.itertuples(index=False):
        row_dict = row._asdict()
        try:
            record = TrajectoryRecord(**row_dict)
            valid_rows.append(record.model_dump())
        except ValidationError as e:
            # czytelna wiadomosc o bledzie
            err_msg = e.errors()[0]['msg'] if 'msg' in e.errors()[0] else str(e)
            invalid_rows.append({
                'czas': row_dict.get('time', 0.0),
                'szczegoly_bledu': err_msg,
                'oryginalne_dane': str(row_dict)
            })

    return valid_rows, invalid_rows