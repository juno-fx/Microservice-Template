.PHONY: k8s

# vars
VENV="venv/bin"

# env
cluster:
	@kind create cluster --name service --config .kind.yaml

down:
	@kind delete cluster --name service

dev:
	@$(MAKE) --no-print-directory cluster || echo "Cluster already exists..."

	# Install the required dependencies
	@$(MAKE) --no-print-directory dependencies

	@skaffold dev -w skaffold.yaml

# development
lint:
	@$(VENV)/ruff check src --preview

format:
	@$(VENV)/ruff format src --preview
	@$(VENV)/ruff check src --fix --preview

qc-format:
	@$(VENV)/ruff format --check src --preview

# testing
dependencies:
	@echo "Installing dependencies..."

_run_tests:
	# Create the cluster if it doesn't exist
	@$(MAKE) --no-print-directory cluster || echo "Cluster already exists..."

	# Install the required dependencies
	@$(MAKE) --no-print-directory dependencies

	# Build the required artifacts and export them to the
	# build file for use in the next steps
	@skaffold build --file-output build.json

	# Force load images into the cluster
	@skaffold deploy -a build.json --load-images=true

	# Launch the integration tests
	@skaffold verify -a build.json

local-test:
	@echo "Running Local tests... Cluster will persist after"
	@$(MAKE) --no-print-directory _run_tests || (echo "Tests failed!" \
		&& rm -rf build.json \
		&& unzip -o htmlcov.zip > /dev/null \
		&& rm -rf htmlcov.zip \
		&& exit 1) && (rm -rf build.json \
		&& unzip -o htmlcov.zip > /dev/null \
		&& rm -rf htmlcov.zip \
		&& exit 0)

test:
	@echo "Running CI tests... Cluster will be taken down after"
	@$(MAKE) --no-print-directory _run_tests || (echo "Tests failed!" \
		&& rm -rf build.json \
		&& $(MAKE) --no-print-directory down \
		&& exit 1) && (echo "Tests passed!" \
		&& rm -rf build.json \
		&& $(MAKE) --no-print-directory down \
		&& exit 0)

open-coverage:
	@xdg-open htmlcov/index.html

