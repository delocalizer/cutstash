"""
Takes FASTQ records from STDIN; cuts trailing lowercase sequence and the
associated qualities, stashing them in the sequence id comment field as a
SAM-style tag: QT:Z:[seq_cut]+[qal_cut]. Existing comments are dropped.
Example usage:
	cutadapt --action=lowercase ...|python cutstash.py|bwa mem -C ...
"""
import sys

LC = {'a', 'c', 'g', 't'}

def main():
    cutstash(sys.stdin)

def cutstash(fh):
    try:
        while True:
            # drop any existing comment
            sid = next(fh).split()[0]
            seq = next(fh).rstrip()
            plus = next(fh).rstrip()
            qual = next(fh).rstrip()
            assert sid.startswith('@')
            assert plus.startswith('+')
            # search backwards for efficiency
            pos = end = len(seq) - 1
            while pos >= 0 and seq[pos] in LC:
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
    except StopIteration:
        pass

if __name__ == '__main__':
    if len(sys.argv) > 1:
        print(__doc__)
    else:
        main()
