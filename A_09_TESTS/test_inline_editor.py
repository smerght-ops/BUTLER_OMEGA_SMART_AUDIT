from A_03_ORCHESTRATION.editor_patch import InlineCodeEditor

e = InlineCodeEditor()

r = e.preview_replace(
    "A_00_ARCHITECTURE\\ACTIVE_SYSTEM.md",
    "ENTRY POINT",
    "ENTRY POINT"
)

print(r)
