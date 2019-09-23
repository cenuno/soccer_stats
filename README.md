# Soccer Statistics

This project demonstrates how to perform Extract, Transform and Load (ETL) to arrange the soccer match data for analysis. A variety of tools were used to perform ETL:

* Python (3.7.4)
    + object-orientied programming via the `Club` & `WeatherGetter` class
    + retreiving data from the [DarkSky](https://darksky.net/dev) API
* PostgreSQL (11.5)
    + Creating `.sql` files and using [`psql`](https://www.postgresql.org/docs/11/app-psql.html)
* MongoDB (4.0.3)
    + To store the requests from the API

## Requirements

### DarkSky API Credentials

To access the DarkSky API, you will need to [register with them](https://darksky.net/dev) to obtain a secret key. You must supply the secret in all API requests.

I chose to create [`~/.secrets/dark_sky_api.json`](python/weathergetter.py#L6) file to store the secret key. I recommend you create a `~/.secrets/` directory to store each of your secret keys to ensure that only you - and not the world - has access to your credentials.

### System

This project was created on a Macbook Pro running MacOS Mojave.

### Software

#### macOS/Linux Packages

To ensure your macOS/Linux machine contains all of the necessary packages, please run [`01_install.sh`](01_install.sh).

#### Python

This project used Python 3.7.4 and Anaconda 4.7.12. All Python packages can be found in the [`requirements.txt`](requirements.txt) file.

#### `soccer-env` environment
To create a new [`conda`](https://docs.conda.io/projects/conda/en/latest/user-guide/concepts/environments.html) environment to use this repo, run:

```bash
# generate the soccer-env environment from the requirements.txt file
conda create --name soccer-env --file requirements.txt
# active (go into) the soccer-env environment
conda activate soccer-env
```

Within `soccer-env`, you can run `conda install <package-name>` to install additional packages. To ensure your additions to the repository remain reproducible, generate your own [`requirements.txt`](requirements.txt) with the following code:

```bash
conda list --export > requirements.txt
```

## Acknowledgements

### Data

Thank you to [Jörg Eitner](https://www.kaggle.com/laudanum) for publishing his Football Delphi dataset on Kaggle:

> [This] dataset consist[s] of historic match data for the German Bundesliga (1st and 2nd Division) as well as the English Premier League reaching back as far as 1993 up to 2016. 

#### Migrate SQLite DB to PostgreSQL DB

To ensure you have the `raw_data/database.sqlite` file as a PostgreSQL database, please run [`02_create_db.sh`](02_create_db.sh).

### Project Idea

This material was created by the Flatiron School. All credit goes to them for generating this project idea for performing ETL using soccer data.

