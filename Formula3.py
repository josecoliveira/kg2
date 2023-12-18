from abc import abstractmethod


class Model:
    def __check_relation_value(relation_value):
        if not isinstance(relation_value, int):
            raise Exception("Relation error: Relation values must be integers.")
        if relation_value < 0 or relation_value > 1:
            raise Exception(
                "Relation error: Relation values must be greater or equal than 0 and less or equal than 1."
            )

    @staticmethod
    def __check_relation(relation, world_size):
        if not isinstance(relation, list):
            raise Exception("Relation error: Relation is not a list.")
        if len(relation) != world_size:
            raise Exception(
                f"Relation error: Relation must be a list of size {world_size}."
            )
        for world_relation in relation:
            if not isinstance(world_relation, list):
                raise Exception("Relation error: Relation must be a list of lists.")
            if len(world_relation) != world_size:
                raise Exception(
                    f"Relation error: Relation size for a world must be of size {world_size}."
                )
            for relation_value in world_relation:
                Model.__check_relation_value(relation_value)

    @staticmethod
    def __check_world_variable_valuation(world_value, type):
        if not isinstance(world_value, int):
            raise Exception(
                f"Valuation error: Valuation{type} value for a world must be a integer."
            )
        if world_value < 0 or world_value > 1:
            raise Exception(
                f"Valuation error: Valuation {type} must be greater or equal than 0 and less or equal than 1."
            )

    @staticmethod
    def __check_variable_valuation(value, type):
        if not isinstance(value, list):
            raise Exception(f"Valuation error: Valuation {type} value must be a list.")
        for world_value in value:
            Model.__check_world_variable_valuation(world_value, type)

    @staticmethod
    def __check_valuation(valuation, type):
        if not isinstance(valuation, dict):
            raise Exception(f"Valuation error: Valuation {type} must be a dictionary.")
        for value in valuation.values():
            Model.__check_variable_valuation(value, type)

    def __init__(
        self,
        worlds_size: int,
        relation=None,
        valuation1=None,
        valuation2=None,
        self_relation=False,
    ) -> None:
        self.worlds_size = worlds_size

        if relation == None:
            self.relation = [
                [1 if i == j and self_relation else 0 for j in range(worlds_size)]
                for i in range(worlds_size)
            ]
        else:
            Model.__check_relation(relation, worlds_size)
            self.relation = relation

        if valuation1 == None:
            self.valuation1 = {}
        else:
            Model.__check_valuation(valuation1, 1)
            self.valuation1 = valuation1

        if valuation2 == None:
            self.valuation2 = {}
        else:
            Model.__check_valuation(valuation1, 1)
            self.valuation2 = valuation2

    def set_relation(self, world1, world2, value):
        Model.__check_relation_value(value)
        self.relation[world1][world2] = value

    def set_variable_valuation1(self, variable, value):
        Model.__check_variable_valuation(value)
        self.valuation1[variable] = value

    def set_variable_valuation1(self, variable, value):
        Model.__check_variable_valuation(value)
        self.valuation2[variable] = value

    @staticmethod
    def __check_world(self, world):
        if not isinstance(world, int):
            raise Exception("World error: World must be an integer.")

    def set_variable_valuation1_for_world(self, variable, world, value):
        Model.__check_world(world)
        Model.__check_world_variable_valuation(value, 1)
        self.valuation1[variable][world] = value

    def set_variable_valuation1_for_world(self, variable, world, value):
        Model.__check_world(world)
        Model.__check_world_variable_valuation(value, 2)
        self.valuation1[variable][world] = value


class Expression:
    @abstractmethod
    def valuation1(self, model: Model, world: int):
        pass

    @abstractmethod
    def valuation2(self, model: Model, world: int):
        pass


class Variable(Expression):
    def __init__(self, variable):
        self.variable = variable

    def __repr__(self) -> str:
        return f"Variable({self.variable})"

    def valuation1(self, model: Model, world: int):
        return model.valuation1[self.variable][world]

    def valuation2(self, model: Model, world: int):
        return model.valuation2[self.variable][world]


class Negation(Expression):
    def __init__(self, operand: Expression):
        self.operand = operand

    def __repr__(self) -> str:
        return f"Negation({self.operand.__repr__()})"

    def valuation1(self, model: Model, world: int):
        return self.operand.valuation2(model, world)

    def valuation2(self, model: Model, world: int):
        return self.operand.valuation1(model, world)


class Conjunction(Expression):
    def __init__(self, left: Expression, right: Expression):
        self.left = left
        self.right = right

    def __repr__(self) -> str:
        return f"Conjunction({self.left.__repr__()}, {self.right.__repr__()})"

    def valuation1(self, model: Model, world: int):
        a = self.left.valuation1(model, world)
        b = self.right.valuation1(model, world)
        return max(a, b)

    def valuation2(self, model: Model, world: int):
        a = self.left.valuation2(model, world)
        b = self.right.valuation2(model, world)
        return min(a, b)


class Disjunction(Expression):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self) -> str:
        return f"Disjunction({self.left.__repr__()}, {self.right.__repr__()})"

    def valuation1(self, model: Model, world: int):
        a = self.left.valuation1(model, world)
        b = self.right.valuation1(model, world)
        return min(a, b)

    def valuation2(self, model: Model, world: int):
        a = self.left.valuation2(model, world)
        b = self.right.valuation2(model, world)
        return max(a, b)


class Implication(Expression):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self) -> str:
        return f"Implication({self.left.__repr__()}, {self.right.__repr__()})"

    def valuation1(self, model: Model, world: int):
        a = self.left.valuation1(model, world)
        b = self.right.valuation1(model, world)
        return 1 if a <= b else b

    def valuation2(self, model: Model, world: int):
        a = self.left.valuation2(model, world)
        b = self.right.valuation2(model, world)
        return 0 if b <= a else b


class Coimplication(Expression):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self) -> str:
        return f"Coimplication({self.left.__repr__()}, {self.right.__repr__()})"

    def valuation1(self, model: Model, world: int):
        b = self.left.valuation1(model, world)
        a = self.right.valuation1(model, world)
        return 0 if b <= a else b

    def valuation2(self, model: Model, world: int):
        b = self.left.valuation2(model, world)
        a = self.right.valuation2(model, world)
        return 1 if a <= b else b


class BoxModality(Expression):
    def __init__(self, operand):
        self.operand = operand

    def __repr__(self) -> str:
        return f"BoxModality({self.operand.__repr__()})"

    def valuation1(self, model: Model, world: int):
        pass


class DiamondModality(Expression):
    def __init__(self, operand):
        self.operand = operand

    def __repr__(self) -> str:
        return f"DiamondModality({self.operand.__repr__()})"

    def evaluate(self, frame):
        # Implement diamond modality evaluation
        pass


def main():
    model = Model(10, self_relation=True)
    print(model.relation)


if __name__ == "__main__":
    main()
