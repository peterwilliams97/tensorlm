import random


test_frac = 0.3
min_group_size = 500
random_split = True
random_seed = 117

para_list = []
line_list = []
between = True
n_lines = 0
n_chars = 0

path = 'original.txt'
if random_split:
    train_path = 'train.rnd.txt'
    test_path = 'test.rnd.txt'
else:
    train_path = 'train.txt'
    test_path = 'train.txt'


random.seed(random_seed)

with open(path, 'rt') as f:
    for line in f:
        line = line.rstrip('\n')
        line = line.strip()
        if line:
            line_list.append(line)
            n_lines += 1
            n_chars += len(line)
        elif line_list:
            para_list.append('\n'.join(line_list))
            line_list = []

print('%8d chars' % n_chars)
print('%8d lines' % n_lines)
print('%8d paras' % len(para_list))
print('%.1f chars/para' % (n_chars / len(para_list)))


group_list = []
group = []
size = 0
for para in para_list:
    group.append(para)
    size += len(para)
    if size > min_group_size:
        group_list.append('\n\n'.join(group))
        group = []
        size = 0

print('%8d groups' % len(group_list))


def show(a_list):
    a_list.sort(key=lambda k: (len(k), k))
    for i, para in enumerate(a_list[:5]):
        print('%d: "%s"' % (i, para))


# show(group_list)

train_list = []
test_list = []
train_size = 0
test_size = 0

if random_split:
    level = level0 = test_frac
    for group in group_list:
        if test_size / test_frac < train_size / (1.0 - test_frac):
            level = (1.0 - level) / 2.0
        else:
            level /= 2.0
        if random.random() < level:
            test_list.append(group)
            test_size += len(group)
        else:
            train_list.append(group)
            train_size += len(group)
        # print('%.4f %.4f %7d %7d' % (level, test_size / (train_size + test_size), test_size, train_size))
        assert level != level0, (level, level0)
        level0 = level
else:
    for group in group_list:
        if test_size / test_frac < train_size / (1.0 - test_frac):
            test_list.append(group)
            test_size += len(group)
        else:
            train_list.append(group)
            train_size += len(group)


print('test =%5d %7d' % (len(test_list), test_size))
print('train=%5d %7d' % (len(train_list), train_size))
print('test=%.3f %.3f' % (len(test_list) / (len(test_list) + len(train_list)),
                         test_size / (test_size + train_size)))

with open(train_path, 'wt') as f:
    f.write('\n\n'.join(train_list))
with open(test_path, 'wt') as f:
    f.write('\n\n'.join(test_list))
