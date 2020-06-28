
class ExpressionEvaluator:

    def __init__(self, text):
        self.text = text
        self.position = int(0)
        self.error_flag = False

    # Expr = Term (+, -) Term
    # Term = Fact (*, /) Fact
    # Fact = ( Expr ) / number

    def error(self):
        self.error_flag = True

    def current_character(self):
        if len(self.text) <= self.position:
            return '!'
        return self.text[self.position]

    def advance(self):
        self.position += 1

    def get_number(self):
        answer = 0
        while self.current_character().isdigit():
            answer = answer * 10 + int(self.current_character()) - int('0')
            self.advance()


        if self.position < len(self.text) and self.current_character() == '.':
            self.advance()

            power = 1e-1
            while self.current_character().isdigit():
                answer += power * int(self.current_character()) - int('0')
                power *= 1e-1
                self.advance()

        return answer

    def evaluate_factor(self, level):
        if self.current_character() == '(':
            self.advance()
            answer = self.evaluate_expression(level + 1)

            try:
                assert self.current_character() == ')'
            except:
                self.error()

            self.advance()
            return answer

        elif self.current_character() == '-':
            self.advance()
            return -self.evaluate_factor(level)

        elif self.current_character().isdigit():
            return self.get_number()

        else:
            self.error()
            return 1

    def evaluate_term(self, level):
        answer = self.evaluate_factor(level)
        while self.current_character() in ('x', '/'):
            if self.current_character() == 'x':
                self.advance()
                answer *= self.evaluate_factor(level)
            else:
                self.advance()

                try:
                    answer /= self.evaluate_factor(level)
                except ZeroDivisionError:
                    self.error()

        return answer

    def evaluate_expression(self, level = 0):
        answer = self.evaluate_term(level)
        while self.current_character() in ('+', '-'):
            if self.current_character() == '+':
                self.advance()
                answer += self.evaluate_term(level)
            else:
                self.advance()
                answer -= self.evaluate_term(level)

        if level == 0 and self.error_flag == True:
            answer = 'Error'
        if level == 0 and self.position < len(self.text):
            answer = 'Error'

        return answer
