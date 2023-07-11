class Formula:
    def __init__(self, formula: str) -> None:
        self.formula = formula

    def __str__(self) -> str:
        return f"<{self.formula}>"

    def __and__(self, other: 'Formula') -> 'Formula':
        if isinstance(other, Formula):
            return Formula(f"({self.formula} /\ {other.formula})")
        else:
            raise TypeError("Unsupported operand type for &")

    def __or__(self, other: 'Formula') -> 'Formula':
        if isinstance(other, Formula):
            return Formula(f"({self.formula} \/ {other.formula})")
        else:
            raise TypeError("Unsupported operand type for |")

    def __rshift__(self, other: 'Formula') -> 'Formula':
        if isinstance(other, Formula):
            return Formula(f"({self.formula} -> {other.formula})")
        else:
            raise TypeError("Unsupported operand type for ->")

    def __gt__(self, other: 'Formula') -> 'Formula':
        if isinstance(other, Formula):
            return Formula(f"({self.formula} >- {other.formula})")
        else:
            raise TypeError("Unsupported operand type for >-")

    def __invert__(self) -> 'Formula':
        return Formula(f"~{self.formula}")

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Formula):
            return self.formula == other.formula
        else:
            return False

    def evaluate(self, fuzzy_frame: dict, agent: str) -> float:
        return self._evaluate_formula(self.formula, fuzzy_frame, agent)

    def _evaluate_formula(self, formula: str, fuzzy_frame: dict, agent: str) -> float:
        if formula[0] == "~":
            return not self._evaluate_formula(formula[1:], fuzzy_frame, agent)
        elif formula[0] == "(" and formula[-1] == ")":
            return self._evaluate_complex_formula(formula[1:-1], fuzzy_frame, agent)
        elif formula[0] == "[" and formula[1] == "]":
            return self._evaluate_box_formula(formula[2:], fuzzy_frame, agent)
        elif formula[0] == "<" and formula[1] == ">":
            return self._evaluate_diamond_formula(formula[2:], fuzzy_frame, agent)
        else:
            return fuzzy_frame.get(formula, {}).get(agent, 0.0)

    def _evaluate_complex_formula(self, formula: str, fuzzy_frame: dict, agent: str) -> float:
        parts = formula.split()
        operator = parts[1]
        left_operand = self._evaluate_formula(parts[0], fuzzy_frame, agent)
        right_operand = self._evaluate_formula(parts[2], fuzzy_frame, agent)

        if operator == "&":
            return min(left_operand, right_operand)
        elif operator == "|":
            return max(left_operand, right_operand)
        elif operator == "->":
            if left_operand <= right_operand:
                return right_operand
            else:
                return 1.0
        elif operator == ">-":
            if left_operand <= right_operand:
                return 0.0
            else:
                return left_operand
        else:
            raise ValueError("Invalid operator")

    def _evaluate_diamond_formula(self, formula: str, fuzzy_frame: dict, agent: str) -> float:
        sub_formula = formula.strip()
        trust_values = fuzzy_frame.get("relation", {}).get(agent, {})
        return max(
            min(
                trust_values[other_agent],
                self._evaluate_formula(sub_formula, fuzzy_frame, other_agent),
            )
            for other_agent in trust_values
        )

    def _evaluate_box_formula(self, formula: str, fuzzy_frame: dict, agent: str) -> float:
        sub_formula = formula.strip()
        trust_values = fuzzy_frame.get("relation", {}).get(agent, {})
        return min(
            1.0
            if trust_values[other_agent]
            <= self._evaluate_formula(sub_formula, fuzzy_frame, other_agent)
            else self._evaluate_formula(sub_formula, fuzzy_frame, other_agent)
            for other_agent in trust_values
        )


# Example usage

formula = Formula("<> A")
fuzzy_frame = {
    "A": {"agent1": 1.0, "agent2": 0.1, "agent3": 0.9},
    "relation": {
        "agent1": {"agent1": 1.0, "agent2": 0.7, "agent3": 0.4},
        "agent2": {"agent1": 0.7, "agent2": 1.0, "agent3": 0.6},
        "agent3": {"agent1": 0.4, "agent2": 0.6, "agent3": 1.0},
    },
}
agent = "agent1"
result = formula.evaluate(fuzzy_frame, agent)
print(result)

