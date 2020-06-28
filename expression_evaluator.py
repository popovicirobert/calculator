
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
        answer = [0, 1]
        while self.current_character().isdigit():
            answer[0] = answer[0] * 10 + int(self.current_character()) - int('0')
            self.advance()

        if self.position < len(self.text) and self.current_character() == '.':
            self.advance()

            while self.current_character().isdigit():
                answer[0] = answer[0] * 10 + int(self.current_character()) - int('0')
                answer[1] *= 10
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
            answer = self.evaluate_factor(level)
            return [-1 * answer[0], answer[1]]

        elif self.current_character().isdigit():
            return self.get_number()

        else:
            self.error()
            return [1, 1]

    def evaluate_term(self, level):
        answer = self.evaluate_factor(level)
        while self.current_character() in ('x', '/'):
            if self.current_character() == 'x':
                self.advance()
                current_factor = self.evaluate_factor(level)
                answer[0] *= current_factor[0]
                answer[1] *= current_factor[1]
            else:
                self.advance()
                current_factor = self.evaluate_factor(level)

                try:
                    assert current_factor[0] != 0
                    answer[0] *= current_factor[1]
                    answer[1] *= current_factor[0]
                except AssertionError:
                    self.error()

        return answer

    def evaluate_expression(self, level = 0):
        answer = self.evaluate_term(level)
        while self.current_character() in ('+', '-'):
            if self.current_character() == '+':
                self.advance()
                current_term = self.evaluate_term(level)
                answer[0] = answer[0] * current_term[1] + answer[1] * current_term[0]
                answer[1] *= current_term[1]
            else:
                self.advance()
                current_term = self.evaluate_term(level)
                answer[0] = answer[0] * current_term[1] - current_term[0] * answer[1]
                answer[1] *= current_term[1]

        if level == 0 and self.error_flag == True:
            answer = ['Error', 'Error']
        if level == 0 and self.position < len(self.text):
            answer = ['Error', 'Error']

        return answer
