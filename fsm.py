import urllib.request
import re
import random
from transitions.extensions import GraphMachine
import telegram


class TocMachine(GraphMachine):
    keyword = ""

    def __init__(self, **machine_configs):
        self.machine = GraphMachine(
            model=self,
            **machine_configs
        )

    def is_going_to_byNum(self, update):
        text = update.message.text
        if text[0] == "/":
            return False
        elif text.isdigit():
            num = int(text, 10)
            if num <= 99999999:
                return True
        return False

    def is_going_to_byName(self, update):
        text = update.message.text
        if text[0] == "/":
            return False
        elif text.isdigit():
            num = int(text, 10)
            if num <= 99999999:
                return False
        return True

    def is_going_to_deck(self, update):
        text = update.message.text
        if "/deck" in text:
            return True
        else:
            return False

    def is_going_to_deckwhich(self, update):
        text = update.message.text
        if "/recommend" in text:
            return False
        else:
            return True

    def is_going_to_deckrecommend(self, update):
        text = update.message.text
        if "/recommend" in text:
            return True
        else:
            return False

    def is_going_to_deckall(self, update):
        text = update.message.text
        if "/all" in text:
            return True
        else:
            return False

    def is_going_to_deckrace(self, update):
        text = update.message.text
        if "/race" in text:
            return True
        else:
            return False

    def is_going_to_decknorace(self, update):
        text = update.message.text
        if "/norace" in text:
            return True
        else:
            return False

    def is_going_to_help(self, update):
        text = update.message.text
        if "/help" in text or "/start" in text:
            return True
        else:
            return False

    def is_going_to_limit(self, update):
        text = update.message.text
        if "/limit" in text:
            return True
        else:
            return False

    def is_going_to_image(self, update):
        text = update.message.text
        if "/image" in text:
            return True
        else:
            return False

    def is_going_to_imageresult(self, update):
        text = update.message.text
        if text.isdigit() and int(text) <= 99999999:
            return True
        else:
            update.message.reply_text("錯誤卡號")
            self.go_back_initial(update)
            return False

    def on_enter_byNum(self, update):
        text = update.message.text
        urequest = urllib.request.urlopen(
            "https://asia.xpg.cards/card/" + text)
        content = urequest.read().decode('utf8', errors="ignore")
        urequest.close()
        name = re.search('name="og:title" content="(.*?)"', content)
        effect = re.search(
            'name="og:description" content="(.*?)"', content, re.DOTALL)
        kind = re.search('"kind":"(.*?)"', content)
        level = re.search('"level":"(.*?)"', content)
        prop = re.search('"property":"(.*?)"', content)
        race = re.search('"race":"(.*?)"', content)
        attack = re.search('"attack":([0-9?]+)', content)
        defence = re.search('"defence":([0-9?]+)', content)
        if name is None or effect is None:
            update.message.reply_text("找不到卡片")
        else:
            button = [[telegram.InlineKeyboardButton(
                "看此卡詳細", "https://asia.xpg.cards/card/" + text)]]
            bm = telegram.InlineKeyboardMarkup(button)
            if level is None or level.group(1) == "":
                update.message.reply_text("《{0}》\n{1}\n{2}".format(name.group(1), kind.group(
                    1), effect.group(1)), parse_mode="Markdown", reply_markup=bm)
            else:
                update.message.reply_text("《{0}》\n{1}\n{2}/{3}屬/{4}/ATK{5}/DEF{6}\n{7}".format(name.group(1), kind.group(
                    1), level.group(1), prop.group(1), race.group(1), attack.group(1), defence.group(1), effect.group(1)), parse_mode="Markdown", reply_markup=bm)
        self.go_back_initial(update)

    def on_enter_deckwhich(self, update):
        TocMachine.keyword = update.message.text
        update.message.reply_text("找全部牌組→/all\n找比賽牌組→/race\n找非比賽牌組→/norace")

    def on_exit_byNum(self, update):
        print('Leaving byNum')

    def on_enter_byName(self, update):
        text = update.message.text
        text = TocMachine.strtofull(self, text)
        text = "《" + text + "》"
        name = text
        try:
            text = urllib.parse.quote(text.encode('euc-jp'))
        except:
            update.message.reply_text("輸入文字的編碼轉換有誤")
            self.go_back_initial(update)
            return
        urequest = urllib.request.urlopen(
            "http://yugioh-wiki.net/index.php?" + text)
        content = urequest.read().decode('euc-jp', errors="ignore")
        urequest.close()
        effect = re.search('<pre>(.*?)</pre>', content, re.DOTALL)
        if effect is None:
            update.message.reply_text("找不到卡片")
        else:
            button = [[telegram.InlineKeyboardButton(
                "看此卡詳細", "http://yugioh-wiki.net/index.php?" + text)]]
            bm = telegram.InlineKeyboardMarkup(button)
            update.message.reply_text("{0}\n{1}".format(
                name, effect.group(1)), parse_mode="Markdown", reply_markup=bm)
        self.go_back_initial(update)

    def on_exit_byName(self, update):
        print('Leaving byName')

    def on_enter_deck(self, update):
        update.message.reply_text("要組特定牌組→輸入關鍵字\n推薦主流牌組→/recommend")

    def on_enter_deckrecommend(self, update):
        urequest = urllib.request.urlopen(
            "https://ocg.xpg.jp/deck/deck.fcgi?Sort=3")
        content = urequest.read().decode('shift-jis', errors="ignore")
        urequest.close()
        match = re.findall(
            '<a href="(deck\.fcgi\?ListNo=[0-9]+)">(.*?)</a>', content)
        no = random.randint(0, 20)
        url = "https://ocg.xpg.jp/deck/" + match[no][0]
        name = match[no][1]
        urequest = urllib.request.urlopen(url)
        content = urequest.read().decode('shift-jis', errors="ignore")
        urequest.close()
        match = re.findall(
            '<td>([1-3])</td><td>[制|準]?</td><td><a href="/c/[0-9]+/">(<table class="lm2">(<tr>(<td( class="s")?></td>){3}</tr>){3}</table>)?(.*?)</a>', content)
        text = "「" + name + "」\n"
        for (x, _, _, _, _, y) in match:
            text += x
            text += "x"
            text += y
            text += "\n"
        update.message.reply_text(text)
        self.go_back_initial(update)

    def on_enter_deckall(self, update):
        try:
            TocMachine.keyword = urllib.parse.quote(
                TocMachine.keyword.encode('shift-jis'))
        except:
            update.message.reply_text("輸入文字的編碼轉換有誤")
            self.go_back_initial(update)
            return
        try:
            urequest = urllib.request.urlopen(
                "https://ocg.xpg.jp/ds/?Title=" + TocMachine.keyword + "&Sort=3")
        except:
            update.message.reply_text("找不到相關牌組")
            self.go_back_initial(update)
            return
        content = urequest.read().decode('shift-jis', errors="ignore")
        urequest.close()
        match = re.findall(
            '<a href="(/deck/deck\.fcgi\?ListNo=[0-9]+)">(.*?)</a>', content)
        if len(match) == 0:
            update.message.reply_text("找不到相關牌組")
            self.go_back_initial(update)
            return
        no = random.randint(0, len(match) - 1)
        url = "https://ocg.xpg.jp" + match[no][0]
        name = match[no][1]
        urequest = urllib.request.urlopen(url)
        content = urequest.read().decode('shift-jis', errors="ignore")
        urequest.close()
        match = re.findall(
            '<td>([1-3])</td><td>[制|準]?</td><td><a href="/c/[0-9]+/">(<table class="lm2">(<tr>(<td( class="s")?></td>){3}</tr>){3}</table>)?(.*?)</a>', content)
        text = "「" + name + "」\n"
        for (x, _, _, _, _, y) in match:
            text += x
            text += "x"
            text += y
            text += "\n"
        update.message.reply_text(text)
        self.go_back_initial(update)

    def on_enter_deckrace(self, update):
        try:
            TocMachine.keyword = urllib.parse.quote(
                TocMachine.keyword.encode('shift-jis'))
        except:
            update.message.reply_text("輸入文字的編碼轉換有誤")
            self.go_back_initial(update)
            return
        try:
            urequest = urllib.request.urlopen(
                "https://ocg.xpg.jp/ds/?Title=" + TocMachine.keyword + "&Sort=3&Flt=1")
        except:
            update.message.reply_text("找不到相關牌組")
            self.go_back_initial(update)
            return
        content = urequest.read().decode('shift-jis', errors="ignore")
        urequest.close()
        match = re.findall(
            '<a href="(/deck/deck\.fcgi\?ListNo=[0-9]+)">(.*?)</a>', content)
        if len(match) == 0:
            update.message.reply_text("找不到相關牌組")
            self.go_back_initial(update)
            return
        no = random.randint(0, len(match) - 1)
        url = "https://ocg.xpg.jp" + match[no][0]
        name = match[no][1]
        urequest = urllib.request.urlopen(url)
        content = urequest.read().decode('shift-jis', errors="ignore")
        urequest.close()
        match = re.findall(
            '<td>([1-3])</td><td>[制|準]?</td><td><a href="/c/[0-9]+/">(<table class="lm2">(<tr>(<td( class="s")?></td>){3}</tr>){3}</table>)?(.*?)</a>', content)
        text = "「" + name + "」\n"
        for (x, _, _, _, _, y) in match:
            text += x
            text += "x"
            text += y
            text += "\n"
        update.message.reply_text(text)
        self.go_back_initial(update)

    def on_enter_decknorace(self, update):
        try:
            TocMachine.keyword = urllib.parse.quote(
                TocMachine.keyword.encode('shift-jis'))
        except:
            update.message.reply_text("輸入文字的編碼轉換有誤")
            self.go_back_initial(update)
            return
        try:
            urequest = urllib.request.urlopen(
                "https://ocg.xpg.jp/ds/?Title=" + TocMachine.keyword + "&Sort=3&Flt=2")
        except:
            update.message.reply_text("找不到相關牌組")
            self.go_back_initial(update)
            return
        content = urequest.read().decode('shift-jis', errors="ignore")
        urequest.close()
        match = re.findall(
            '<a href="(/deck/deck\.fcgi\?ListNo=[0-9]+)">(.*?)</a>', content)
        if len(match) == 0:
            update.message.reply_text("找不到相關牌組")
            self.go_back_initial(update)
            return
        no = random.randint(0, len(match) - 1)
        url = "https://ocg.xpg.jp" + match[no][0]
        name = match[no][1]
        urequest = urllib.request.urlopen(url)
        content = urequest.read().decode('shift-jis', errors="ignore")
        urequest.close()
        match = re.findall(
            '<td>([1-3])</td><td>[制|準]?</td><td><a href="/c/[0-9]+/">(<table class="lm2">(<tr>(<td( class="s")?></td>){3}</tr>){3}</table>)?(.*?)</a>', content)
        text = "「" + name + "」\n"
        for (x, _, _, _, _, y) in match:
            text += x
            text += "x"
            text += y
            text += "\n"
        update.message.reply_text(text)
        self.go_back_initial(update)

    def on_enter_help(self, update):
        update.message.reply_text(
            "我是遊戲王卡片機器人\n找中文卡片→輸入卡號\n找日文卡片→輸入日文卡名\n查卡圖→/image\n找推薦牌組→/deck\n用法→/help\n最新禁卡表→/limit")
        self.go_back_initial(update)

    def on_enter_limit(self, update):
        urequest = urllib.request.urlopen(
            "http://yugioh-wiki.net/index.php?%A5%EA%A5%DF%A5%C3%A5%C8%A5%EC%A5%AE%A5%E5%A5%EC%A1%BC%A5%B7%A5%E7%A5%F3")
        content = urequest.read().decode('euc-jp', errors="ignore")
        urequest.close()
        match = re.findall(
            '<li><a href=".*?" title=".*?">(.*?)</a></li>|(<hr class="full_hr" />|<div class="jumpmenu">)', content)
        cn = 0
        text = ""
        for (name, control) in match:
            if control == '<hr class="full_hr" />' or control == '<div class="jumpmenu">':
                cn += 1
            if cn == 3:
                text += "-----禁止卡-----\n"
                cn += 1
            elif cn == 4 or cn == 6 or cn == 8:
                text += "{0}\n".format(name)
            elif cn == 5:
                text += "\n-----限制卡-----\n"
                cn += 1
            elif cn == 7:
                text += "\n-----準限制卡-----\n"
                cn += 1
            elif cn > 8:
                break
        # print(text)
        update.message.reply_text(text, parse_mode="Markdown")
        self.go_back_initial(update)

    def on_enter_image(self, update):
        update.message.reply_text("請輸入卡號")

    def on_enter_imageresult(self, update):
        text = update.message.text
        urequest = urllib.request.urlopen(
            "https://asia.xpg.cards/card/" + text)
        content = urequest.read().decode('utf8', errors="ignore")
        urequest.close()
        url = re.search('<img src="(.*?)"', content)
        if url is None:
            update.message.reply_text("找不到卡片")
        else:
            update.message.reply_photo(url.group(1))
        self.go_back_initial(update)

    def strtofull(self, ustring):
        rstring = ""
        for uchar in ustring:
            c = ord(uchar)
            if c == 0xb7:
                rstring += chr(0x30fb)
            elif c < 0x20 or c > 0x7e:
                rstring += uchar
            elif c == 0x20:
                rstring += uchar
            elif c == 0x2e:
                rstring += uchar
            else:
                rstring += chr(c + 0xfee0)
        return rstring
