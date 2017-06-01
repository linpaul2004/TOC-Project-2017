# YuGiOh Bot on Telegram

遊戲王卡片查詢機器人

基於 Finite State Machine 的 Telegram bot

**必須使用Linux運行**

## 安裝

### 必備環境
* Python 3

#### 安裝套件
```sh
pip install -r requirements.txt
```

* pygraphviz (用來畫 Finite State Machine)
    * [Setup pygraphviz on Ubuntu](http://www.jianshu.com/p/a3da7ecc5303)

### Bot 資訊

請**務必**要把 app.py 中的 `API_TOKEN` (line 10 in app.py) 與 `WEBHOOK_URL` (line 11 in app.py) 改成正確的值

* `API_TOKEN` 是 Bot 的 token ， 請在 Telegram 跟 BotFather 取得
* `WEBHOOK_URL` 是伺服器的網址，請**務必**使用 https 網址

### 本地端運行
可以選擇自己架設 https 伺服器或使用 `ngrok` 來代理

**在以下的說明中預設使用 `ngrok`**

```sh
ngrok http 5000
```

之後， `ngrok` 會產生一個 https 的網址

將 `WEBHOOK_URL` (app.py 中) 設為 `your-https-URL/hook`.

#### 執行伺服器

```sh
python3 app.py
```

## Finite State Machine
![fsm](./img/show-fsm.png)

## 用法
一開始的state設在 `initial`

功能：

1. 找中文卡片→輸入卡號
2. 找日文卡片→輸入日文卡名
3. 查卡圖→/image
4. 找推薦牌組→/deck
5. 用法→/help
6. 最新禁卡表→/limit

----------

* byNum
	* 輸入卡號
	* Input:`55144522` 
	* 《強欲之壺》
	* 通常魔法
	* 我方抽2張牌。
* byName
	* 輸入日文卡名
	* Input:`死者蘇生`
	* 《死者蘇生》
	* 通常魔法（制限カード）
	* (1)：自分または相手の墓地のモンスター１体を対象として発動できる。
そのモンスターを自分フィールドに特殊召喚する。
* deck
	* Input:`/deck`
	* 要組特定牌組→輸入關鍵字
	* 推薦主流牌組→/recommend
		* Input:`封印`
		* 找全部牌組→/all
		* 找比賽牌組→/race
		* 找非比賽牌組→/norace
* help
	* Input:`/help`
	* 顯示使用說明
* limit
	* Input:`/limit`
	* 回覆最新版禁卡表
* image
	* Input:`/image`
	* 請輸入卡號
		* Input:`83764718`
		* ![image](http://cdn.asia.xpg.cards/card-image/ST17/JP022/fd5781eb-64e4-41c4-ab88-bc1a374fd4e0200X282.jpg?v=1)

## 作者
[林偉哲](https://github.com/linpaul2004)
