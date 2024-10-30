# code-challenge-indicium
## Setup
First, if you haven't already, install Docker.

Then, run the following command to start the database containers:
```bash
docker compose up -d
```
In this project, we're using Docker to run 2 postgres databases:
- `db-source`: the source database, which contains the Northwind dataset.
- `db-analytics`: the analytics database, which we will be storing the results of our transformations in.

## Transformations  

