from A_03_ORCHESTRATION.dps_vdk import DPSVDK

d = DPSVDK()

print(
    d.check("DELETE_PROJECT")
)

print(
    d.check("CREATE_IMAGE")
)
