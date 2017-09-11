# IdioTransit

Share the idiocy of drivers.

## Useful information

- [Business Rules](docs/BusinessRules.md)
- [Entity-Relation Diagram (ERD)](https://www.draw.io/#G0B4yTyCMc2tdNWGhsYnpZTWtJeW8)

## Contributing

Any contribution is very welcome. Fill a issue and lets start discussing about it.

## Development

We use and recommend [JetBrains' PyCharm](https://www.jetbrains.com/pycharm/download/).

Cloning this repo and running the following commands at the root will give you a working development environment:

- `./create_env.sh`
- `source ./env/bin/activate`
- `pip install -e .`

Don't miss the "e" option, which stands for "editable" ([more about it](https://pip.pypa.io/en/stable/reference/pip_install/#editable-installs)).

The variable "DATABASE_URL" is required to be set in the environment, referencing a PostgreSQL database.

You can do this by manually defining it (`exports` etc.) or creating a `.env` file based on `.env.example`, in the
project's root.

## Deployment

The _Continuous Integration_ triggers the _Continuous Deployment_. This means, if all tests passes and the changes are
all good, the updates are applied to the production server.
