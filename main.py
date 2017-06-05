#! /usr/bin/env python3
# -*- coding: UTF-8 -*-

import argparse
from consts import *

parser = argparse.ArgumentParser(description='Hairpin Finder by soo. Please Enjoy!')
parser.add_argument('-v', '--verbose', help='increase output verbosity', action='store_true')
parser.add_argument('-t', '--toy', help='run with the given toy sequence', action='store_true')
parser.add_argument('input_file', help='input file to read a DNA sequence', type=argparse.FileType('r'))
args = parser.parse_args()


def lcs_length(s1: str, s2: str):
    # c 가 필요없을 것 같음. b 만으로 가능해 보임.
    m = len(s1)  # type: int
    n = len(s2)  # type: int
    b = [[0 for x in range(n + 1)] for y in range(m + 1)]
    c = [[0 for x in range(n + 1)] for y in range(m + 1)]

    for i in range(1, m + 1):
        b[i][0] = ARROW_UP
    for j in range(1, n + 1):
        b[0][j] = ARROW_LEFT

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                b[i][j] = ARROW_CORNER
                c[i][j] = c[i - 1][j - 1] + 1
            else:
                if c[i - 1][j] >= c[i][j - 1]:
                    b[i][j] = ARROW_UP
                    c[i][j] = c[i - 1][j]
                else:
                    b[i][j] = ARROW_LEFT
                    c[i][j] = c[i][j - 1]

    return b, c


def match_lcs(b, s1: str, s2: str, match_result):
    i = len(s1)
    j = len(s2)
    if i == 0 and j == 0:
        return
    if b[i][j] == ARROW_CORNER:
        match_lcs(b, s1[:-1], s2[:-1], match_result)
        match_result.append((MATCH, s1[i - 1]))
    elif b[i][j] == ARROW_UP:
        match_lcs(b, s1[:-1], s2, match_result)
        match_result.append((INDEL_UP, s1[i - 1]))
    else:
        match_lcs(b, s1, s2[:-1], match_result)
        match_result.append((INDEL_DOWN, s2[j - 1]))


def lcs_match_pairs(s1: str, s2: str):
    b, c = lcs_length(s1, s2)
    match_result = []
    match_lcs(b, s1, s2, match_result)
    return match_result


def get_extended_arm(match_pairs, is_eq_seq: bool):
    idx = 0  # type: int
    prev_match_idx = -1  # type: int
    for pair_type, char in match_pairs:
        if pair_type != MATCH:
            idx += 1
            continue

        if idx == 0:
            prev_match_idx = idx
            idx += 1
            continue

        if match_pairs[idx - 1][0] == MATCH:
            prev_match_idx = idx
            idx += 1
            continue

        region_start = idx - BETA // 2
        region_start = region_start if region_start >= 0 else 0
        region_end = idx + BETA // 2 + 1
        region_end = region_end if region_end <= len(match_pairs) else len(match_pairs)

        nr_indel = len(list(filter(lambda pair: pair[0] != MATCH, match_pairs[region_start:region_end])))
        if nr_indel >= ALPHA:
            # stop 조건일 때
            arm = match_pairs[:prev_match_idx + 1]

            return prev_match_idx, arm

        # FIXME optimization idx 를 끝까지가 아니라 절반만 돌 수 도 있음
        prev_match_idx = idx
        idx += 1

    # stop 조건을 못만났을때, 전체가 다 확장된 팔이 되는데, 전체가 음수면 1짜리 루프가 있다고 봐야.
    arm = match_pairs[:prev_match_idx + 1] if prev_match_idx != -1 else (
        match_pairs if not is_eq_seq else match_pairs[:len(match_pairs) // 2])
    return prev_match_idx, arm


def get_loop(seq_m, extended_arm_in_loop):
    return list(filter(
        lambda pair: pair[0] != INDEL_DOWN,
        seq_m[len(extended_arm_in_loop):len(seq_m) - len(extended_arm_in_loop)]
    ))


def get_sequence() -> str:
    if args.toy:
        return toy_sequence
    else:
        sequence = ''
        with args.input_file as f:
            f.readline()
            sequence = f.readline()
        # else:
        #     f = open(sys.stdin, 'r')
        #     sequence = args.input_file.readline()
        #     f.close()
        return sequence


def reverse_seq(s: str) -> str:
    return ''.join(reversed(s))


def seq_to_match_pairs(seq: str):
    return list(map(lambda c: (MATCH, c), seq))


def match_pairs_to_seq(match_pairs) -> str:
    return ''.join(map(lambda pair: pair[1], match_pairs))


if __name__ == '__main__':
    full_seq = get_sequence()  # type: str

    k_mer_start = 0  # type: int

    while k_mer_start <= len(full_seq) - LOOP_MAX:
        k_mer = full_seq[k_mer_start: k_mer_start + k_unit]  # type: str
        # 문제 조건에 따르면 k_mer_start + HAIRPIN_MAX + 1 를 해야하는데, 그렇게 되면
        # k_seq_left_right_len 계산에서 HAIRPIN_MAX - 2 * k_unit - len(k_seq_middle) 가 1 오버되어 음수가 되어 버린다.
        # 이 문제를 막기 위해 k_mer_start + HAIRPIN_MAX 로 한다.
        seq_in_distance = full_seq[k_mer_start + LOOP_MAX: k_mer_start + HAIRPIN_MAX]  # type: str
        k_mer_rev = reverse_seq(k_mer)  # type: str

        # only first k_mer_rev is used.
        # FIXME k_mer_rev 가 지켜야할 조건은 loop max 조건밖에 없는데, 이 조건은 작은 것에서 지켜지지 않고 큰것에서 지켜지는 경우가 없다.
        k_mer_rev_start = seq_in_distance.find(k_mer_rev)  # type: int

        if k_mer_rev_start == -1:
            k_mer_start += 1
        else:
            k_mer_rev_start = k_mer_rev_start + LOOP_MAX + k_mer_start
            k_seq_middle = full_seq[k_mer_start + k_unit: k_mer_rev_start]  # type: str

            # FIXME // 2 를 할 때, 홀짝을 고려해야할 수 있음. 일단은 나이브하게.
            k_seq_left_right_len = (HAIRPIN_MAX - 2 * k_unit - len(k_seq_middle)) // 2  # type: int

            # lower bound check
            k_seq_left = full_seq[
                         k_mer_start - k_seq_left_right_len
                         if k_mer_start - k_seq_left_right_len >= 0
                         else 0: k_mer_start
                         ]  # type: str

            # upper bound check is done automatically by python
            k_seq_right = full_seq[
                          k_mer_rev_start + k_unit:
                          k_mer_rev_start + k_unit + k_seq_left_right_len
                          ]  # type: str

            k_seq_right_rev = reverse_seq(k_seq_right)  # type: str
            k_seq_middle_rev = reverse_seq(k_seq_middle)  # type: str

            match_lr = lcs_match_pairs(k_seq_left, k_seq_right_rev)
            match_m = lcs_match_pairs(k_seq_middle, k_seq_middle_rev)

            match_lr.reverse()

            last_arm_idx1, arm_lr = get_extended_arm(match_lr, False)
            last_arm_idx2, arm_m = get_extended_arm(match_m, True)

            arm_lr.reverse()
            extended_arm = arm_lr + seq_to_match_pairs(k_mer) + arm_m

            left_arm = list(filter(lambda pair: pair[0] != INDEL_DOWN, extended_arm))
            right_arm = list(filter(lambda pair: pair[0] != INDEL_UP, extended_arm))
            right_arm.reverse()
            arm_lcs = list(filter(lambda pair: pair[0] == MATCH, extended_arm))
            loop = get_loop(match_m, arm_m)

            if len(loop) > LOOP_MAX:
                k_mer_start += 1
                continue

            left_arm_seq = match_pairs_to_seq(left_arm)
            right_arm_seq = match_pairs_to_seq(right_arm)

            hairpin_seq = match_pairs_to_seq(left_arm + loop + right_arm)
            arm_lcs_seq = match_pairs_to_seq(arm_lcs)
            loop_seq = match_pairs_to_seq(loop)

            if args.verbose:
                print('k_mer')
                print(k_mer)
                print('k_mer_rev')
                print(k_mer_rev)
                print('k_mer_start')
                print(k_mer_start)
                print('k_mer_rev_start')
                print(k_mer_rev_start)
                print('k_seq_middle')
                print(k_seq_middle)

                print('k_seq_left')
                print(k_seq_left)
                print('k_seq_right')
                print(k_seq_right)
                print('k_seq_right_rev')
                print(k_seq_right_rev)

                print('left_arm_seq_ex')
                print(match_pairs_to_seq(list(filter(lambda pair: pair[0] != INDEL_DOWN, arm_lr))))
                print('left_arm_seq')
                print(left_arm_seq)
                print('right_arm_seq_ex')
                print(match_pairs_to_seq(list(filter(lambda pair: pair[0] != INDEL_UP, arm_lr))))
                print('right_arm_seq')
                print(right_arm_seq)

                print('middle_arm_lcs')
                print(match_pairs_to_seq(list(filter(lambda pair: pair[0] == MATCH, arm_m))))

                print('hairpin')
                print(hairpin_seq)
                print('arm_lcs_seq')
                print(arm_lcs_seq)
                print('loop_seq')
                print(loop_seq)
            else:
                print(hairpin_seq)
                print(arm_lcs_seq)
                print(loop_seq)

            print()

            k_mer_start = k_mer_rev_start + k_unit + k_seq_left_right_len
