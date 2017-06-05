# define
TOY = 'TOY'  # type: str

ARROW_CORNER = 'C'  # type: str
ARROW_LEFT = 'L'  # type: str
ARROW_UP = 'U'  # type: str

MATCH = 'M'  # type: str
INDEL_UP = 'U'  # type: str
INDEL_DOWN = 'D'  # type: str

k_unit = 10  # type: int
HAIRPIN_MIN = 200  # type: int
HAIRPIN_MAX = 400  # type: int
LOOP_MAX = 50  # type: int
ALPHA = 4  # type: int
BETA = 9  # type: int


def check_distance(distance: int) -> bool:
    return LOOP_MAX <= distance <= HAIRPIN_MAX


def check_loop_length(loop_length: int) -> bool:
    return 0 <= loop_length <= LOOP_MAX


def check_hairpin_sequence_length(seq_len: int) -> bool:
    return HAIRPIN_MIN <= seq_len <= HAIRPIN_MAX


toy_sequence = 'GCACGATAGATATACGATAATTAATAGCGAGAGGACAACGTGGAGCAGGGGACCGTACGTTTGACGAGCGTGCAACAGGAGAGCGATATTAGGGTAGAGACAGTGTGAGCT'  # type: str
toy_lcs = 'ATTATAGCGAGAGGACAACGTGGAGCAG'  # type: str
toy_loop = 'GGGACCGTACGTTT'  # type: str
