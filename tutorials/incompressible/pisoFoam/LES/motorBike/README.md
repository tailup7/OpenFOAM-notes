# motorBikeLES

`tutorials/incompressible/pisoFoam/LES/motorBike` を適当な作業ディレクトリにコピーする。階層構造は以下のようになっている

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


まず実行権限を与える。`motorBike`フォルダ直下で

``` bash
chmod +x Allrun Allclean
chmod +x motorBike/Allrun motorBike/Allclean
chmod +x lesFiles/Allrun
```
