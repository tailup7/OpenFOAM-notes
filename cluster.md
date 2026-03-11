# ジョブスケジューラ

## インハウス計算機クラスタ
### OS
+ CentOS 7
<br>
自分が使用しているインハウス計算機クラスタは、ジョブスケジューラに PBS (Portable Batch System) を使用している。<br>
シェルスクリプトの拡張子は .sh ではなく .pbs とし、以下のコマンドでジョブ投入をする。
<br>
<br>
ジョブ投入コマンド

``` bash
$ qsub foo.pbs
```
<br>

投入されている全ジョブの確認

``` bash
$ qstat
```
<br>

全計算ノードの状態を確認するコマンド
``` bash
$ pbsnodes
```
<br>

実行中のジョブを終了するコマンド
``` bash
$ qdel <job ID> # 終了したいジョブのID
```
<br>

## 富岳
### OS
+ RHEL 8

富岳ではジョブスケジューラに富岳専用のジョブ管理システムである PJM (Priority Job Manager) を使用している。


## OpenMPI
OpenFOAM は OpenMPI を用いて並列化を行い、解析領域(=メッシュ) を空間的に複数に分割して各processでそれぞれ計算を進め、MPI通信で分割された境界の情報をやりとりしながら全体としての計算が進む。 

