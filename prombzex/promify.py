"""Turn BZ data into Prometheus data"""


class Promify:
    """Promify class"""
    def __init__(self, query, data):
        self.query = query
        self.data = data
        self.output = f"""# HELP {self.query["name"]} {self.query["help"]}
# TYPE {self.query["name"]} {self.query["type"]}
"""

    def promify(self):
        """Dispatch the correct formatting function"""
        if 'group_field' in self.query:
            return self.promify_group_count()
        raise ValueError

    def promify_group_count(self):
        """Counter of grouped data"""
        group_field = self.query['group_field']
        counts = {}
        for item in self.data:
            if not item[group_field] in counts:
                counts[item[group_field]] = 1
            else:
                counts[item[group_field]] += 1

        for field in counts.keys():
            self.output += f"""{self.query['name']}{{{group_field}="{field}"}} {counts[field]}
"""

        return self.output
