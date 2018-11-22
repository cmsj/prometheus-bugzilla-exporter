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
            if self.query['type'] == 'gauge':
                return self.promify_grouped_gauge()
        else:
            if self.query['type'] == 'counter':
                return self.promify_counter()
        raise ValueError

    def promify_grouped_gauge(self):
        """Guages of grouped data"""
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

    def promify_counter(self):
        """Simple counter"""
        count = len(self.data)
        self.output += f"""{self.query['name']} {count}
"""
        return self.output
