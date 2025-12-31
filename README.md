# OpenFOAM-notes

OpenFOAMのおぼえがき。環境構築とか、実際に使ったスクリプトとか。

### 動作確認環境
|Usage Type | Environment | OS                |         CPU / Cores                   |  Job Scheduler         | OpenFOAM |   Python       |
|-----------|-------------|-------------------|:-------------------------------------:|:----------------------:|:--------:|----------------|    
| shared    | HPC cluster | CentOS 7.4.1708   |  login: 10 cores, compute: 36×3, 32×2 |  Portable Batch System | v1612+   | Python 3.11.0  |
| shared    | Fugaku      | RHEL8.10          |  Fujitsu A64FX (48 cores / node)      |  Project Job Manager   | v2506    | Python 3.11.11 |
| private   | local       | ubuntu22.04.5     |                                       |             -          | v2312    | Python 3.13.0  | 
| private   | local       | ubuntu24.04(WSL2) |     8Cores                            |             -          | v2506    | Python 3.12.3(System default)|

上記の4つの環境を使っている。このリポジトリ内の設定ファイル(0/Uなど)やバッチファイル(*.sh や *.pbs)は、1つ目の環境(centOS7, OpenFOAM-v1612+)で使っている。

#### OpenFOAMのバージョンについて
OpenFOAMにはOpenCFD社によって年2回更新されるもの(OpenFOAM-v2312, OpenFOAM-v2406, ... )と、 OpenFOAM foundationによって年1回更新されるもの(OpenFOAM11(2022のもの), OpenFOAM12(2023のもの), OpenFOAM13(2024のもの), ...) とがあるが、とくにこだわりが無ければ前者のものでLinux環境に応じた最新のバージョンを利用するのが良いと思われる。最新のバージョンは https://www.openfoam.com/current-release で、各バージョンと Linux distribution との対応は https://www.openfoam.com/news/main-news/openfoam-v2506 で確認できる。


## OpenFOAMインストール手順
(例. UbuntuOSまたはWSLによるUbuntu環境にOpenFOAM-v2506をインストールする) <br>
Ubuntu(22.04 or 24.04)ターミナルを起動し、以下コマンドを入力 
``` bash
sudo apt update
sudo apt upgrade -y
sudo wget -O - http://dl.openfoam.com/add-debian-repo.sh | sudo bash
sudo apt install openfoam2506-default
```
これで、OpenFOAMが /usr/lib/openfoam/ にインストールされた。
自分のシェル設定ファイル(home/user/.bashrc)に、OpenFOAMの環境を自動で使えるようにするための設定(usr/lib/openfoam/openfoam2506/etc/bashrc に書いてある) を追加する以下のコマンドを実行
``` bash
echo "source /usr/lib/openfoam/openfoam2506/etc/bashrc" >> ~/.bashrc
source ~/.bashrc
```
設定ができたので、以下のコマンドで動作確認をしてみる。やっていることは、2D直交格子を生成し、キャビティ流れを`icoFoam`ソルバで解いている。
```
mkdir -p $FOAM_RUN
cd $FOAM_RUN
cp -r $FOAM_TUTORIALS/incompressible/icoFoam/cavity/cavity .
cd cavity
blockMesh
icoFoam
```
計算が完了すると、T=0.500までの物理量が表示されるはず。結果をparaviewで可視化するために、以下のコマンドを実行
```
foamToVTK
```
生成された `VTK` フォルダ内の `cavity_時刻.vtm` ファイルをparaviewで可視化すると、cavity流れ場が確認できる。

#### 参考リンク
+ [OpenFOAM のインストール](https://ss1.xrea.com/penguinitis.g1.xrea.com/study/OpenFOAM/install_memo/install_memo.html)

## ケース構成
OpenFOAMをインストールしたら、適当なチュートリアルケースからパッケージをコピーするなどして、以下のようなケース構成を用意する。
自分の解析したい条件に合わせて設定ファイルを追加したり、中身を書き換える。自身で用意したメッシュをインポートして流体解析を行う場合、以下のようなディレクトリ構成になる。

``` bash
  root/
   ├─ 0/                        # 初期条件・境界条件を設定
   │   ├─ U                     # 速度場
   │   └─ P                     # 圧力場
   ├─ constant/
   │   ├─ polyMesh/             # gmshToFoam や fluentMeshToFoam をした段階で生成される。はじめは不要。
   │   ├─ transportProperties   # 流体の物性値(動粘性係数) の設定
   │   └─ turbulenceProperties  # 乱流モデルの設定
   ├─ dynamicCode/              # 設定ファイル内でcodeFixedValue等の動的コードを使っていると、計算開始時に生成。はじめは不要。
   ├─ system/
   │   ├─ controlDict           # ソルバ、時間刻み、可視化用の出力刻み、終了時刻、functionObject(WSSの計算とか)の設定
   │   ├─ decomposeParDict      # 並列化するなら必要。しないなら不要。
   │   ├─ fvSchemes             # 数値スキーム(支配方程式の各項の離散化手法)の設定。
   │   ├─ fvSolution            # 連立方程式ソルバや収束条件の設定。
   │   └─ meshQualityDict       # メッシュ品質チェック用。基本的に不要。
   ├─ foo.msh                   # ファイル名は自由。流体解析するメッシュ。他にも(*.cas)とか。
   └─ read.foam                 # ファイル名は自由。ParaViewで可視化するための空フォルダ。計算には不要。
```

計算のために最低限必要なファイル・フォルダ構成は以下のようになる。
``` bash
  root/
   ├─ 0/                        
   │   ├─ U                     
   │   └─ P                     
   ├─ constant/
   │   ├─ transportProperties   
   │   └─ turbulenceProperties  
   ├─ system/
   │   ├─ controlDict           
   │   ├─ fvSchemes            
   │   └─ fvSolution  
   └─ foo.msh     
```


## 前処理と後処理
メッシュ生成ツールとして、以下の2つを使っている。
+ Ansys ICEM CFD
+ Gmsh

Ansys ICEM CFDは商用ツールであり、自身もいずれライセンスが切れるため、OSSであるGmshを主に使っている。このリポジトリ内のバッチファイル(*.sh や *.pbs)は、Gmsh形式とFluent形式のどちらでも対応するようにしている。<br>
<br>
また解析結果の可視化には ParaView を使用している。

## 実行
用意したメッシュファイルのデータ形式を OpenFOAM 側で読み込むためのコマンドを実行する。例えば Gmsh で作成したメッシュファイルなら、
``` bash
$ gmshToFoam foo.msh  # 他にも例えば、ICEM CFDで作成したメッシュなら、fluentMeshToFoam foo.msh 
```
次に、いちおうメッシュの品質を確認しておく。
``` bash
$ checkMesh
```
これで `mesh failed.` などが出たら、メッシュのどこかが破綻していて、ほとんどの場合計算が発散したりするのでメッシュファイルを修正するか作り直すこと。
`Mesh OK.`と出たらOK. <br>
(必要なら) メッシュファイルのスケール変換をする。(OpenFOAM は 長さの単位はメートル)
``` bash
# 医用画像の段階でmm単位であり、segmentation→smoothing→meshing までずっとmmで扱ってきたが、OpneFOAMはmで計算するため。
$ transformPoints -scale "(1e-3 1e-3 1e-3)" 
```
以上で下準備が終わったのでソルバを実行する。
``` bash
$ simpleFoam | tee log # ログ出力するオプションも付けておく
```
<br>
OpenFOAMは 圧力 p を p/rho として計算している(NS式の両辺をrhoで割ったものを解いているため)。<br>
なので、計算終了後に p (やwallShearStress) に rho (血液なら1060kg/m^3) を掛ける後処理をしておく。

``` bash
$ simpleFoam -postProcess -func "wallShearStress(patches (WALL); writeFields yes;)" -latestTime
$ python pa_convert.py --rho 1060 --time latest
```

※ pa_convert.py は 計算終了後の pファイル や wssファイル 内の数値を1060倍する自作コードです。<br>
　 この後処理コマンドが必須というわけではなく、計算結果のp (やwss) が p/rho になっていることが頭に入っていればOKです。

  
<br>

---
