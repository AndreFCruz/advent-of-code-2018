import sys, re

# Operation Indices
OP_CODE_IDX, A_IDX, B_IDX, C_IDX = 0, 1, 2, 3

class OpCodes:
    @staticmethod
    def get_ops():
        return [
            OpCodes.addr, OpCodes.addi, OpCodes.mulr, OpCodes.muli, OpCodes.borr, OpCodes.bori,
            OpCodes.banr, OpCodes.bani, OpCodes.setr, OpCodes.seti, OpCodes.getir, OpCodes.getri,
            OpCodes.getrr, OpCodes.eqir, OpCodes.eqri, OpCodes.eqrr
        ]

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


def count_samples_matches(samples):
    num_sample_matches = list()
    for sample in samples:
        num_sample_matches.append(0)
        for op in OpCodes.get_ops():
            regs = sample[REGS_BEFORE_IDX].copy()
            op(regs, sample[OPERATION_IDX])
            if regs == sample[REGS_AFTER_IDX]:
                num_sample_matches[-1] += 1

    return num_sample_matches


if __name__ == '__main__':
    lines = [l.rstrip() for l in open('../input/day16.in').readlines()]
    samples = extract_samples(iter(lines))

    ## First part
    print(sum(map(lambda e: 1 if e >= 3 else 0, count_samples_matches(samples))))

    
    pass