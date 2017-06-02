# define
TOY = 'TOY'

ARROW_CORNER = 'C'
ARROW_LEFT = 'L'
ARROW_UP = 'U'

MATCH = 'M'
INDEL_UP = 'U'
INDEL_DOWN = 'D'

k_unit = 10
HAIRPIN_MIN = 200
HAIRPIN_MAX = 400
LOOP_MAX = 50
ALPHA = 4
BETA = 9


def check_distance(distance):
    return LOOP_MAX <= distance <= HAIRPIN_MAX


def check_loop_length(loop_length):
    return 0 <= loop_length <= LOOP_MAX


def check_hairpin_sequence_length(seq_len):
    return HAIRPIN_MIN <= seq_len <= HAIRPIN_MAX


toy_sequence = 'GCACGATAGATATACGATAATTAATAGCGAGAGGACAACGTGGAGCAGGGGACCGTACGTTTGACGAGCGTGCAACAGGAGAGCGATATTAGGGTAGAGACAGTGTGAGCT'
toy_lcs = 'ATTATAGCGAGAGGACAACGTGGAGCAG'
toy_loop = 'GGGACCGTACGTTT'