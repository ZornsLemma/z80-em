#!/bin/bash
set -e
(cd zexall; ./make.sh)
python make-tables.py > tables.beebasm
beebasm -w -do z.ssd -v -opt 3 -i em1.beebasm  > em1.lst
cp cpm-blank.dsd testcpm.dsd
python ~/Dropbox/cpm-tmpish/deinterleave.py
cpmcp -f acorn3a testcpm.dsk zexall/zexdoc-sf.cim 0:zexdoc.com
python ~/Dropbox/cpm-tmpish/interleave.py
