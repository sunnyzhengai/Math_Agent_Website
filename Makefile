.PHONY: help ci test lint format clean install update-goldens serve telemetry analyze-telemetry build-docker run-docker docker-up docker-down eval eval-test eval-ci

help:
	@echo "Math Agent — Development Commands"
	@echo ""
	@echo "  make ci              Run all checks (tests + lint)"
	@echo "  make test            Run unit tests"
	@echo "  make lint            Check code quality"
	@echo "  make format          Auto-format code"
	@echo "  make update-goldens  Regenerate golden snapshots"
	@echo "  make serve           Run FastAPI server (localhost:8000)"
	@echo "  make telemetry       Tail telemetry log (Ctrl+C to exit)"
	@echo "  make analyze-telemetry  Analyze telemetry events"
	@echo "  make eval            Run agent eval harness (baseline)"
	@echo "  make eval-test       Run eval harness tests"
	@echo "  make eval-ci         Run eval tests + harness"
	@echo "  make build-docker    Build Docker image"
	@echo "  make run-docker      Run Docker container (port 8080)"
	@echo "  make docker-up       Start docker-compose stack (port 80)"
	@echo "  make docker-down     Stop docker-compose stack"
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

telemetry:
	@echo "📊 Tailing telemetry log (Ctrl+C to exit)..."
	@tail -f logs/telemetry.jsonl 2>/dev/null || echo "No telemetry log yet (run server first)"

analyze-telemetry:
	@echo "📈 Analyzing telemetry..."
	@python3 tools/analyze_telemetry.py logs/telemetry.jsonl

eval:
	@echo "🤖 Running agent eval harness (baseline)..."
	python3 -m agentic.evals.run_eval -v

eval-test:
	@echo "🧪 Running eval harness contract tests..."
	python3 -m pytest agentic/evals/test_eval_harness.py -v

eval-ci: eval-test eval
	@echo "✅ Agent eval CI passed!"

install:
	pip install -r requirements.txt
	@echo "✅ Dependencies installed!"

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	@echo "✅ Cache cleaned!"

build-docker:
	@echo "🐳 Building Docker image..."
	docker build -t math-agent:latest .
	@echo "✅ Docker image built!"

run-docker:
	@echo "🚀 Running Docker container on port 8080..."
	docker run --rm -p 8080:8080 -v "$(PWD)/logs:/app/logs" math-agent:latest

docker-up:
	@echo "🐳 Starting docker-compose stack (Nginx + API)..."
	docker-compose up -d
	@echo "✅ Stack up! Visit http://localhost"

docker-down:
	@echo "🛑 Stopping docker-compose stack..."
	docker-compose down
	@echo "✅ Stack down!"
