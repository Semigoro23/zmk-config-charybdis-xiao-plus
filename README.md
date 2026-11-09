# Charybdis / XIAO nRF52840 Plus / Rev H PCB

Y13 Rev H試作基板とXIAO用ZMK設定。Rev HでもGPIO信号の割当はRev Gから維持しています。左右各XIAO nRF52840 Plus、左エンコーダー、右PMW3610に対応する試作用ファームウェアです。ビルド成功と実機動作確認は別です。実機試験は未実施です。
本PCBは、もともとnice!nano v2を搭載するPCBをベースに設計しています。nice!nano v2はBluetooth通信に対応していますが、日本の技適認証を取得していないため、日本国内での使用を想定し、技適認証に対応したXIAO nRF52840 Plusへ変更しました。

## Rev H 基板の発注データ

**[発注用Gerber ZIP](hardware/revH/Y13-XIAO-revH-order-gerbers.zip?raw=true)** · **[基板画像・発注／組立メモ](hardware/revH/README.md)**

2層・FR-4・板厚1.6 mm。XIAOの部品面をキャリアへ向けるRev Hです。旧Rev G以前のGerberは使用しないでください。取付高さと支持部材は実物で調整する前提の少量試作用で、ケース適合・電池充電・実機動作は未検証です。

左4×6＋5＝29キー、右4×6＋3＝27キー＋トラックボールに対応します。UF2名のrevGは既存ファームウェアの名前で、旧基板の取付方向を示すものではありません。

## 構成

- **右が親機（central）**。PCへのUSB／Bluetooth接続は右側を使います。左は子機。
- 左右各5行×6列。既存キーマップの配置・4レイヤー・56キーの割当を継承。60キー分のGPIOがあっても、空いている4位置は現キーマップに登録していません。
- 左エンコーダー：D6/P1.11、D8/P1.13、GND。
- 右PMW3610：SCLK D8/P1.13、SDIO D19/P1.07、NCS D13/P1.01、MOTION D6/P1.11。SPIのMOSI/MISOは同じSDIO線です。
- 左J7の予備D13/P1.01、D17/P1.03、D18/P1.05は予約のみ。キー等へ割り当てず、ファームウェアから駆動しません。
- 電池電圧はXIAO標準のP0.31とP0.14制御の分圧回路で取得。
- 充電電流選択P0.13は起動時に無プル入力とし、公称約50 mAを選びます。**D13/P1.01とは別ピン**です。100 mAモードは実装していません。
- RF送信出力を独自に上げる設定は移植していません。ソフトウェアだけで技適や組立後の無線適合を保証するものではありません。

ZMK v0.3の固定コミットと、元のDoctorWangWang PMW3610ドライバーの固定コミットを使用します。v0.3でのボード名は`seeeduino_xiao_ble`です。Plusの追加端子はGPIO番号で指定します。外付けQSPIフラッシュは使わず、設定はnRF内部フラッシュへ保存します。

## ダウンロードと書き込み

1. このリポジトリの **Actions → Build XIAO Plus Rev G firmware** を開き、成功した実行の`firmware`をダウンロード・展開します。
2. 初回またはペアリング不整合時は、左右ともRESETを素早く2回押してUSBドライブを表示し、`charybdis-xiao-plus-settings-reset.uf2`を各XIAOへコピーします。保存済みペアリング等が消えます。
3. 再度ブートローダーへ入り、左には`charybdis-xiao-plus-revG-left.uf2`、右には`charybdis-xiao-plus-revG-right-central.uf2`をコピーします。
4. 両側を起動し、右をUSBでPCへ接続してキーを確認します。その後、PCからBluetoothの`Charybdis XIAO+`へ接続します。

PCB上のRESETボタンを使うにはキャリアRESET端子からXIAO TP2への追加線が必要です。電源スイッチは電池＋だけを切ります。USB接続中の完全な電源OFFではありません。

## 電池と通電前確認

3.7 V・満充電4.2 Vの単セル電池を左右に1個ずつ独立接続する構成です。**電池の許容充電電流・保護回路は未確認**で、キャリアに逆接保護はありません。電池の極性、電源―GND短絡、追加線の導通を確認し、最初は電池を外してUSBで確認してください。

内蔵充電ICの約10時間タイマーに対し、50 mAでは400 mAhも充電状態によって時間切れの可能性があり、1100 mAhを深い放電から1回で満充電する用途には適合未確認です。このファームウェアはタイマー制限を解決しません。電池の仕様確認と実測が必要です。充電には電源SWをONにします。

USB位置の公差、ピン・スペーサーの固定と絶縁、スイッチの実物適合、電池固定、ケース収納は別途確認が必要です。元のnice!nano用UF2は書き込まないでください。

## 配線・変更

`docs/wiring.csv`がRev HのXIAO―キャリア対応、`docs/trackball.csv`が右の横一列6端子です。XIAOへの追加線は左7本・右6本、合計13本（任意BAT−補助線を除く）。主端子14本だけでは全機能は接続されません。

行はD1/D2/D4/D5/D7、列はD3/D0/D9/D10/D11/D12。ダイオード方向は元設定の`row2col`を維持。ボール方向・感度は既存設定を継承し、実物で必要なら調整します。予備GPIOの用途を追加する場合は対応する設定も変更してください。

## 出典

- 元設定・キーマップ：https://github.com/Semigoro23/zmk-config-nicenanov2-GERBER-adapter_Y13 （b3e0c08964bd929275c06698c74caaf6f8720078）
- ZMK：https://github.com/zmkfirmware/zmk （edf5c0814fd3ea202e43aad2d68fd32e882a518c）
- PMW3610：https://github.com/DoctorWangWang/zmk-pmw3610-driver （1d9c2c68ca76012e1b1e5f6ef02fa5eadc4ca399）
- Seeed公式：https://wiki.seeedstudio.com/XIAO_BLE/
- 充電IC：https://www.ti.com/lit/ds/symlink/bq25100.pdf

既存ファイルの著作権・ライセンス表記を維持しています。上流ソースのライセンスは各リポジトリを参照してください。
