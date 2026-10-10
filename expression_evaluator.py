"""Stack-based mathematical expression evaluator (DCOMP320 - Stacks Implementation)."""


class Stack:
    def __init__(self):
        self._items = []

    def push(self, item):
        self._items.append(item)

    def pop(self):
        if self.is_empty():
            raise IndexError("pop from empty stack")
        return self._items.pop()

    def peek(self):
        if self.is_empty():
            raise IndexError("peek from empty stack")
        return self._items[-1]

    def is_empty(self):
        return len(self._items) == 0

    def size(self):
        return len(self._items)


def precedence(op):
    if op in ("*", "/"):
        return 2
    if op in ("+", "-"):
        return 1
    return 0


def apply_operator(operators, values):
    op = operators.pop()
    if values.size() < 2:
        raise ValueError("Invalid expression")
    b = values.pop()
    a = values.pop()
    if op == "+":
        values.push(a + b)
    elif op == "-":
        values.push(a - b)
    elif op == "*":
        values.push(a * b)
    elif op == "/":
        if b == 0:
            raise ZeroDivisionError("Division by zero")
        values.push(a / b)


def evaluate_expression(expr):
    values, operators = Stack(), Stack()
    i, prev = 0, None  # prev: last token type, used to detect unary minus
    while i < len(expr):
        ch = expr[i]
        if ch.isspace():
            i += 1
            continue
        if ch.isdigit() or ch == ".":
            j = i
            while j < len(expr) and (expr[j].isdigit() or expr[j] == "."):
                j += 1
            values.push(float(expr[i:j]))
            i, prev = j, "num"
            continue
        if ch == "(":
            operators.push(ch)
            i, prev = i + 1, "("
            continue
        if ch == ")":
            while not operators.is_empty() and operators.peek() != "(":
                apply_operator(operators, values)
            if operators.is_empty():
                raise ValueError("Mismatched parentheses")
            operators.pop()
            i, prev = i + 1, ")"
            continue
        if ch in "+-*/":
            if ch in "+-" and prev in (None, "(", "op"):  # unary sign
                values.push(0.0)
            while (not operators.is_empty() and operators.peek() != "("
                   and precedence(operators.peek()) >= precedence(ch)):
                apply_operator(operators, values)
            operators.push(ch)
            i, prev = i + 1, "op"
            continue
        raise ValueError("Unknown character")
    while not operators.is_empty():
        if operators.peek() == "(":
            raise ValueError("Mismatched parentheses")
        apply_operator(operators, values)
    if values.size() != 1:
        raise ValueError("Invalid expression")
    return values.pop()


def is_separator(line):
    s = line.strip()
    return len(s) > 0 and set(s) == {"-"} and len(s) >= 3


def format_result(x):
    return str(int(x)) if x == int(x) else str(round(x, 6))


def process_files(in_path="input.txt", out_path="output.txt"):
    with open(in_path) as fin, open(out_path, "w") as fout:
        for line in fin:
            line = line.rstrip("\n")
            if is_separator(line):
                fout.write(line + "\n")
            elif line.strip() == "":
                fout.write("\n")
            else:
                try:
                    fout.write(format_result(evaluate_expression(line)) + "\n")
                except ZeroDivisionError:
                    fout.write("ERROR: Division by zero\n")
                except ValueError as e:
                    fout.write(f"ERROR: {e}\n")
                except IndexError:
                    fout.write("ERROR: Invalid expression\n")


if __name__ == "__main__":
    process_files()
    print("Done. Results written to output.txt")