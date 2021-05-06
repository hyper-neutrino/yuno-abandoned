mapping = dict((x + [""])[:2] for x in map(str.split, """ウ ]
カ ka
ケ ke
キ ki
コ ko
ク ku
タ ta
テ te
チ chi
ト to
ツ tsu
サ sa
セ se
シ si
ソ so
ス su
ナ na
ネ ne
ニ ni
ノ no
ヌ nu
ハ ha
ヘ he
ヒ hi
ホ ho
フ fu
マ ma
メ me
ミ mi
モ mo
ム mu
ラ ra
レ re
リ ri
ロ ro
ル ru
ヤ ya
ヨ yo
ユ yu
ワ wa
ヲ wo
ガ ga
ゲ ge
ギ gi
ゴ go
グ gu
ザ za
ゼ ze
ジ zi
ゾ zo
ズ zu
ダ da
デ de
ヂ di
ド do
ヅ du
バ ba
ベ be
ビ bi
ボ bo
ブ bu
パ pa
ペ pe
ピ pi
ポ po
プ pu
ン \\
キャ "
キョ '
キュ +
チャ /
チョ :
チュ _
シャ <
ショ =
シュ >
ニャ an
ニョ on
ヒャ `
ヒョ {
ヒュ }
ミャ (
ミョ )
ミュ |
リャ ar
リョ or
リュ ur
ギャ
ギョ in
ギュ ng
ジャ
ジョ
ジュ
ヂャ
ヂョ
ヂュ
ビャ
ビョ
ビュ
ピャ
ピョ
ピュ
ッカ kka
ッケ kke
ッキ kki
ッコ kko
ック kku
ッタ tta
ッテ tte
ッチ tti
ット tto
ッツ ttu
ッサ ssa
ッセ sse
ッシ ssi
ッソ sso
ッス ssu
ッパ ppa
ッペ ppe
ッピ ppi
ッポ ppo
ップ ppu
ッキャ
ッキョ
ッキュ
ッチャ at
ッチョ
ッチュ
ッシャ as
ッショ
ッシュ shi
ッピャ
ッピョ
ッピュ er
イェ ye
ウェ we
ウィ wi
ウォ wo
ヴァ va
ヴェ ve
ヴィ vi
ヴォ vo
ヴ vu
シェ she
ジェ je
チェ che
ティ ti
トゥ tu
ディ th
ドゥ nd
ツァ tsa
ツェ tse
ツィ tsi
ツォ tso
ファ fa
フェ fe
フィ fi
フォ fo
ヴャ ea
ヴョ ou
ヴュ is
テュ nt
デュ ed
フュ of
ッシェ es
ッティ et
ットゥ ld
ッツァ al
ッツェ en
ッツィ it
ッツォ st
ッテゥ le
Ａ A
Ｂ B
Ｃ C
Ｄ D
Ｅ E
Ｆ F
Ｇ G
Ｈ H
Ｉ I
Ｊ J
Ｋ K
Ｌ L
Ｍ M
Ｎ N
Ｏ O
Ｐ P
Ｑ Q
Ｒ R
Ｓ S
Ｔ T
Ｕ U
Ｖ V
Ｗ W
Ｘ X
Ｙ Y
Ｚ Z
ａ a
ｂ b
ｃ c
ｄ d
ｅ e
ｆ f
ｇ g
ｈ h
ｉ i
ｊ j
ｋ k
ｌ l
ｍ m
ｎ n
ｏ o
ｐ p
ｑ q
ｒ r
ｓ s
ｔ t
ｕ u
ｖ v
ｗ w
ｘ x
ｙ y
ｚ z
０ 0
１ 1
２ 2
３ 3
４ 4
５ 5
６ 6
７ 7
８ 8
９ 9
！ !
＠ @
＃ #
＄ $
％ %
＾ ^
＆ &
＊ *
「 [
、 ,
。 .
？ ?
ー -
〜 ~
； ;""".splitlines()))

mapping["　"] = " "
mapping["ニュ"] = "\n"

mapping["ア"] = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
mapping["エ"] = "abcdefghijklmnopqrstuvwxyz"
mapping["イ"] = ""
mapping["オ"] = "Hello, World!"
