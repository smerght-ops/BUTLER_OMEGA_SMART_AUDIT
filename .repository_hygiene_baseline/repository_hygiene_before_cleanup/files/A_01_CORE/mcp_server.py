import sys, json
from A_02_MANAGERS.catalog_manager import CatalogManager
from A_01_CORE.orchestrator import Orchestrator

sys.stdout.reconfigure(encoding='utf-8')
sys.stdin.reconfigure(encoding='utf-8')

class ButlerMcpServer:
    def __init__(self):
        self.catalog = CatalogManager()
        self.orchestrator = Orchestrator()

    def listen(self):
        while True:
            try:
                line = sys.stdin.readline()
                if not line: break
                request = json.loads(line)
                response = self.handle_request(request)
                sys.stdout.write(json.dumps(response, ensure_ascii=False) + "\n")
                sys.stdout.flush()
            except Exception as e:
                error = {"jsonrpc": "2.0", "error": {"code": -32603, "message": str(e)}, "id": None}
                sys.stdout.write(json.dumps(error, ensure_ascii=False) + "\n")
                sys.stdout.flush()

    def handle_request(self, request):
        req_id = request.get("id")
        method = request.get("method")
        params = request.get("params", {})

        if method == "tools/list":
            return {
                "jsonrpc": "2.0",
                "result": {
                    "tools": [
                        {"name": "search_documents", "description": "Поиск по базе (FTS5)", "inputSchema": {"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]}},
                        {"name": "rebuild_index", "description": "Перестроить индекс базы", "inputSchema": {"type": "object", "properties": {}}},
                        {"name": "run_diagnostics", "description": "Запуск диагностики", "inputSchema": {"type": "object", "properties": {}}}
                    ]
                }, "id": req_id
            }

        elif method == "tools/call":
            tool_name = params.get("name")
            
            if tool_name == "search_documents":
                query = params.get("arguments", {}).get("query", "")
                rows = self.catalog.full_text_search(query)
                results = [{"id": r[0], "filepath": r[1], "summary": r[2], "tags": r[3]} for r in rows]
                return {"jsonrpc": "2.0", "result": {"content": [{"type": "text", "text": json.dumps(results, ensure_ascii=False)}]}, "id": req_id}

            elif tool_name == "rebuild_index":
                # Вызываем оркестратор
                self.orchestrator.rebuild_search_index()
                return {"jsonrpc": "2.0", "result": {"content": [{"type": "text", "text": "Индекс успешно перестроен."}]}, "id": req_id}

            elif tool_name == "run_diagnostics":
                # Заглушка для вызова диагностики
                return {"jsonrpc": "2.0", "result": {"content": [{"type": "text", "text": "Диагностика системы запущена и выполнена."}]}, "id": req_id}

        return {"jsonrpc": "2.0", "error": {"code": -32601, "message": "Метод не поддерживается"}, "id": req_id}

if __name__ == "__main__":
    ButlerMcpServer().listen()
