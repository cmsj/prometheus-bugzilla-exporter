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
        # NOTE: We might need to be more picky here based on self.query['type']
        # but for now everything is just a count of matching data
        if 'group_field' in self.query:
            return self.promify_grouped_count()
        if 'avg_field' in self.query:
            return self.promify_avg()
        if 'sum_field' in self.query:
            return self.promify_sum()
        if 'max_field' in self.query:
            return self.promify_max()
        return self.promify_count()

    def promify_grouped_count(self):
        """Guages of grouped data"""
        group_field = self.query['group_field']
        counts = {}
        for item in self.data:
            bit = item[group_field]
            if isinstance(bit, list):
                bit = bit[0]
            if bit not in counts:
                counts[bit] = 1
            else:
                counts[bit] += 1

        for field in counts.keys():
            self.output += f"""{self.query['name']}{{{group_field}="{field}"}} {counts[field]}
"""

        return self.output

    def promify_count(self):
        """Simple counter"""
        count = len(self.data)
        self.output += f"""{self.query['name']} {count}
"""
        return self.output

    def promify_avg(self):
        """Average a field in the results"""
        avg_field = self.query['avg_field']
        count = len(self.data)
        sum_val = 0
        for item in self.data:
            sum_val += int(item[avg_field])
        avg = sum_val / count
        self.output += f"""{self.query['name']} {avg}
"""
        return self.output

    def promify_sum(self):
        """Sum a field in the results"""
        sum_field = self.query['sum_field']
        sum_val = 0
        for item in self.data:
            sum_val += int(item[sum_field])
        self.output += f"""{self.query['name']} {sum}
"""
        return self.output

    def promify_max(self):
        """Find the maximum value of a field in the results"""
        max_field = self.query['max_field']
        max_val = 0
        for item in self.data:
            max_val = max(max_val, int(item[max_field]))
        self.output += f"""{self.query['name']} {max_val}
"""
        return self.output
