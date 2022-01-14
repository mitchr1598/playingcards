

def concat_by_line(strings: list, sep=''):
    if len(strings) > 2:
        return concat_by_line_two(strings[0], concat_by_line(strings[1:], sep=sep), sep=sep)
    else:
        return concat_by_line_two(strings[0], strings[1], sep=sep)


def concat_by_line_two(s1, s2, sep=''):
    return '\n'.join([l1 + sep + l2 for l1, l2 in zip(s1.split('\n'), s2.split('\n'))])


