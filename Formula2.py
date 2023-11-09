import re


class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __repr__(self) -> str:
        return f"Token({self.type}, {self.value})"

    def __str__(self) -> str:
        return self.__repr__()


class TokenType:
    VARIABLE = "VARIABLE"
    CONJUNCTION = "CONJUNCTION"
    DISJUNCTION = "DISJUNCTION"
    IMPLICATION = "IMPLICATION"
    COIMPLICATION = "COIMPLICATION"
    NEGATION = "NEGATION"
    BOX_MODALITY = "BOX_MODALITY"
    DIAMOND_MODALITY = "DIAMOND_MODALITY"
    PAREN = "PAREN"
    CLOSING_PAREN = "CLOSING_PAREN"
    WHITESPACE = "WHITESPACE"
    EOF = "EOF"


class Lexer:
    def __init__(self, input_string):
        self.input_string = input_string
        self.current_token = None
        self.lookahead_token = None

    def next_token(self) -> Token:
        if self.lookahead_token is not None:
            token = self.lookahead_token
            self.lookahead_token = None
            return token

        while True:
            if self.is_end_of_file():
                return Token(TokenType.EOF, None)

            self.consume()

            token_type = self.get_token_type()

            if token_type is not TokenType.WHITESPACE:
                return Token(token_type, self.current_char)

    def peek_token(self):
        if self.lookahead_token is None:
            self.lookahead_token = self.next_token()

        return self.lookahead_token

    def consume(self):
        self.current_char = self.input_string[0]
        self.input_string = self.input_string[1:]

    def is_end_of_file(self):
        return len(self.input_string) == 0

    def get_token_type(self):
        if self.current_char.isalpha():
            return TokenType.VARIABLE

        elif self.current_char == "&":
            return TokenType.CONJUNCTION

        elif self.current_char == "|":
            return TokenType.DISJUNCTION

        elif self.current_char == "-":
            self.consume()
            if self.current_char == ">":
                self.current_char = "->"
                return TokenType.IMPLICATION
            elif self.current_char == "<":
                self.current_char = "-<"
                return TokenType.COIMPLICATION
            else:
                raise ValueError(f"Invalid character: {self.current_char}")

        elif self.current_char == "~":
            return TokenType.NEGATION

        elif self.current_char == "[":
            self.consume()
            if self.current_char == "]":
                self.current_char = "[]"
                return TokenType.BOX_MODALITY
            else:
                raise ValueError(f"Invalid character: {self.current_char}")

        elif self.current_char == "<":
            self.consume()
            if self.current_char == ">":
                self.current_char = "<>"
                return TokenType.DIAMOND_MODALITY
            else:
                raise ValueError(f"Invalid character: {self.current_char}")

        elif self.current_char == "(":
            return TokenType.PAREN

        elif self.current_char == ")":
            return TokenType.CLOSING_PAREN

        elif self.current_char.isspace():
            return TokenType.WHITESPACE

        else:
            raise ValueError(f"Invalid character: {self.current_char}")

    def list_tokens(self):
        print("Listing")
        tokens = []

        while True:
            token = self.next_token()
            if token.type is TokenType.EOF:
                tokens.append(token.__repr__())
                break

            tokens.append(token.__repr__())

        return tokens


class Expression:
    def evaluate(self, frame):
        pass


class Variable(Expression):
    def __init__(self, name):
        self.name = name

    def __repr__(self) -> str:
        return f"Variable({self.name})"

    def evaluate(self, frame):
        # Access the variable value from the frame
        pass


class Negation(Expression):
    def __init__(self, operand):
        self.operand = operand

    def __repr__(self) -> str:
        return f"Negation({self.operand.__repr__()})"

    def evaluate(self, frame):
        # Implement negation evaluation
        pass


class Conjunction(Expression):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self) -> str:
        return f"Conjunction({self.left.__repr__()}, {self.right.__repr__()})"

    def evaluate(self, frame):
        # Implement conjunction evaluation
        pass


class Disjunction(Expression):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self) -> str:
        return f"Disjunction({self.left.__repr__()}, {self.right.__repr__()})"

    def evaluate(self, frame):
        # Implement disjunction evaluation
        pass


class Implication(Expression):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self) -> str:
        return f"Implication({self.left.__repr__()}, {self.right.__repr__()})"

    def evaluate(self, frame):
        # Implement implication evaluation
        pass


class Coimplication(Expression):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self) -> str:
        return f"Coimplication({self.left.__repr__()}, {self.right.__repr__()})"

    def evaluate(self, frame):
        # Implement biconditional evaluation
        pass


class BoxModality(Expression):
    def __init__(self, operand):
        self.operand = operand

    def __repr__(self) -> str:
        return f"BoxModality({self.operand.__repr__()})"

    def evaluate(self, frame):
        # Implement box modality evaluation
        pass


class DiamondModality(Expression):
    def __init__(self, operand):
        self.operand = operand

    def __repr__(self) -> str:
        return f"DiamondModality({self.operand.__repr__()})"

    def evaluate(self, frame):
        # Implement diamond modality evaluation
        pass


class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.next_token()

    def parse(self):
        return self.expr()

    def expr(self):
        # WIP
        token = self.current_token

        # Handle unary operations
        if token.type in (
            TokenType.NEGATION,
            TokenType.BOX_MODALITY,
            TokenType.DIAMOND_MODALITY,
        ):
            operator = token.type
            self.current_token = self.lexer.next_token()

            if operator == TokenType.NEGATION:
                return Negation(self.expr())
            elif operator == TokenType.BOX_MODALITY:
                return BoxModality(self.expr())
            elif operator == TokenType.DIAMOND_MODALITY:
                return DiamondModality(self.expr())

        # Handle variables
        if token.type == TokenType.VARIABLE:
            variable = Variable(token.value)
            # self.current_token = self.lexer.next_token()

            # Check if the next token is a binary operator or the end of input
            if self.lexer.peek_token().type not in (
                TokenType.CONJUNCTION,
                TokenType.DISJUNCTION,
                TokenType.IMPLICATION,
                TokenType.COIMPLICATION,
            ):
                return variable

            operator = self.lexer.next_token().type
            right_operand = self.expr()

            if operator == TokenType.CONJUNCTION:
                return Conjunction(variable, right_operand)
            elif operator == TokenType.DISJUNCTION:
                return Disjunction(variable, right_operand)
            elif operator == TokenType.IMPLICATION:
                return Implication(variable, right_operand)
            elif operator == TokenType.COIMPLICATION:
                return Coimplication(variable, right_operand)

        # Handle parenthesized expressions
        if token.type == TokenType.PAREN:
            self.current_token = self.lexer.next_token()
            sub_expr = self.expr()
            self.current_token = self.lexer.next_token()  # Consume closing parenthesis
            return sub_expr

        raise ValueError(f"Invalid token: {token}")


# def evaluate_formula(formula, frame):
#     # Tokenize the formula
#     lexer = Lexer(formula)

#     # Parse the formula
#     parser = Parser(lexer)
#     ast = parser.parse()

#     # Evaluate the formula
#     result = ast.evaluate(frame)

#     return result


lexer = Lexer("[] a -< b")
# print(lexer.list_tokens())

parser = Parser(lexer)
exp = parser.expr()
print(exp)
