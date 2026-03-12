# motorBikeLES

## 概要
チュートリアルケース`motorBikeLES`を, 原点(0,0,0)を通り面ベクトル(0,1,0)の断面でU, nut, nuTilda, p などをanimetion可視化するための手順。`lesFiles/controlDict`のように、あらかじめ断面のみを出力するように設定しておかないと、動画のような時間解像度(writeInterval)、時間長さ(endTime)で計算すると数百Gb程度のファイルサイズになってしまう。


## 手順
1. `tutorials/incompressible/pisoFoam/LES/motorBike` を適当な作業ディレクトリにコピーする。階層構造は以下のようになっている

   ``` bash
   motorBike/
      ├─ lesFiles/                # LES計算に使う設定ファイル群
      │   ├─ Allrun               #
      │   ├─ controlDict          # 
      │   ├─ fvSchemes            # 
      │   ├─ fvSolution            #
      │   └─ turbulenceProperties  # 
      ├─ motorBike/
      │   ├─ 0.orig/          
      │   ├─ constant/
      │   ├─ system/
      │   ├─ Allclean  
      │   └─ Allrun
      ├─ Allclean
      └─ Allrun  
   ```

2. アニメーションとして見やすくするために、`lesFiles/controlDict`をこのリポジトリにある`lesFiles/controlDict`に置き換える.


3. 実行権限を与える。`motorBike`フォルダ直下で

   ``` bash
   chmod +x Allrun Allclean
   chmod +x motorBike/Allrun motorBike/Allclean
   chmod +x lesFiles/Allrun
   ```

4. 実行する
   ``` bash
   ./Allrun
   ```

   実行すると、まず`motorBike/motorBike`フォルダで計算が走る。これはsimpleFoamソルバ, 層流モデルでの計算。endTime=500まで計算した後、`motorBike/motorBikeLES`フォルダが作成され、`lesFiles`の設定ファイルがコピーされたあと、endTime=500の状態を初期場として`motorBike/motorBikeLES`フォルダで計算が走る。これはpisoFoamソルバ, LESモデルによる計算。(default設定のままの場合)どちらも並列数は8で実行される。

5. `motorBikeLES/y0Plane/`に出力されるvtpファイル群を、ParaViewでanimetionとして可視化するために、例えば以下のような`.pvd`ファイルを作成する. 
   ``` bash
   <?xml version="1.0"?>
   <VTKFile type="Collection" version="0.1">
     <Collection>
       <DataSet timestep="0.005" file="0005.vtp"/>
       <DataSet timestep="0.01" file="0010.vtp"/>
       <DataSet timestep="0.015" file="0015.vtp"/>
       <DataSet timestep="0.02" file="0020.vtp"/>
       <DataSet timestep="0.025" file="0025.vtp"/>
       <DataSet timestep="0.03" file="0030.vtp"/>
       <DataSet timestep="0.035" file="0035.vtp"/>
       <DataSet timestep="0.04" file="0040.vtp"/>
       <DataSet timestep="0.045" file="0045.vtp"/>
       <DataSet timestep="0.05" file="0050.vtp"/>
       ...
       ...
       ...
     </Collection>
   </VTKFile>
   ```
   そのために、`convert_vtp_series.py`を実行する。生成される`forParaview/y0Plane/y0Plane.pvd`をParaViewにimportすると、animetion再生と保存ができる。





