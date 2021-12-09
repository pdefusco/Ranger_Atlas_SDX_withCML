# This is a Cloudera Machine Learning library file
# Please do not update or edit directly

import os
import requests

__all__ = ["getConnection"]
__version__ = "0.0.1"

PROJECT_CONNECTIONS_URL = os.environ["CDSW_PROJECT_DATA_CONNECTION_URL"]
session = requests.Session()
session.auth = (os.getenv("CDSW_API_KEY"), "")
session.headers.update(
    {
        "Content-type": "application/json",
        "Accept": "application/json",
    }
)


def _get_project_dataconnections():
    res = session.get(PROJECT_CONNECTIONS_URL)
    res.raise_for_status()
    return res.json()


def _get_project_dataconnection(dataconnection_id):
    url = PROJECT_CONNECTIONS_URL + "/" + str(dataconnection_id)
    res = session.get(url)
    res.raise_for_status()
    return res.json()


def _get_data_connection_id_from_name(dataconnection_name):
    try:
        res = _get_project_dataconnections()
        dataconnections = res["projectDataConnectionList"]
    except KeyError as error:
        raise KeyError(
            "Project Data Connections returned unexpected value " + str(error)
        )
    for dc in dataconnections:
        if dc["name"] == dataconnection_name:
            return dc["id"]
    raise ValueError(f"No data connection named {dataconnection_name} found")


def _get_properties(properties):
    required_properties = ["CONNECTION_NAME"]
    bad_keys = [p for p in required_properties if properties.get(p) is None]
    if len(bad_keys) > 0:
        raise KeyError(
            "The following variables are not set "
            + " ".join(str(bad_key) for bad_key in bad_keys)
        )
    return (
        properties.get("CONNECTION_NAME"),
        properties.get("USERNAME"),
        properties.get("PASSWORD"),
    )


def _getConnectionSnippet(properties):
    dataconnection_name, username, password = _get_properties(properties)
    dataconnection_id = _get_data_connection_id_from_name(dataconnection_name)
    try:
        res = _get_project_dataconnection(dataconnection_id)
        codesnippets = res["projectDataConnectionDetails"]["codeSnippet"]
        pythonsnippet = codesnippets["rawCode"]["python"]
    except KeyError as error:
        raise KeyError(
            "Project Data Connections returned unexpected value " + str(error)
        )
    codesnippet = "\n".join(pythonsnippet)

    # Replace username and password if credentials passed in
    if username is not None:
        USER_STR_TO_REPLACE = "USERNAME = os.getenv('HADOOP_USER_NAME')"
        USERSTR = "USERNAME = '" + username + "'"
        codesnippet = codesnippet.replace(USER_STR_TO_REPLACE, USERSTR)

    if password is not None:
        PASSWORD_STR_TO_REPLACE = "PASSWORD = os.getenv('WORKLOAD_PASSWORD')"
        PWDSTR = "PASSWORD = '" + password + "'"
        codesnippet = codesnippet.replace(PASSWORD_STR_TO_REPLACE, PWDSTR)

    return codesnippet


def getConnection(properties):
    """
    Usage:
    conn = getConnection(
        {
            "CONNECTION_NAME": "somename",
            "USERNAME": "someuser",  # (optional)
            "PASSWORD": "somepassword",  # (optional)
        }
    )
    dbCursor = conn.getCursor()
    dbCursor.execute("show databases")
    for row in dbCursor:
        print(row)
    """
    fmt_codesnippet = _getConnectionSnippet(properties)
    scope = {}
    exec(fmt_codesnippet, scope)
    return scope["conn"]
