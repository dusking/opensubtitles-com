pre_push:
	make rebase
	make format
	make format_check
	make verbose_test

format:
	black src tests
	isort src tests

format_check:
	pylint src tests
	black src tests --check --diff --color
	isort src tests --check --diff

test:
	pytest tests

verbose_test:
	pytest tests -vvv -s

rebase:
	git checkout main
	git pull
	git checkout -
	git rebase main
