# Best City Data Pipeline

I've been working on this fun end-to-end side project in my free time, where I'm trying to figure out the best Canadian city for me to live in. When it comes to picking a great place to call home, I take a bunch of factors into account (not in any particular order, though):

**The locals**:

* How friendly they are
* How often they drop bad words in everyday conversation

**Jobs**:

* Checking out how many data-related jobs are available
* Plus, keeping an eye on the number of Python-related gigs (I'm a big fan of Python!)

## Overview
This project is developed to be run either using:
* Docker containers (either local or Azure Container Instances) and Airflow
* Azure Virtual Machine and Airflow or CRON job

## Setup

Copy and paste the following command in the terminal:
openssl rand -base64 32
Set the MB_ENCRYPTION_SECRET_KEY env variable in .env_example with the result.

MB_ENCRYPTION_SECRET_KEY="IYqrSi5QDthvFWe4/WdAxhnra5DZC3RKx3ZSrOJDKsM="

### Current state

- [x] ETL
- [x] NLP
- [x] Data Visualization
- [x] Dockerize app
- [ ] Write README.md
