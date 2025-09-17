# OpenFOAM-notes
OpenFOAMのおぼえがき。血流解析のため。圧力駆動の流入条件、拍動流、WSS・OSI計算、並列化など。<br>
生体を対象にするので流体の密度は一定、なので扱うのは非圧縮性ソルバのみ。

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
