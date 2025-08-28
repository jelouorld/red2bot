# Red2Bot

Red2Bot is a **serverless, domain-partitioned AI project** built with Python and Terraform. It is designed to be modular, scalable, and easy to maintain, leveraging AWS serverless components and a clean separation of concerns.

---

## **Architecture Overview**

The project follows a **serverless architecture**:

- **AWS Lambda** functions handle the execution of code for bots, data converters, and fetchers.
- **API Gateway** exposes endpoints to interact with the bots and other services.
- **Embeddings & AI services** are used for advanced processing and chatbot functionalities.
- **Terraform** manages all infrastructure as code for reproducibility and scalability.
- Each module maintains its **own Terraform state**, enabling isolated deployments.

![Architecture Diagram]<img width="901" height="822" alt="image" src="https://github.com/user-attachments/assets/7af2bba0-010b-468f-8066-3167d0ca386f" />

---

## **Domain-Partitioned Design**

The project is structured by **domains**, each encapsulating its own logic, infrastructure, and tests:

### 1. Bot Domain (`domain/bot`)
Handles the core chatbot logic and API exposure.

- **Python code**: `src/main.py`
- **Infrastructure**: `infra/` contains Lambda, API Gateway, permissions, embeddings, and deployment configs.
- **Tests**: `test/` contains unit, smoke, and e2e tests.
- **Deployment**: `deploy.sh` deploys the bot domain independently.

### 2. Data Ingestion (`domain/dataingestion`)
Responsible for fetching and converting data from external sources.

- **Converter (`converter/`)**  
  - Transforms raw data into structured formats.  
  - Own Lambda function (`src/main.py`) and Terraform infra.  
  - Tested with unit, integration, and e2e tests.

- **Fetchers (`fetchers/`)**  
  - Connects to external APIs or databases to fetch data for ingestion.  
  - Each client (e.g., `luchy`, `medar`) has a dedicated folder with:
    - Lambda function (`src/main.py`)  
    - Terraform infra (`infra/main/fetcher.tf`, `scheduler.tf`)  
    - Tests (`test/`)

- **Deployment**: Each fetcher has a `deploy.sh` for isolated deployment.

---


## Key Features

- Serverless: AWS Lambda functions and API Gateway.

- Domain-partitioned: Independent modules for bot, converter, and fetchers.

- Infrastructure as Code: Terraform-managed infra for reproducibility.

- AI-powered: Embeddings and chatbot logic integrated in the bot domain.

- Modular Testing: Unit, integration, and e2e tests per module.

- Independent Deployments: Each domain can be deployed and updated independently.

---

