# Best City Data Pipeline
## Overview
I've been working on this fun end-to-end side project in my free time, where I'm trying to figure out the best Canadian city for me to live in. When it comes to picking a great place to call home, I take a bunch of factors into account (not in any particular order, though):

**The locals**:

* How friendly they are.
* How often they drop bad words in everyday conversation.
* The general sentiment towards their own community.

**Jobs**:

* Checking out how many data-related jobs are available
* Plus, keeping an eye on the number of Python-related gigs (I'm a big fan of Python!)

The pipeline collects comments and submitions from each city's subreddit, using polars and the RoBERTa model to clean and process the data to finally be stored in PostgreSQL. Metabase is used as the visualization tool. Docker compose is used to manage and start the required services.
## Table of Contents
## Architecture

## Setup
## Improvements

- Use multiprocessing: the main bottleneck is running the RoBERTa model for each comment. According to the PyTorch documentation, using multiprocessing can improve this process.
- 

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
