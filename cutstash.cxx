#include <iostream>

using namespace std;

int main(int argc, char* argv[]) {

  if (argc > 1) {
    cout << "Takes FASTQ records from STDIN; cuts trailing lowercase sequence and the\n";
    cout << "associated qualities, stashing them in the sequence id comment field as a\n";
    cout << "SAM-style tag: ZT:Z:[seq_cut]+[qal_cut]. Existing comments are dropped.\n";
    cout << "Example usage:\n";
    cout << "\tcutadapt --action=lowercase ...|cutstash|bwa mem -C ...\n";
    return 0;
  }

  // Un-sync and un-tie the I/O; this makes a HUGE difference in speed when
  // reading from stdin and writing to stdout with streams.
  ios::sync_with_stdio(false);
  cin.tie(0);

  string sid, seq, seq_cut, sep, qal, qal_cut;
  int64_t end, pos, space;
  while(getline(cin, sid)) {
     // drop any existing comment
     space = sid.find_first_of(" \t");
     if (space != string::npos){
       sid = sid.substr(0, space);
     }
     getline(cin, seq);
     getline(cin, sep);
     getline(cin, qal);
     end = pos = seq.length() - 1;
     while (pos >= 0 && islower(seq[pos])) { pos--; }
     if (pos < end) {
       seq_cut = seq.substr(pos+1, string::npos);
       for (auto & c: seq_cut) { c = toupper(c); }
       seq = seq.substr(0, pos+1);
       qal_cut = qal.substr(pos+1, string::npos);
       qal = qal.substr(0, pos+1);
       sid = sid + " ZT:Z:" + seq_cut + "+" + qal_cut;
     } 
     cout << sid << "\n";
     cout << seq << "\n";
     cout << sep << "\n";
     cout << qal << "\n";
  }
  return 0;
}
