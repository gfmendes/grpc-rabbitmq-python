from functools import reduce
import uuid


class MathOperation:
    func_mapping = {'sum': lambda x, y: x + y,
                    'sub': lambda x, y: x - y,
                    'mul': lambda x, y: x * y,
                    'div': lambda x, y: x / y}

    def calc(self, func):
        result = 0
        status = 'fail'
        try:
            operand = self.func_mapping[func['operator']]
            result = reduce(operand, func['operands'])
            status = 'success'
        except ArithmeticError as ae:
            result = ae.__str__()
        except KeyError as ke:
            result = 'Operator %s not supported:' % ke.__str__()
            print("Operator %s not supported!" % func['operator'])
        except TypeError:
            result = 'Operands %s not supported:' % func['operands']
            print("Operands %s not supported!" % func['operands'])
        except:
            result = 'generic error'
            print("Generic error.")
        finally:
            func['result'] = result
            func['status'] = status
            func['uid'] = uuid.uuid4().__str__()
            return func
