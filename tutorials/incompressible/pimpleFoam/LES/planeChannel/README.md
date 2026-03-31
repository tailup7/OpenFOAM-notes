# 使い方

### 権限を与える
すべてのジョブスクリプトに実行権限を与える。`planeChannnel/`フォルダ直下に`Allrun`, `Allclean`, `plot`があるのと、`planeChannel/setups.orig/common/`に`Allrun-parallel`などがあるので以下のコマンドでまとめて権限を与える

``` bash
find . -maxdepth 3 \( -name "Allrun*" -o -name "Allclean*" \) -type f -exec chmod +x {} \;
```

### 並列数を変える
デフォルトだと並列数が36になっているので、`planeChannel/setups.orig/common/system/decomposeParDict`ファイル内の`numberOfSubdomains`の値を使用マシンのコア数に応じて変更する。

### 計算結果の書き出し設定の変更
`planeChannel/setups.orig/common/system/controlDict`を本リポジトリの設定のように変える

特に、`purgeWrite`について、デフォルトでは`purgeWrite      3;`になっているはず。これは最新の3時刻分の流れ場の結果だけ残し、古いものは削除する、という意味なので、流れ場の時間発展をParaViewで可視化したい場合は 0に変更しておく 。ただし、出力される計算結果のファイルサイズが膨大になるのでその点は注意が必要

### 実行する
以前にも計算を実行して中途半端に生成物が残っている場合は`planeChannnel/`フォルダ直下で`./Allclean`してから、

``` bash
./Allrun
```

## 計算中でも途中までの計算結果を可視化したいとき
別ターミナルを開いて、
``` bash
reconstructPar
```
をすればよい。2回目以降は、一度生成した時刻フォルダを削除してから(`0/`は削除しないこと)再度`reconstructPar`するか、
``` bash
reconstructPar -newTimes
```
で追加で計算済みになった時刻フォルダを生成できる。
