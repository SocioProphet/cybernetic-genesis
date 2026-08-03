# cybernetic-genesis — reviewable make targets that wrap the CI teeth.
# `make check` is the plumb-line: every gate the CI runs, runnable locally, fail-closed.
.PHONY: check schema mount-strategy test deploy-check

check: schema mount-strategy test deploy-check ## run every fail-closed gate

schema: ## schema selftest — valids validate, invalids rejected
	python tools/validate.py selftest

mount-strategy: ## InceptionMountStrategy contract — mapping + symlink + task-persistence teeth
	python tools/verify_mount_strategy.py selftest
	python -m pytest -q tests/test_mount_strategy.py

test: ## runtime + emission tests
	python -m pytest -q tools/test_emit_tritrpc.py
	PYTHONPATH=src python -m pytest -q tests/test_inception.py

deploy-check: ## deploy overlay self-containment (INV-DEP-10) + mounts declared through the strategy
	python tools/verify_deploy_self_contained.py
	python tools/verify_deploy_mount_strategy.py
	python -m pytest -q tests/test_deploy_mount_strategy.py
