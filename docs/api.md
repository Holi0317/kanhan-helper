# API 說明

這是看漢中文網與python互動的模塊, 以及整個程式的模心模塊

## 主要物件
 - kanhan\_api

## 主要功能
| 功能名稱 | 功能 | 傳入的資料 | 回傳 |
|:----:|:----:|:----:|:----:|
| login | 登入 | 登入名稱, 密碼, 學校ID | 成功與否(Bool) |
| get\_id | 取得練習的id | 日期, 預設為今天 | id |
| is\_exercise\_done | 取得練習的token, 以及是否完成 | 練習id, 預設為今天的 | 是否已經完成(Bool) |
| take\_exercise | 做練習 | 答案(list), id(string) | 成功與否(Bool) |

## Todo
 - [ ] 改以request寫成網絡模塊
 - [ ] 整理代碼, 令其更簡單
