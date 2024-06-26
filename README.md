# Best City Data Pipeline
## Overview
I've been working on this fun end-to-end side project in my free time, where I'm trying to figure out the best Canadian city for me to live in. When it comes to picking a great place to call home, I take a bunch of factors into account (not in any particular order, though):

**The locals**:

* How friendly they are.
* How often they drop bad words in everyday conversation.
* The general sentiment towards their own community.

**Jobs**:

* Checking out how many data-related jobs are available
* Plus, keeping an eye on the number of Python-related job postings (I'm a big fan of Python!)

The pipeline collects comments and submitions from each city's subreddit, using polars and the RoBERTa model to clean and process the data to finally be stored in PostgreSQL. Metabase is used as the visualization tool. Docker compose is used to manage and start the required services.
## Table of Contents
- [Overview](#overview)
- [Table of Contents](#table-of-contents)
- [Architecture](#architecture)
- [Setup](#setup)
- [Improvements](#improvements)
## Architecture
![Python SQL Metabase Docker](https://raw.githubusercontent.com/rmaciasc/best_city/main/images/best-city.png)
## Requirements
- Docker (tested on v24.0.6)
- Reddit credentials
## Setup
To get the data pipeline running, first populate the `.env_example` file with your Reddit credentials:

```
...
REDDIT_CLIENT_ID=<dev_application_client_id>
REDDIT_CLIENT_SECRET=<dev_application_client_secret>
REDDIT_USER_AGENT=<dev_application_name>
REDDIT_USERNAME=<reddit username>
REDDIT_PASSWORD=<reddit password>
...
```

To get your credentials, create a Reddit account and then create a reddit developer application in the following link:
[Reddit Developer App](https://www.reddit.com/prefs/apps/).

Now just run the data pipeline along with Metabase:
```bash
# Start the postgres, python and metabase containers
$ docker compose up
```

The first run takes a couple of minutes. After the python container exits successfuly, 
visit the Metabase dashboard at http://localhost:3000/.
Use `john.doe@hotmail.com` for the username and `example1` for the password.
### Overview Dashboard
![overview dashboard](https://raw.githubusercontent.com/rmaciasc/best_city/main/images/bad_words.png)
The average sentiment range from -1 (negative) to 1 (positive). I chose to to use the average of the title of the submission as a way to analyze the sentiment of the people from these cities when they start a conversation. Here we can observe that only London and Kitchener / Waterloo present a positive value while Toronto and Calgary show the most negative values. 
Finally, Mississauga, Windsor and Hamilton remain almost neutral. 


The bar chart on the right analyzes how people continue the conversation. While Mississauga and Hamilton show a neutral sentiment when starting the conversation, people continue it in a positive way.

The bad word table also shows that swearing is most common in the big cities when people communicate over the internet.

Overall, we can conclude that London is the city where people prefer to be nicer and more polite than the other cities. For London to be my perfect city, it'll have to offer a good quantity of job postings, lets see if that's the case on the Jobs chart. 
### Jobs Dashboard
![jobs dashboard](https://raw.githubusercontent.com/rmaciasc/best_city/main/images/jobs.png)
Sadly, London is the city with the least amount of data-related job postings. Based on these results, if a person is looking to continues their career as a Data Analyst or a Data Engineer, they will have to move to the GTA or a big city. 

## Improvements

- Use multiprocessing: the main bottleneck is running the RoBERTa model for each comment. According to the PyTorch documentation, using multiprocessing can improve this process.
- Azure integration: The code is designed to either use cloud solutions or local containers so adding the option of using Azure, AWS or GCP should result in a seamless integration.
- Unit & Integration testing.