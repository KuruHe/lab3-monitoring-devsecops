# Lab 3: Monitoring, Logging & DevSecOps

## Project
A small Flask web application demonstrating centralized logging (ELK), CI/CD security scanning (GitHub Actions + Trivy), feature flags, load testing (Locust), and browser testing (Selenium).

## Prerequisites
- Docker Desktop with Docker Compose
- Python 3.12+
- Git
- Chrome browser (for local Selenium test)

## Run the application
```bash
docker compose up --build -d
```
- App: http://localhost:5000
- Elasticsearch: http://localhost:9200
- Kibana: http://localhost:5601

Generate logs:
```bash
curl http://localhost:5000/
curl http://localhost:5000/health
curl http://localhost:5000/simulate-error
```

## ELK logging
The Logstash pipeline reads JSON logs from `./logs/*.log` and sends them to Elasticsearch. For an easy file-input demonstration, create `logs/demo.log`:
```json
{"timestamp":"2026-11-09T10:00:00Z","level":"INFO","service":"lab3-app","message":"Application started"}
{"timestamp":"2026-11-09T10:01:00Z","level":"ERROR","service":"lab3-app","message":"Demo error"}
```
Then restart Logstash:
```bash
docker compose restart logstash
```
In Kibana, open **Discover**, create a data view `lab3-logs-*`, and select `@timestamp` if prompted.

## Feature flag
Edit `FEATURE_NEW_DASHBOARD` in `docker-compose.yml`:
- `false` = classic dashboard
- `true` = new dashboard enabled

Apply:
```bash
docker compose up -d --force-recreate app
```

## Unit tests
```bash
python -m pip install -r requirements.txt
pytest -v
```

## Load testing with Locust
```bash
locust -f locustfile.py --host http://localhost:5000
```
Open http://localhost:8089. Start with 10 users and spawn rate 2 users/sec. Capture the results page.

## Selenium
Install Chrome and run:
```bash
python selenium_test.py
```
Selenium Manager may download a compatible ChromeDriver automatically. Capture the passing test output.

## DevSecOps CI
Push this repository to GitHub. The workflow in `.github/workflows/devsecops.yml` runs pytest, builds the Docker image, and scans it with Trivy. Open GitHub Actions and capture the successful workflow and scan output.

## Stop services
```bash
docker compose down
```
To remove Elasticsearch data too:
```bash
docker compose down -v
```
