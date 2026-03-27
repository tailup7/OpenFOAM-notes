# 使い方

すべてのジョブスクリプトに実行権限を与える。`planeChannnel/`フォルダ直下に`Allrun`, `Allclean`, `plot`があるのと、`planeChannel/setups.orig/common/`に`Allrun-parallel`などがあるので以下のコマンドでまとめて権限を与える

``` bash
find . -maxdepth 3 \( -name "Allrun*" -o -name "Allclean*" \) -type f -exec chmod +x {} \;
```

以前にも計算を実行して中途半端に生成物が残っている場合は`planeChannnel/`フォルダ直下で`./Allclean`してから、

``` bash
./Allrun
```
