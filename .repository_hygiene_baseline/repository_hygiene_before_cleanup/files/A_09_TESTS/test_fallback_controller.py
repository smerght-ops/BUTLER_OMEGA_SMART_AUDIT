from A_03_ORCHESTRATION.fallback_controller import FallbackController

f = FallbackController()

f.register(
    "IMAGE",
    lambda: "IMAGE_FALLBACK_OK"
)

print(
    f.run(
        "IMAGE",
        "ComfyUI offline"
    )
)

print(
    f.run(
        "CODING",
        "Ollama offline"
    )
)
