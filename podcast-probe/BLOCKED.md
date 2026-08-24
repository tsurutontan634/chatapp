# ポッドキャスト配信プローブ — 通信ブロック記録

## 結論

このコンテナから対象URLへの通信は **ネットワークポリシーによって拒否** されました。
配信構造の採取(index.html / RSSフィード / mp3 の取得)は実施できていません。

## 対象

- URL: `https://pub-1414ccf484cc4bba82adcba7706654cb.r2.dev/099760db6104196bd02cff2d/index.html`
- ホスト: `pub-1414ccf484cc4bba82adcba7706654cb.r2.dev:443`

## 実行時刻(UTC)

- 1回目: 2026-08-24T16:22:48Z
- 2回目(再試行): 2026-08-24T16:23:01Z
- 記録作成: 2026-08-24T16:23:01Z

## 実行コマンド

```
curl -sS -o podcast-probe/index.html -w "%{http_code}" \
  "https://pub-1414ccf484cc4bba82adcba7706654cb.r2.dev/099760db6104196bd02cff2d/index.html"
```

## エラー全文

1回目・2回目とも同一の結果:

```
curl: (56) CONNECT tunnel failed, response 403
HTTP_CODE=000
EXIT=56
```

`HTTP_CODE=000` は、HTTPレスポンスに到達する前にプロキシがCONNECTトンネルの確立自体を拒否したことを示します(上位のHTTPステータスは返っていません)。

## エージェントプロキシの診断ログ

`$HTTPS_PROXY/__agentproxy/status` より該当部分を抜粋:

```json
"recentRelayFailures": [
  {
    "ts": "2026-08-24T16:22:48.030Z",
    "kind": "connect_rejected",
    "detail": "gateway answered 403 to CONNECT (policy denial or upstream failure)",
    "host": "pub-1414ccf484cc4bba82adcba7706654cb.r2.dev:443"
  },
  {
    "ts": "2026-08-24T16:23:01.432Z",
    "kind": "connect_rejected",
    "detail": "gateway answered 403 to CONNECT (policy denial or upstream failure)",
    "host": "pub-1414ccf484cc4bba82adcba7706654cb.r2.dev:443"
  }
]
```

## 原因の解釈

- 送信HTTPS通信は事前設定済みのエージェントプロキシ経由となり、宛先ホストはこの環境のegressポリシーで許可されたホスト一覧(`noProxy` / 許可リスト)に含まれていません。
- そのため `r2.dev` ドメインへのCONNECTがゲートウェイで **403(policy denial)** として拒否されました。
- これは環境側のネットワークポリシーによる制御であり、コンテナ内の設定不備やTLS証明書の問題ではありません(TLS検証を無効化するなどの回避は行っていません)。

## リトライ

指示に従い、再試行は1回のみ実施。2回とも同一のポリシー拒否のため、以降の採取処理には進んでいません。

## 許可する場合の対応(参考)

この宛先を許可するには、この環境のネットワークポリシー(egress許可リスト)に
`*.r2.dev`(または当該バケットのホスト)を追加する必要があります。
許可後に本プローブを再実行すれば、index.html・RSSフィード・mp3の採取に進めます。
