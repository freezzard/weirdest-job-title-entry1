"""Weirdest Job Title: Blind Judge Showdown -- entry 1.

A single job title of at most 60 characters, chosen by a small local
tournament held inside this program. Twelve candidate titles are scored
against the five judge criteria published in RULES.txt, in the order the
judge weighs them:

  1. weird job title, a few words naming an odd job
  2. stranger than ordinary work, a job nobody has heard of
  3. funny, with a twist that lands on the first read
  4. sounds like a real job, specific enough to picture the person
  5. reads instantly, short enough to take in at a glance

The program picks the highest total, breaks ties by the head-to-head
order recorded below, checks the gate (1 to 60 characters, UTF-8, not
only white space), confirms the winning bytes against the digest fixed
in this file, and writes exactly the winning title, nothing more, to
/output/entry.txt. The run is deterministic: the same input always
produces the same bytes.
"""

import hashlib
import os
import sys


WJT_MAX_CHARS = 60
WJT_MIN_CHARS = 1
WJT_OUTPUT_PATH = "/output/entry.txt"
WJT_OUTPUT_DIR = "/output"

# Digest of the winning title bytes, measured on the first local run.
WJT_EXPECTED_SHA256 = "9b78ba6317045e456b4fdb6b0d18929dbc1d58ce8e6c385aede364541904cba2"


# Candidate titles, each with five criterion scores in judge order.
# Scores were fixed during the local tournament in this session.
WJT_CANDIDATES = (
    {
        "title": "Senior Apologizer for Self-Driving Cars",
        "scores": (5, 5, 5, 4, 4),
        "note": "Real-sounding senior title plus one vivid twist: cars that need apologies.",
    },
    {
        "title": "Lost Sock Reuniter, Laundromat Division",
        "scores": (5, 5, 5, 4, 4),
        "note": "Everybody has lost a sock; a whole division reunites them.",
    },
    {
        "title": "Official Sigh Counter, Open-Plan Office",
        "scores": (5, 5, 5, 4, 4),
        "note": "A measurable office misery, counted by an official.",
    },
    {
        "title": "Cloud Shape Approver, Sky Division",
        "scores": (5, 5, 4, 3, 5),
        "note": "A bureaucrat for the sky, approving shapes one cloud at a time.",
    },
    {
        "title": "Underwater Basket Weaving Inspector",
        "scores": (4, 4, 4, 4, 5),
        "note": "The classic joke major, inspected for real this time.",
    },
    {
        "title": "Professional Mourner, Funerals Only",
        "scores": (4, 3, 4, 5, 5),
        "note": "A genuinely old profession, narrowed to one venue.",
    },
    {
        "title": "Senior Penguin Counter, Antarctica",
        "scores": (4, 4, 3, 5, 5),
        "note": "A real Antarctic job, made stranger by the seniority.",
    },
    {
        "title": "Pet Psychic for Grumpy Cats",
        "scores": (4, 4, 4, 3, 5),
        "note": "The cats are grumpy, the psychic is professional.",
    },
    {
        "title": "Professional Pillow Fluffer, Five-Star Hotels",
        "scores": (4, 4, 4, 4, 4),
        "note": "Luxury service taken to its logical, fluffy end.",
    },
    {
        "title": "Expert in Awkward Silence, Meetings",
        "scores": (4, 4, 5, 3, 4),
        "note": "Every meeting has the silence; this person owns it.",
    },
    {
        "title": "Moon Dust Sweeper, Night Shift",
        "scores": (4, 4, 3, 3, 5),
        "note": "Somebody has to sweep the moon, and only at night.",
    },
    {
        "title": "Chief Nap Quality Inspector",
        "scores": (3, 3, 4, 4, 5),
        "note": "Naps, but inspected to a standard.",
    },
)


# Head-to-head order among the three candidates tied at 23 points.
# The winner beat both rivals on the funny-twist criterion; the
# runner-up beat the third on first-read relatability.
WJT_TIE_ORDER = (
    "Senior Apologizer for Self-Driving Cars",
    "Lost Sock Reuniter, Laundromat Division",
    "Official Sigh Counter, Open-Plan Office",
)


def wjt_total_score(candidate):
    """Add up one candidate's five criterion scores."""
    scores = candidate["scores"]
    running_total = 0
    for single_score in scores:
        running_total = running_total + single_score
    return running_total


def wjt_tie_rank(title):
    """Position of a title in the head-to-head order, or a large number."""
    rank = 0
    for ordered_title in WJT_TIE_ORDER:
        if ordered_title == title:
            return rank
        rank = rank + 1
    return 1000


def wjt_candidate_is_better(total, tie_rank, length, best_total, best_tie_rank, best_length):
    """Decide whether a candidate beats the current best.

    Highest total wins. A tie is settled by the recorded head-to-head
    order, then by the shorter title.
    """
    if total > best_total:
        return True
    if total == best_total and tie_rank < best_tie_rank:
        return True
    if total == best_total and tie_rank == best_tie_rank and length < best_length:
        return True
    return False


def wjt_pick_winner(candidates):
    """Pick the tournament winner deterministically."""
    best_candidate = None
    best_total = -1
    best_tie_rank = 1000
    best_length = 1000000
    for candidate in candidates:
        total = wjt_total_score(candidate)
        tie_rank = wjt_tie_rank(candidate["title"])
        length = len(candidate["title"])
        better = wjt_candidate_is_better(
            total, tie_rank, length, best_total, best_tie_rank, best_length
        )
        if better:
            best_candidate = candidate
            best_total = total
            best_tie_rank = tie_rank
            best_length = length
    return best_candidate


def wjt_is_valid_title(title):
    """Apply the sealed gate: 1 to 60 characters, not only white space."""
    if title is None:
        return False
    if len(title) < WJT_MIN_CHARS:
        return False
    if len(title) > WJT_MAX_CHARS:
        return False
    if title.strip() == "":
        return False
    if "\n" in title:
        return False
    if "\r" in title:
        return False
    return True


def wjt_title_bytes(title):
    """Encode the title as UTF-8 bytes, exactly as the gate reads them."""
    return title.encode("utf-8")


def wjt_sha256_hex(data):
    """Hex digest of bytes, used to prove the two runs match."""
    digest = hashlib.sha256(data)
    return digest.hexdigest()


def wjt_digest_matches(title):
    """Check the winning bytes against the digest fixed in this file."""
    digest = wjt_sha256_hex(wjt_title_bytes(title))
    if digest != WJT_EXPECTED_SHA256:
        return False
    return True


def wjt_prepare_output_dir(path):
    """Create the output directory when it is missing."""
    if os.path.isdir(path):
        return True
    os.makedirs(path, exist_ok=True)
    return os.path.isdir(path)


def wjt_write_entry(path, title):
    """Write exactly the title bytes to the entry file, nothing more."""
    data = wjt_title_bytes(title)
    handle = open(path, "wb")
    handle.write(data)
    handle.close()
    return len(data)


def wjt_read_entry(path):
    """Read the entry file back as bytes for verification."""
    handle = open(path, "rb")
    data = handle.read()
    handle.close()
    return data


def wjt_verify_entry(path, title):
    """Confirm the file on disk holds exactly the winning title."""
    expected = wjt_title_bytes(title)
    actual = wjt_read_entry(path)
    if actual != expected:
        return False
    return True


def wjt_report_winner(candidate, written_bytes, digest):
    """Print a short human-readable summary of the run."""
    title = candidate["title"]
    total = wjt_total_score(candidate)
    print("winner: " + title)
    print("characters: " + str(len(title)))
    print("bytes written: " + str(written_bytes))
    print("tournament total: " + str(total) + " / 25")
    print("sha256: " + digest)
    print("output: " + WJT_OUTPUT_PATH)


def wjt_run():
    """Run the whole entry: pick, gate, write, verify, report."""
    winner = wjt_pick_winner(WJT_CANDIDATES)
    if winner is None:
        print("error: no candidate survived the tournament")
        return 1
    title = winner["title"]
    if wjt_is_valid_title(title) is False:
        print("error: winning title fails the gate: " + repr(title))
        return 2
    if wjt_digest_matches(title) is False:
        print("error: winning bytes differ from the fixed digest")
        return 3
    if wjt_prepare_output_dir(WJT_OUTPUT_DIR) is False:
        print("error: cannot prepare output directory: " + WJT_OUTPUT_DIR)
        return 4
    written = wjt_write_entry(WJT_OUTPUT_PATH, title)
    if written != len(wjt_title_bytes(title)):
        print("error: short write to " + WJT_OUTPUT_PATH)
        return 5
    if wjt_verify_entry(WJT_OUTPUT_PATH, title) is False:
        print("error: verification mismatch on " + WJT_OUTPUT_PATH)
        return 6
    digest = wjt_sha256_hex(wjt_title_bytes(title))
    wjt_report_winner(winner, written, digest)
    return 0


def main(argv):
    """Entry point: ignore extra arguments, run once, exit with status."""
    if len(argv) > 1:
        print("note: extra arguments ignored: " + " ".join(argv[1:]))
    status = wjt_run()
    return status


if __name__ == "__main__":
    sys.exit(main(sys.argv))
