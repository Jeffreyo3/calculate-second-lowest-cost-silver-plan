class ZipNode:
    def __init__(self, zipcode, state, county_code, name, rate_area):
        self.zipcode = zipcode
        self.state = state
        self.county_code = county_code
        self.name = name
        self.rate_area = rate_area

    def __str__(self):
        return f"|zipcode: {self.zipcode}, rate_area: {self.rate_area}, state: {self.state}|"

    __repr__ = __str__
