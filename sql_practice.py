import duckdb
import pandas as pd
pd.set_option('display.max_columns', None)

vehicles = pd.DataFrame({
    "vehicle_id": [1, 2, 3, 4],
    "model": ["ModelX", "ModelY", "ModelX", "ModelZ"],
    "release_version": ["2024.05", "2024.12", "2024.09", "2024.11"]
})
print(vehicles)

trips = pd.DataFrame({
    "trip_id": [101, 102, 103, 104, 105, 106],
    "vehicle_id": [1, 1, 2, 3, 3, 4],
    "start_time": pd.to_datetime([
        "2026-05-01 08:00",
        "2026-05-01 18:00",
        "2026-05-02 09:00",
        "2026-05-03 10:00",
        "2026-05-03 18:00",
        "2026-05-04 12:00"
    ]),
    "end_time": pd.to_datetime([
        "2026-05-01 08:30",
        "2026-05-01 18:45",
        "2026-05-02 09:40",
        "2026-05-03 10:50",
        "2026-05-03 18:40",
        "2026-05-04 12:30"
    ]),
    "miles": [10, 15, 20, 12, 18, 25]
})

print(trips)

disengagements = pd.DataFrame({
    "disengage_id": [1001, 1002, 1003, 1004, 1005],
    "trip_id": [101, 101, 103, 104, 106],
    "timestamp": pd.to_datetime([
        "2026-05-01 08:10",
        "2026-05-01 08:25",
        "2026-05-02 09:20",
        "2026-05-03 10:30",
        "2026-05-04 12:10"
    ]),
    "reason": [
        "camera_failure",
        "lidar_failure",
        "radar_failure",
        "camera_failure",
        "lidar_failure"
    ]
})

print(disengagements)

sensor_events = pd.DataFrame({
    "event_id": [1,2,3,4,5,6,7,8],
    "vehicle_id": [1,1,2,2,3,3,4,4],
    "event_time": pd.to_datetime([
        "2026-05-01 08:05",
        "2026-05-01 18:20",
        "2026-05-02 09:10",
        "2026-05-02 09:35",
        "2026-05-03 10:25",
        "2026-05-03 18:10",
        "2026-05-04 12:05",
        "2026-05-04 12:20"
    ]),
    "event_type": [
        "camera_failure",
        "lidar_failure",
        "radar_failure",
        "camera_failure",
        "lidar_failure",
        "radar_failure",
        "camera_failure",
        "lidar_failure"
    ]
})

print(sensor_events)

print('=========================================')

df = duckdb.sql("""
select v.model,
sum(t.miles) as total_miles
from trips t
left join vehicles v -- TODO:
on t.vehicle_id = v.vehicle_id
group by v.model
""").df()
print(df)