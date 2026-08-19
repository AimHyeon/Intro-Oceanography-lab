from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"

files = [
    DATA_DIR / "summer_salinity.csv",
    DATA_DIR / "winter_salinity.csv",
    DATA_DIR / "summer_temperature.csv",
    DATA_DIR / "winter_temperature.csv"
]

coordinates = []

for file in files:
    df = pd.read_csv(file, skiprows=2, header=None)

    lat = pd.to_numeric(df.iloc[:, 0], errors="coerce")
    lon = pd.to_numeric(df.iloc[:, 1], errors="coerce")

    coords = {
        (lat, lon)
        for lat, lon in zip(lat, lon)
        if pd.notna(lat) and pd.notna(lon)
    }

    coordinates.append(coords)

common_coordinates = set.intersection(*coordinates)

summer_temp = pd.read_csv(
    DATA_DIR / "summer_temperature.csv",
    skiprows=2,
    header=None
)

summer_temp.iloc[:, 0] = pd.to_numeric(
    summer_temp.iloc[:, 0],
    errors="coerce"
)

summer_temp.iloc[:, 1] = pd.to_numeric(
    summer_temp.iloc[:, 1],
    errors="coerce"
)

summer_temp.iloc[:, 2] = pd.to_numeric(
    summer_temp.iloc[:, 2],
    errors="coerce"
)

results = []

for lat, lon in common_coordinates:

    row = summer_temp[
        (summer_temp.iloc[:, 0] == lat) &
        (summer_temp.iloc[:, 1] == lon)
    ]

    if not row.empty:
        temp_0m = row.iloc[0, 2]

        results.append({
            "위도": lat,
            "경도": lon,
            "여름 0m 수온": temp_0m
        })

results = sorted(
    results,
    key=lambda x: x["여름 0m 수온"],
    reverse=True
)

print("4개 파일에서 일치하는 경위도")

for result in results:
    print(
        f"위도: {result['위도']}, "
        f"경도: {result['경도']}, "
        f"여름 0m 수온: {result['여름 0m 수온']}"
    )