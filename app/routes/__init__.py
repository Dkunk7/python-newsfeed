# NOTES

# When a directory has __init__.py in it, it becomes a "package". Here, routes is a package, as well as app. home.py is considered a module, and it belongs to the routes package.

# You can import any variables or functions defined by Python modules (like home.py) into other modules.
# This means I can import the "bp" stuff from home.py elsewhere without having to export it first (You pretty much use "from" to tell the import where to get it from)

from .home import bp as home # The routes are attached to bp, so importing this brings those routes with it (also bp is being renamed to "home" here)

from .dashboard import bp as dashboard

from .api import bp as api