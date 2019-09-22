echo "Start creating soccer database"

# create soccer PostgreSQL database
createdb soccer

# migrate the .sqlite file to the soccer PostgreSQL database
pgloader raw_data/database.sqlite postgresql:///soccer

echo "Finished creating soccer database"
