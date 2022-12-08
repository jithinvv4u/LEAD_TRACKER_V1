"""
File contains variables that should be changed with the project
"""

PROJECT_NAME = "leadtracker_v1"

DOMAIN_FORMAT = "v1{env}.api.<project_domain>"

PROJECT_ID = 0  # Gitlab project ID

PROJECT_GITLAB_SSH = ""  # Gitlab project ssh url


if not PROJECT_ID or not PROJECT_GITLAB_SSH:
    raise AssertionError(
        "Please set PROJECT_ID and PROJECT_GITLAB_SSH in fabfile/project_variables.py"
    )
