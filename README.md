## how to use
1. `src/web_exporter/config.toml` を作成し wiki のパスワードなどを設定する
1. rye をインストール
   1. [参考記事](https://nsakki55.hatenablog.com/entry/2023/05/29/013658)
1. `rye sync`
1. `rye run python src/web_exporter/main.py`
1. `output/` 配下に markdown ファイルが出力される
