
class County(object):
    def __init__(self, name, api, test_date):
        self.name = name
        self.base_api = api
        self.test_date = test_date
        self.result = None
        self.county_api = '{}?county={}&test_date={}'.format(self.base_api, self.name, self.test_date)
        self.result = []

    def prepare_data(self):
        rows = []
        for data in self.result:
            rows.append(
                (
                    data['test_date'],
                    data['county'],
                    data['new_positives'],
                    data['cumulative_number_of_positives'],
                    data['total_number_of_tests'],
                    data['cumulative_number_of_tests']
                )
            )
        return rows

