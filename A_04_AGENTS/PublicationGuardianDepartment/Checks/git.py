from .base import Inspector


class GitInspector(Inspector):
    inspector_id = "git"

    def run(self, context, policy):
        if context.request.publication_mode.casefold() != "git":
            return [], []
        if context.source != "git-index":
            return [self.finding(
                "GIT_INDEX_NOT_USED", "BLOCK", "Git-публикация сформирована не из индекса.",
                "Повторите проверку на основе git diff --cached.",
            )], []
        if not context.git_integrity_ok:
            raise RuntimeError("Git index integrity could not be established")
        return [], []
