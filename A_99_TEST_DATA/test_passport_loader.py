from A_07_CONFIG.project_passport_loader import ProjectPassportLoader

p = ProjectPassportLoader()

print("STAGE =", p.current_stage())
print("IDENTITY =", p.project_identity())
print("FROZEN =", p.frozen_modules())
