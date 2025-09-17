#!/bin/bash
set -e  

gmshToFoam foo.msh

# gmshは単位が無く、mmスケールでメッシュ生成していたため、mスケールに直す
transformPoints -scale "(1e-3 1e-3 1e-3)"

# constant/polyMesh/boundary ファイル内の "WALL" の "type" を "patch"から "wall" に変更
sed -i 's/\("WALL"[ \t]*(\|WALL\)/\1/; s/\(type[ \t]*\)patch/\1wall/' constant/polyMesh/boundary

# 計算実行。ログをコンソールに流しながらファイルとしても出力する
simpleFoam | tee log
