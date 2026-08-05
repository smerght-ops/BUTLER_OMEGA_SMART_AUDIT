from A_03_ORCHESTRATION.observation_layer import ObservationLayer

o = ObservationLayer()

print(
    o.record(
        source="TEST",
        event="START",
        payload={"hello":"world"}
    )
)
