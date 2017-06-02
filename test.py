from main import *

match1 = [('D', 'T'), ('D', 'C'), ('M', 'G'), ('U', 'C'), ('M', 'A'), ('D', 'G'), ('D', 'T'), ('U', 'C'), ('M', 'G'), ('U', 'A'), ('M', 'T'), ('U', 'A'), ('M', 'G'), ('M', 'A'), ('D', 'C'), ('U', 'T'), ('M', 'A'), ('D', 'G'), ('U', 'T'), ('M', 'A'), ('U', 'C'), ('M', 'G'), ('M', 'A'), ('M', 'T'), ('D', 'G'), ('D', 'G'), ('D', 'G'), ('U', 'A'), ('M', 'A'), ('M', 'T'), ('M', 'T'), ('U', 'A')]
match1.reverse()
match2 = [('M', 'G'), ('M', 'A'), ('M', 'C'), ('M', 'A'), ('M', 'A'), ('M', 'C'), ('M', 'G'), ('M', 'T'), ('M', 'G'), ('D', 'C'), ('M', 'G'), ('M', 'A'), ('M', 'G'), ('M', 'C'), ('M', 'A'), ('M', 'G'), ('D', 'T'), ('D', 'T'), ('D', 'T'), ('M', 'G'), ('D', 'C'), ('D', 'A'), ('D', 'T'), ('U', 'G'), ('M', 'G'), ('U', 'A'), ('M', 'C'), ('M', 'C'), ('D', 'A'), ('D', 'G'), ('M', 'G'), ('U', 'T'), ('U', 'A'), ('U', 'C'), ('M', 'G'), ('U', 'T'), ('U', 'T'), ('U', 'T'), ('M', 'G'), ('M', 'A'), ('M', 'C'), ('M', 'G'), ('M', 'A'), ('M', 'G'), ('U', 'C'), ('M', 'G'), ('M', 'T'), ('M', 'G'), ('M', 'C'), ('M', 'A'), ('M', 'A'), ('M', 'C'), ('M', 'A'), ('M', 'G')]


print('get_last_arm_index1')
idx, a = get_extended_arm(match1, True)
if idx == 3:
    print('success')
else:
    print('failure')

print('get_last_arm_index2')
idx, a = get_extended_arm(match2, False)
if idx == 15:
    print('success')
else:
    print('failure')
