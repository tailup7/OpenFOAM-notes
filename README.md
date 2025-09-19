# OpenFOAM-notes
血流解析に関するOpenFOAM設定・スクリプトを記録した備忘録。<br>

圧力駆動の流入条件、拍動流、WSS・OSI計算、並列化など。<br>
生体を対象にするので流体の密度は一定、なので扱うのは非圧縮性ソルバのみ。

### 環境

|usage type | environment | OS                |  job scheduler         | OpenFOAM |   Python      |
|-----------|-------------|-------------------|:----------------------:|----------|---------------|    
| shared    | HPC cluster | centOS 7.4.1708   |  Portable Batch System | v1612+   | Python 3.11.0 |
| private   | local       | ubuntu22.04.5     |             -          | v2312    | Python 3.13.0 | 

上記の2つの環境を使い分けている。このリポジトリ内の設定ファイル(0/Uなど)やバッチファイル(*.sh や *.pbs)は、1つ目の環境(centOS7, OpenFOAM-v1612+)で使っている。

### 前処理と後処理
メッシュ生成ツールとして、以下の2つを使っている。
+ Ansys ICEM CFD
+ Gmsh

Ansys ICEM CFDは商用ツールであり、自身もいずれライセンスが切れるため、OSSであるGmshを主に使っている。このリポジトリ内のバッチファイル(*.sh や *.pbs)は、Gmshで生成したファイルに対応したスクリプトになっている。<br>
<br>
また解析結果の可視化には ParaView を使用している。


## 環境構築

## ケース構成
OpenFOAMをインストールしたら、適当なチュートリアルケースからパッケージをコピーするなどして、以下のようなケース構成を用意する。
自分の解析したい条件に合わせて設定ファイルを追加したり、中身を書き換える。

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
   ├─ foo.msh                   # 流体解析するメッシュ。ファイル名は自由。形式は .fluent とかでも可。
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
