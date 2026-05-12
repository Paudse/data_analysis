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

for df, col in [
    (trips, "start_time"),
    (trips, "end_time"),
    (disengagements, "timestamp"),
    (sensor_events, "event_time")
]:
    df[col] = pd.to_datetime(df[col])


print('=========================================')
df = trips.merge(disengagements, on="trip_id", how="left")
print("df:\n", df)

res = (df.groupby("vehicle_id", as_index=False)["miles"])
print("res:\n", res)

df = trips.merge(vehicles, on = "vehicle_id", how = "left")

res = (
    df.groupby("model", as_index = False)["miles"]
    .sum()
    .rename(columns={"miles":"total_miles"})
)

print(res)

df = trips.merge(disengagements, on = "trip_id", how = "left")

res = (
    df.groupby("vehicle_id")["disengage_id"]
    .count()
    .reset_index(name="disengage_count")
)
print(res)

res = (
    df.groupby("vehicle_id")["disengage_id"]
    .count()
    .reset_index(name="disengage_count")
)

trip_cnt = trips.groupby("vehicle_id").size().rename("trip_count")
print(trip_cnt)

diseng_cnt = (
    trips.merge(disengagements, on = "trip_id", how = "left")
    .groupby("vehicle_id")["disengage_id"]
    .count()
    .rename("diseng_count")
)

res = (
    pd.concat([trip_cnt, diseng_cnt], axis=1)
    .assign(diseng_rate=lambda x: x.diseng_count / x.trip_count)
    # .reset_index()
)

print(res)

res = (
    pd.concat([trip_cnt, diseng_cnt], axis=1)
    .assign(diseng_rate=lambda x: x.diseng_count / x.trip_count)
    .reset_index()
)

print(res)

res = (
    sensor_events["event_type"]
    .value_counts()
    .reset_index(name="count")
    .rename(columns={"index":"event_type"})
    .head(1)
)
print(res)

miles = trips.groupby("vehicle_id")["miles"].sum()
diseng = (
    trips.merge(disengagements, on = "trip_id", how = "left")
    .groupby("vehicle_id")["disengage_id"]
    .count()
)

res = (
    pd.concat([miles, diseng], axis=1)
    .rename(columns={"miles":"total_miles","disengage_id":"diseng"})
    .assign(instability=lambda x: x.diseng*1000/x.total_miles)
    .sort_values("instability", ascending=False)
    .head(3)
    .reset_index()
)

print(res)



