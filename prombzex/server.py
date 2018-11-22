"""Scaffolding to expose the Bugzilla REST API nicely"""
from simple_rest_client.api import API
from simple_rest_client.resource import Resource

from . import promify


class BugzillaResource(Resource):
    """Class to define the custom REST endpoints we want"""
    actions = {
        'search': {'method': 'GET', 'url': 'rest/bug'},
    }


class BZServer:
    """Our object for interacting with a Bugzilla server"""
    def __init__(self, base_url, config):
        self.config = config
        data = self.config.server(base_url)

        self.base_url = base_url
        self.name = data["name"]
        self.api_key = data["api_key"]
        self.queries = data["queries"]

        self.bugzilla = API(
            api_root_url=self.base_url,
            params={"api_key": self.api_key},
            json_encode_body=True,
            timeout=self.config.get("timeout"),
        )
        self.bugzilla.add_resource(resource_name='bz',
                                   resource_class=BugzillaResource)

    def query_names(self):
        """Get the names of all queries defined for this server"""
        return [x["name"] for x in self.queries]

    def run_query(self, name):
        """Run a query on this server, by its name"""
        query_data = None
        for query in self.queries:
            if query["name"] == name:
                query_data = query
        if not query_data:
            raise KeyError

        params = {}
        for param in query_data["params"]:
            params[param["key"]] = param["value"]
        response = self.bugzilla.bz.search(params=params)

        if response.status_code != 200:
            raise ValueError(response.body)

        prom = promify.Promify(query_data, response.body['bugs'])
        return prom.promify()
