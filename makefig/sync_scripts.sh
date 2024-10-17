#!/bin/bash
source1="/home/jiang/Documents/jureca/benchmark/beNNch/makefig/*.py"
source2="/home/jiang/Documents/jureca/benchmark/beNNch/makefig/*.sh"
target="/home/jiang/git/beNNch-hj/makefig"

rsync -auv $source1 $source2 $target
