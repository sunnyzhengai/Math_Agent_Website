.PHONY: help ci test lint format clean install update-goldens serve

help:
	@echo "Math Agent — Development Commands"
	@echo ""
	@echo "  make ci              Run all checks (tests + lint)"
	@echo "  make test            Run unit tests"
	@echo "  make lint            Check code quality"
	@echo "  make format          Auto-format code"
	@echo "  make update-goldens  Regenerate golden snapshots"
	@echo "  make serve           Run FastAPI server (localhost:8000)"
	@echo "  make install         Install dependencies"
	@echo "  make clean           Remove cache files"

ci: lint test
	@echo "✅ CI passed!"

test:
	@echo "🧪 Running tests..."
	python3 -m pytest tests/ -v

lint:
	@echo "🔍 Linting..."
	python3 -m pylint engine/ api/ tests/ --disable=C0111,C0103 || true
	@echo "📝 Type checking..."
	python3 -m mypy engine/ api/ || true

format:
	@echo "✨ Formatting..."
	python3 -m black engine/ api/ tests/

update-goldens:
	@echo "📸 Regenerating golden snapshots..."
	python3 -c "import json; from engine.templates import generate_item; item = generate_item('quad.graph.vertex', 'easy', seed=42); open('tests/goldens/golden_item_quad_graph_vertex_easy_42.json', 'w').write(json.dumps(item, indent=2))"
	@echo "✅ Golden updated"

serve:
	@echo "🚀 Starting FastAPI server..."
	python3 -m uvicorn api.server:app --reload --host 0.0.0.0 --port 8000

install:
	pip install -r requirements.txt
	@echo "✅ Dependencies installed!"

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	@echo "✅ Cache cleaned!"
