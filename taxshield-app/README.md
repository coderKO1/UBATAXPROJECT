# TaxShield

Production-style fintech simulation for UBA SME banking with tax automation.

## Features
- JWT login
- Dashboard with balance, transactions, profit, estimated annual tax
- Transfer and receive flows with mandatory narration categories
- VAT/CIT wallet automation
- Payroll management with PAYE deductions and salary validation
- AI assistant with financial query engine
- Analytics charts and category insights

## Run with Docker
```bash
cd taxshield-app/docker
docker compose up --build
```

Frontend: http://localhost:3000  
Backend docs: http://localhost:8000/docs

Demo login:
- email: `demo@taxshield.com`
- password: `password123`
