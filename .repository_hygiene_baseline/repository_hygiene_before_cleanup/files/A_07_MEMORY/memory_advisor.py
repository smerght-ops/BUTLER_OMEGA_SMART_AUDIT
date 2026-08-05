import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from A_07_MEMORY.search_engine import SemanticSearchEngine

class MemoryAdvisor:

    def __init__(self):
        self.engine = SemanticSearchEngine()

    def analyze(self):
        stats = self.engine.memory_stats()

        recommendations = []

        ratio = stats.get("cache_hit_ratio", 0)

        if ratio < 30:
            recommendations.append(
                "Increase cache usage or review repeated queries."
            )

        if stats.get("cache_entries", 0) > 240:
            recommendations.append(
                "Cache is close to configured limit."
            )

        if stats.get("synonyms", 0) < 20:
            recommendations.append(
                "Expand synonym dictionary."
            )

        if stats.get("documents", 0) == 0:
            recommendations.append(
                "Memory index appears empty."
            )

        if not recommendations:
            recommendations.append(
                "Memory subsystem looks healthy."
            )

        return {
            "stats": stats,
            "recommendations": recommendations
        }


if __name__ == "__main__":
    advisor = MemoryAdvisor()
    report = advisor.analyze()

    print("=" * 60)
    print("BUTLER MEMORY ADVISOR")
    print("=" * 60)

    for k, v in report["stats"].items():
        print(f"{k:20}: {v}")

    print()
    print("Recommendations:")

    for item in report["recommendations"]:
        print(f" - {item}")
