#!/bin/bash
python make-tables.py > tables.beebasm
beebasm -w -do z.ssd -v -opt 3 -i em1.beebasm  > em1.lst
