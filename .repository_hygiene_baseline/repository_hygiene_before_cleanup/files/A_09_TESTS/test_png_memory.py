from A_07_MEMORY.png_workflow_memory import PNGWorkflowMemory

m = PNGWorkflowMemory()

m.register(
    "dragon.png",
    "fantasy_workflow.json"
)

print(
    m.get_workflow(
        "dragon.png"
    )
)
