# 伺服器後端

本來想做加入一個伺服器介面的, 不過發現Google要收錢, 自己架又太麻煩, 所以就做出這樣的東西

## 簡介

一次性完成一堆使用者的練習, 預計配合cron(或者systemd/timers)使用

## 使用說明

| 指令 | 說明 | 參數 |
|:----:|:----:|:----:|
| web\_main --help 或 web\_main -h | 內鍵的說明頁, 內容尚未完成 | *無* |
| web\_main main | 最主要的內容, 由登入到亂填答案一手包辦 | --sacrifice [ID], 指定亂填的使用者ID |
| web\_main add\_user | 增加使用者到data/web\_data | --id, --passwd, --school\_id, 後面接對應的數據, 如果沒有填上的話會問使用者 |

## 檔案
 - ~/.khh/web\_data -- 用戶的資料, 以json格式儲存
 - ~/.khh/log/web.log -- 紀錄檔
 - ~/.khh/yyyy/mm/dd -- 該天的答案, 未來可能會更改格式

## 需求
 - click(Command Line Interface Creation Kit)
