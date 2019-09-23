echo "Start installing necessary packages"

# Check for xcode-select; install if we don't have it
# for more information, see: https://help.apple.com/xcode/mac/current/#/devc8c2a6be1
if test ! $(which xcode-select); then 
    echo "Installing xcode-select..."
    xcode-select --install
fi

# Check for Homebrew; install if we don't have it
# for more information, see: https://brew.sh/
if test ! $(which brew); then
    echo "Installing homebrew..."
    ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
fi


# Check for anaconda; install if we don't have it
if test ! $(which anaconda); then
    echo "Installing anaconda..."
    brew cask install anaconda
fi

# Check for MongoDB; install if we don't have it
if test ! $(which mongo); then
    echo "Installing MongoDB..."
    brew install mongodb
fi

# Check for PostgreSQL; install if we don't have it
if test ! $(which postgres); then
    echo "Installing PostgreSQL..."
    brew install postgresql
fi

# start PostgreSQL services
echo "Ensuring PostgreSQL services are running..."
brew services start postgresql

# Check for pgloader; install if we don't have it
if test ! $(which pgloader); then
    echo "Install pgloader to transform SQLite database to a PostgreSQL database..."
    brew install --HEAD pgloader
fi

echo "Finished installing necessary packages"
