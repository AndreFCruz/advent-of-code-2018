import sys, re
from ortools.sat.python import cp_model
from functools import reduce

# Operation Indices
OP_CODE_IDX, A_IDX, B_IDX, C_IDX = 0, 1, 2, 3

class OpCodes:

    @staticmethod
    def addr(registers, operation):
        registers[operation[C_IDX]] = registers[operation[A_IDX]] + registers[operation[B_IDX]]
    
    @staticmethod
    def addi(registers, operation):
        registers[operation[C_IDX]] = registers[operation[A_IDX]] + operation[B_IDX]

    @staticmethod
    def mulr(registers, operation):
        registers[operation[C_IDX]] = registers[operation[A_IDX]] * registers[operation[B_IDX]]

    @staticmethod
    def muli(registers, operation):
        registers[operation[C_IDX]] = registers[operation[A_IDX]] * operation[B_IDX]

    @staticmethod
    def banr(registers, operation):
        registers[operation[C_IDX]] = registers[operation[A_IDX]] & registers[operation[B_IDX]]

    @staticmethod
    def bani(registers, operation):
        registers[operation[C_IDX]] = registers[operation[A_IDX]] & operation[B_IDX]

    @staticmethod
    def borr(registers, operation):
        registers[operation[C_IDX]] = registers[operation[A_IDX]] | registers[operation[B_IDX]]

    @staticmethod
    def bori(registers, operation):
        registers[operation[C_IDX]] = registers[operation[A_IDX]] | operation[B_IDX]

    @staticmethod
    def setr(registers, operation):
        registers[operation[C_IDX]] = registers[operation[A_IDX]]

    @staticmethod
    def seti(registers, operation):
        registers[operation[C_IDX]] = operation[A_IDX]

    @staticmethod
    def getir(registers, operation):
        registers[operation[C_IDX]] = 1 if operation[A_IDX] > registers[operation[B_IDX]] else 0

    @staticmethod
    def getri(registers, operation):
        registers[operation[C_IDX]] = 1 if registers[operation[A_IDX]] > operation[B_IDX] else 0

    @staticmethod
    def getrr(registers, operation):
        registers[operation[C_IDX]] = 1 if registers[operation[A_IDX]] > registers[operation[B_IDX]] else 0

    @staticmethod
    def eqir(registers, operation):
        registers[operation[C_IDX]] = 1 if operation[A_IDX] == registers[operation[B_IDX]] else 0

    @staticmethod
    def eqri(registers, operation):
        registers[operation[C_IDX]] = 1 if registers[operation[A_IDX]] == operation[B_IDX] else 0

    @staticmethod
    def eqrr(registers, operation):
        registers[operation[C_IDX]] = 1 if registers[operation[A_IDX]] == registers[operation[B_IDX]] else 0

    @staticmethod
    def get_ops():
        return OpCodes.operations

    @staticmethod
    def get_op_index(op):
        return OpCodes.operations.index(op) if op in OpCodes.operations else -1

OpCodes.operations = [
    OpCodes.addr, OpCodes.addi, OpCodes.mulr, OpCodes.muli, OpCodes.borr, OpCodes.bori,
    OpCodes.banr, OpCodes.bani, OpCodes.setr, OpCodes.seti, OpCodes.getir, OpCodes.getri,
    OpCodes.getrr, OpCodes.eqir, OpCodes.eqri, OpCodes.eqrr
]


# Sample Indices
REGS_BEFORE_IDX, OPERATION_IDX, REGS_AFTER_IDX = 0, 1, 2

def extract_samples(lines_iter):
    samples = list()
    while True:
        line = next(lines_iter)
        m = re.match(r'(Before|After):\s+\[(\d+), (\d+), (\d+), (\d+)\]', line)
        if m is None and len(line) == 0:
            return samples
        elif m is None:
            samples[-1].append([int(el) for el in line.split(' ')])
        elif m.group(1) == 'Before':
            samples.append(list())
            samples[-1].append([int(el) for el in m.groups()[1:]])
        elif m.group(1) == 'After':
            samples[-1].append([int(el) for el in m.groups()[1:]])
            next(lines_iter)


def get_samples_matches(samples):
    samples_match_ops = list()
    for sample in samples:
        samples_match_ops.append(set())
        for op in OpCodes.get_ops():
            regs = sample[REGS_BEFORE_IDX].copy()
            op(regs, sample[OPERATION_IDX])
            if regs == sample[REGS_AFTER_IDX]:
                samples_match_ops[-1].add(op)

    return samples_match_ops


def get_code_to_idx_mapping(op_code_to_possible_indices):
    code_to_idx = dict()

    num_operations = len(op_code_to_possible_indices)
    while len(code_to_idx) < num_operations:
        for op_code in list(op_code_to_possible_indices.keys()):
            possible_indices = op_code_to_possible_indices[op_code]
            if len(possible_indices) == 1:
                code_to_idx[op_code] = possible_indices.pop()
                del op_code_to_possible_indices[op_code]

                for val in op_code_to_possible_indices.values():
                    val -= {code_to_idx[op_code]}

    return code_to_idx


def execute_program(operations, code_to_op):
    registers = [0, 0, 0, 0]
    for op in operations:
        code_to_op[op[OP_CODE_IDX]](registers, op)
    return registers


if __name__ == '__main__':
    lines = [l.rstrip() for l in sys.stdin.readlines()]
    it = iter(lines)
    samples = extract_samples(it)
    program_operations = [[int(e) for e in l.split(' ')] for l in it if l != '']

    ## First part
    sample_matches = get_samples_matches(samples)
    print(sum(map(lambda e: 1 if len(e) >= 3 else 0, sample_matches)))

    ## Get mapping OP_CODE -> operation
    code_to_ops = dict()
    for i, matches in enumerate(sample_matches):
        op_code = samples[i][OPERATION_IDX][OP_CODE_IDX]
        if op_code not in code_to_ops:
            code_to_ops[op_code] = matches
        else:
            code_to_ops[op_code] = code_to_ops[op_code] & matches

    code_to_possible_indices = {i: {OpCodes.get_op_index(op) for op in code_to_ops[i]} for i in range(len(code_to_ops))}

    code_to_idx = get_code_to_idx_mapping(code_to_possible_indices)
    code_to_op = {op_code: OpCodes.get_ops()[idx] for op_code, idx in code_to_idx.items()}

    ## Second part
    final_regs = execute_program(program_operations, code_to_op)
    print(final_regs[0])
