"""
Takes FASTQ records from STDIN; cuts trailing lowercase sequence and the
associated qualities, stashing them in the sequence id comment field as a
SAM-style tag: QT:Z:[seq_cut]+[qal_cut]. Existing comments are dropped.
Example usage:
	cutadapt --action=lowercase ...|python cutstash.py|bwa mem -C ...
"""
import sys


def cutstash(fh):
    try:
        for line in fh:
            # drop any existing comment
            sid = line.rstrip().split()[0]
            seq = next(fh).rstrip()
            plus = next(fh).rstrip()
            qual = next(fh).rstrip()
            assert sid.startswith('@')
            assert plus.startswith('+')
            # search backwards for efficiency
            pos = end = len(seq) - 1
            while pos >= 0 and seq[pos].islower():
                pos -= 1
            if pos < end:
                seq, seq_trimmed = seq[:pos+1], seq[pos+1:].upper()
                qual, qual_trimmed = qual[:pos+1], qual[pos+1:]
                tag = f'QT:Z:{seq_trimmed}+{qual_trimmed}'
                sid = f'{sid} {tag}'
            # faster than print()
            sys.stdout.write(f'{sid}\n')
            sys.stdout.write(f'{seq}\n')
            sys.stdout.write(f'{plus}\n')
            sys.stdout.write(f'{qual}\n')
    except StopIteration as si:
        sys.stderr.write(f'Unexpected end of FASTQ record at {sid}\n')
        return 2
    return 0


if __name__ == '__main__':
    if len(sys.argv) > 1:
        print(__doc__)
    else:
        sys.exit(cutstash(sys.stdin))
