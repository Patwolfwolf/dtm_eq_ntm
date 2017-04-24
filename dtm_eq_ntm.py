import itertools


def load(filename):
    f = file(filename)
    inst = []
    for line in f:
        line = line.strip()
        curr = line.split(";")
        set = []
        for a in curr:
            set.append(a.split(" "))
        inst.append(set)
    return inst


def bfs_execute(path, program):
    register = 0
    lineNum = 0
    for curr in path:
        if lineNum >= len(program):
            return False
        line = program[lineNum]
        if curr >= len(line):
            return False
        if line[curr][0] == "incr":
            register = register + int(line[curr][1])
            lineNum = lineNum + 1
            if register == 0:
                return True
        elif line[curr][0] == "jump":
            lineNum = lineNum + int(line[curr][1])
        else:
            return False
    return False


def bfs_simulate(filename):
    i = 1
    while True:
        paths = list(itertools.product([0, 1, 2, 3], repeat=i))
        program = load(filename)
        for path in paths:
            result = bfs_execute(path, program)
            if result:
                return True
        i = i + 1
    return False


def dfs_execute(program, reg, counter):
    cure = reg
    if counter < len(program):
        for curr in program[counter]:
            reg = cure
            if curr[0] == "incr":
                reg = reg + int(curr[1])
                if reg == 0:
                    return True
                elif dfs_execute(program, reg, counter + 1):
                    return True
            elif curr[0] == "jump":
                counter = counter + int(curr[1])
                if dfs_execute(program, reg, counter):
                    return True
            else:
                return False
        return False


def dfs_simulate(filename):
    program = load(filename)
    print dfs_execute(program, 0, 0)

filename = "test1.txt"
print bfs_simulate(filename)
dfs_simulate(filename)

# discussion
# program 1: The result for bfs and dfs search is both true.
# program 2: The bfs will give a true result while the dfs will reach infinity loop.
# program 3: The bfs will not give a result in a reasonable time(no solution) and the dfs will reach an infinity loop.
#
# The bfs search the program starting with limit number of instructions to execute and
# as long as it find the register equal to zero it will return true. After trying every possible combination of
# instructions of certain length, it will then increase the length of the instructions. Therefore in program 1 and 2
# bfs search found the True solution. However in program 3, there is no solution for such program, bfs will keep
# trying with longer length of instruction and since there is no such length exist, it reach an infinity loop.
#
# For the dfs search, only program 1 give the correct solution. Dfs search go through each possible route and
# will keep going until reaching the end of such route. As we can see from program 1, at the end of first route
# ([0, 0, 0, 0]) the program will reach jump - 2 at line 4 will bring the program to line 2 and forming a loop.
# In program the result of such loop is +2 and by keep adding +2 to the register with value -6 before entering
# the loop. After some repetition of the loop, the register will become 0.
# However in program 2, dfs search will still stuck in the loop. For this time, the result of loop is -1 and the
# value of register before entering the loop is -3. As keep adding -1 to -3 will never reach 0.
# In program 3, dfs search will be stuck in the same loop as in program 2.
