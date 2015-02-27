# Chinese Kan-han helper

## 簡介
一個"輔助工具", 優化使用者做看漢中文網的體驗

## 功能介紹
 - 以Python3寫成
 - 可以作答看漢中文網的題目
 - 以一個api作為base寫成, 其他開發者理論上可以容易開發自己的一套軟件
 - 可分析和取得答案, 以及利用取得的答案作答

## 模組
 - module\_api -- 這套軟件的核心, 令python與看漢中文網可以作出互動
 - cli\_main -- Command Line Interface
 - gui\_main -- Graphic User Interface, *已放棄*
 - web\_main -- 批次完成練習的後端, 事實上與網頁完全沒有關係

## Todo
 - [x] 完成cli的作業
 - [x] 製作/放棄gui
 - [x] 製作setup.py, 並加入dependency
 - [x] 整理目錄
 - [ ] 拍一段安裝教學影片

## 說明頁
大部份的模塊也有寫上簡單的說明. 而 docs/ 裏也有一些說明. 最新和詳細的說明都以模塊裏的為準.

## 安裝
以下為Windows版的安裝方式. 理論上可行, 但未被測試
1. 到[python.org](https://www.python.org/downloads/)下載Python **3** 必需為3而不是2
2. 用git clone 下整個repo. 或者直接接右邊的Download zip
3. 執行 `setup.py install` , 此為安裝程式
4. 在Termial (cmd/powerline) 中輸入 `khh-server` 執行伺服器,`khh-cli` 執行文字介面

以下為GNU/Linux的安裝方式, 應該也能套用在Mac OS X上
(雖然我不認為使用這些系統的人需要指導)
1. 用package manager安裝 `python3 git`. 如 `yaourt -Syy python3 git`. 不同的distro用不同的package manager是常識吧
2. `git clone [此repo的網址]`
3. `sudo ./setup.py install` 如果沒有root權限, 可使用virtualenv取代
4. 執行`khh-server` 執行伺服器, `khh-cli` 為CLI
