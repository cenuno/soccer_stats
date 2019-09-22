# Raw Data

This directory will store raw data related to this project.

## Note

I used `pgloader` to convert the SQLite database to a PostgreSQL database. To install `pgloader`, please run the following commands in the Terminal:

```bash
# install psql
brew install postgresql

# ensure the PostgreSQL is running
brew services start postgresql

# install pgloader
brew install --HEAD pgloader

# create soccer database
createdb soccer

# transform SQLite db to psql
# note: be mindful of database.sqlite's relative path
pgloader database.sqlite postgresql:///soccer
```
