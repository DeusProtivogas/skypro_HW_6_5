from pytest_factoryboy import register

from factories import UserFactory, CategoryFactory, AdFactory

pytest_plugins = "fixtures"

# Factories
register(UserFactory)
register(CategoryFactory)
register(AdFactory)
