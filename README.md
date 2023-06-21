A very simple tool that takes FASTQ records from STDIN, cuts trailing lowercase sequence and the associate qualities, and stashes them in the sequence id comment field as a SAM-style tag:
```
QT:Z:[seq_cut]+[qual_cut]
```
Existing comments are dropped.

## Rationale

We have two mildly confliciting pipeline requirements:

1. Adapter sequence must be completely removed before alignment so that soft-clipped alignments are (more likely to be) "real" and usable for structural variant detection.
1. Original fastq sequence and qualities must be completely recoverable from the aligned records.

A solution is to use [cutadapt](https://github.com/marcelm/cutadapt) with `--action=lowercase` to identify adapter sequence, then use this tool to actually cut the sequence and qualities and store them in the FASTQ as a SAM-style tag in the sequence id comment. The tag in the comment is added to the alignment record by [bwa](https://github.com/lh3/bwa) when run with `-C` option.

## Build / Install

Two implementations are included. The Python one is just a script that needs no installation; it has been tested with Python 3.9+ but probably works with lots of other versions. The C++ one requires C++11 and the executable can be built simply with:
```
g++ cutstash.cxx -o cutstash
```

## Usage

Example (Python version):
```
...|cutadapt --action=lowercase ... -|python cutstash.py|bwa mem -C ...
```
Example (compiled version):
```
...|cutadapt --action=lowercase ... -|cutstash|bwa mem -C ...
```

The compiled version has a little more than twice the througput of the Python script but that's likely irrelevant in a pipeline where the bottleneck is the aligner.
