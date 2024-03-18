build:
	@docker build -t watch-webhook:latest .
	@docker push watch-webhook:latest

run_local: ## Shell Terraform console
	@docker build -t watch-filter:latest .
	@docker run -p 5001:5000 watch-filter:latest
