class Prefix:
    def __init__(self, expression):
        self.expression = expression.strip()  # Удаляем лишние пробелы

    def to_infix_notation(self):
        stack = []
        operators = set(['+', '-', '*', '/'])

        # Если выражение пустое, возвращаем пустую строку
        if not self.expression:
            return ""

        # Разбиваем выражение на элементы
        tokens = self.expression.split()

        # Обрабатываем элементы в обратном порядке
        for token in reversed(tokens):
            if token in operators:
                # Проверяем, что в стеке достаточно операндов
                if len(stack) < 2:
                    operand1 = stack.pop()
                    new_expr = f'({operand1})'
                    stack.append(new_expr)
                    break
                    # raise IndexError(f"Недостаточно операндов в выражении {stack}.")

                # Операция: извлекаем два операнда из стека
                operand1 = stack.pop()
                operand2 = stack.pop()
                # Формируем инфиксное выражение
                new_expr = f'({operand1} {token} {operand2})'
                stack.append(new_expr)
            else:
                # Операнд: добавляем в стек
                stack.append(token)

        # В стеке должен остаться один элемент - итоговое инфиксное выражение
        if len(stack) == 1:
            return stack[0]
        else:
            raise IndexError("Некорректное выражение.")
