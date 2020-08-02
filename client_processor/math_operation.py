from functools import reduce
import uuid
import logging


class MathOperation:
    func_mapping = {'sum': lambda x, y: x + y,
                    'sub': lambda x, y: x - y,
                    'mul': lambda x, y: x * y,
                    'div': lambda x, y: x / y}

    def __init__(self, *args, **kwargs):
        self.log = logging.getLogger(self.__class__.__name__)

    def calc(self, operation):
        result = 0
        status = 'fail'
        try:
            operation['uid'] = uuid.uuid4().__str__()
            operand = self.func_mapping[operation['operator']]
            result = reduce(operand, operation['operands'])
            status = 'success'
        except ArithmeticError as ae:
            result = ae.__str__()
            self.log.error("ArithmeticError type %s when processing %s" % (ae.__str__(), operation))
        except KeyError as ke:
            result = 'Operator %s not supported' % ke.__str__()
            self.log.error("Operator %s not supported when processing %s" % (ke.__str__(), operation))
        except TypeError:
            result = 'Operands %s not supported' % operation['operands']
            self.log.error("Operands %s not supported when processing %s" % (operation['operands'], operation))
        except:
            result = 'unknow error'
            self.log.error("Unknow error when processing %s" % (operation['operands'], operation))
        finally:
            operation['result'] = result
            operation['status'] = status
            return operation
