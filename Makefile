.PHONY: help ci test lint format clean install update-goldens serve telemetry analyze-telemetry build-docker run-docker docker-up docker-down eval eval-test eval-ci eval-agent eval-matrix eval-diversity eval-uniqueness eval-coverage eval-variation eval-calibration eval-all-quality audit-templates

agent ?= rules
cases ?=

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
	@echo "  make eval            Run agent eval harness (oracle)"
	@echo "  make eval-test       Run eval harness tests"
	@echo "  make eval-ci         Run eval tests + harness"
	@echo "  make eval-agent      Run eval with specific agent (e.g. make eval-agent agent=random)"
	@echo "  make eval-matrix     Compare all agents (oracle, random, always_a, rules)"
	@echo ""
	@echo "Quality Evals (Phase 0):"
	@echo "  make eval-diversity      Check question diversity (no repetition)"
	@echo "  make eval-uniqueness     Check for consecutive duplicates"
	@echo "  make eval-coverage       Verify all templates get used"
	@echo "  make eval-variation      Check parameter variation (Phase 2)"
	@echo "  make eval-calibration    Test difficulty calibration"
	@echo "  make eval-all-quality    Run all quality evals"
	@echo "  make audit-templates     Generate template inventory report"
	@echo ""
	@echo "Phase 2 Evals (Parameterized Generation):"
	@echo "  make eval-parameter-diversity   Check parameter uniqueness & coverage"
	@echo "  make eval-correctness           Verify 100% oracle accuracy"
	@echo "  make eval-distractor-quality    Check distractor plausibility"
	@echo "  make eval-phase2                Run all Phase 2 evals"
	@echo ""
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
	@echo "🤖 Running agent eval harness (oracle)..."
	python3 -m agentic.evals.run_eval --agent oracle

eval-test:
	@echo "🧪 Running eval harness contract tests..."
	python3 -m pytest agentic/evals/test_eval_agents.py agentic/agents/test_agents.py -v

eval-ci: eval-test eval
	@echo "✅ Agent eval CI passed!"

eval-agent:
	@echo "🤖 Running eval with agent: $(agent) $(if $(cases),cases=$(cases),)"
	python3 -m agentic.evals.run_eval --agent $(agent) $(if $(cases),--cases $(cases),)

eval-matrix:
	@echo "📊 Running agent comparison matrix..."
	python3 -m agentic.evals.run_eval --agent oracle --out agentic/evals/report.oracle.jsonl
	python3 -m agentic.evals.run_eval --agent random --out agentic/evals/report.random.jsonl
	python3 -m agentic.evals.run_eval --agent always_a --out agentic/evals/report.always_a.jsonl
	@echo "📊 Reports written to agentic/evals/"

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

# Evaluation Infrastructure
.PHONY: eval-all eval-coverage eval-freshness eval-latency eval-telemetry eval-validity

eval-all: ## Run all evaluation checks
	@echo "🔍 Running all evaluations..."
	@python3 -m evals.run_coverage_eval && \
	 python3 -m evals.run_dataset_freshness_eval && \
	 python3 -m evals.run_latency_eval && \
	 python3 -m evals.run_telemetry_eval && \
	 python3 -m evals.run_validity_eval && \
	 echo "✅ All evaluations passed!"

eval-coverage: ## Check skill/difficulty coverage
	python3 -m evals.run_coverage_eval

eval-freshness: ## Check dataset freshness
	python3 -m evals.run_dataset_freshness_eval

eval-latency: ## Check API latency metrics
	python3 -m evals.run_latency_eval

eval-telemetry: ## Check telemetry completeness
	python3 -m evals.run_telemetry_eval

eval-validity: ## Check generated item validity
	python3 -m evals.run_validity_eval

# Quality Evaluation Targets (Phase 0)
eval-diversity:
	@echo "📊 Running diversity eval..."
	python3 evals/run_diversity_eval.py

eval-uniqueness:
	@echo "🔄 Running uniqueness eval..."
	python3 evals/run_uniqueness_eval.py

eval-coverage:
	@echo "📈 Running coverage eval..."
	python3 evals/run_coverage_eval.py

eval-variation:
	@echo "🎲 Running variation eval..."
	python3 evals/run_variation_eval.py

eval-calibration:
	@echo "🎯 Running calibration eval..."
	python3 evals/run_calibration_eval.py

eval-all-quality: eval-diversity eval-uniqueness eval-coverage eval-variation eval-calibration
	@echo "✅ All quality evals complete!"

# Phase 2 Evaluation Targets (Parameterized Generation)
eval-parameter-diversity:
	@echo "🎲 Running parameter diversity eval..."
	python3 evals/run_parameter_diversity_eval.py

eval-correctness:
	@echo "✅ Running correctness eval..."
	python3 evals/run_correctness_eval.py

eval-distractor-quality:
	@echo "🎯 Running distractor quality eval..."
	python3 evals/run_distractor_quality_eval.py

eval-phase2: eval-parameter-diversity eval-correctness eval-distractor-quality
	@echo "✅ All Phase 2 evals complete!"

audit-templates:
	@echo "📚 Auditing template inventory..."
	python3 tools/audit_templates.py
