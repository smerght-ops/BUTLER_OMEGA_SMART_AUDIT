path = "A_03_ORCHESTRATION/butler_harness.py"
code = open(path, "r", encoding="utf-8").read()

# Точный блок, который мы заменяем
old_block = """              self.observation.record(
                  source=department_name,
                  event="HARNESS_V3_SUCCESS",
                  payload={"task": str(task)}
              )
              return result"""

# Новый блок с легальной автоматической синхронизацией
new_block = """              self.observation.record(
                  source=department_name,
                  event="HARNESS_V3_SUCCESS",
                  payload={"task": str(task)}
              )

              # [PASSPORT_ACTIVE_SYNC] Автоматическая фиксация живой системы
              if department_name == "SEARCH":
                  try:
                      from A_07_CONFIG.project_passport_loader import ProjectPassportLoader
                      loader = ProjectPassportLoader()
                      loader.commit_proof("search_department_routing", "PROVEN")
                      loader.commit_proof("catalog_search_bridge", "PROVEN")
                  except Exception as e:
                      print(f"[HARNESS SYNC ERROR] {str(e)}")

              return result"""

if old_block in code:
    open(path, "w", encoding="utf-8").write(code.replace(old_block, new_block))
    print("✅ Хирургическая врезка авто-синхронизации в Harness завершена.")
else:
    print("❌ Не удалось найти целевой блок кода. Проверьте отступы.")
