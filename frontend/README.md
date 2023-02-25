# 概要

このディレクトリにはPolityLinkのフロントエンドのコードが置かれています。Gatsbyという静的サイトジェネレーターを使い、builderが生成したデータからページを作成します。

# 環境構築

記載のコードはMacOSに環境構築する場合です。適宜読み替えて実行してください。

## Gatsby

[Gatsby](https://www.gatsbyjs.com/docs/tutorial/part-0/)をインストールします。最新の情報は公式サイトを参照してください。

```
brew install node
```

```
nvm install 18
nvm use 18
```

```
npm install -g gatsby-cli
```

## ライブラリ
依存ライブラリをインストールします。
```
npm install
```

# 実行

## データの準備

builderが生成したデータを`artifact`というディレクトリに置く必要があります。builderがローカルで生成しているファイルを参照する場合は、シンボリックリンクを貼ると便利です。

```
ln -s ../builder/out/artifact artifact
```

## サイトの立ち上げ
開発時は`develop`コマンドを使えば http://localhost:8000 のサイトが随時更新されます。

```
gatsby develop -H 0.0.0.0
```

本番のファイルを確認したい場合は`build`してください。

```
gatsby build
gatsby serve -H 0.0.0.0
```