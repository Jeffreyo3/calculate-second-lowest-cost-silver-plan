class PlanNode:
    def __init__(self, plan_id, state, metal_level, rate, rate_area):
        self.plan_id = plan_id
        self.state = state
        self.metal_level = metal_level
        self.rate = rate
        self.rate_area = rate_area

    def __str__(self):
        return f"[rate: {self.rate}, rate_area: {self.rate_area}, state: {self.state}]"

    __repr__ = __str__
