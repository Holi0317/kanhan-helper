# API 說明

這是看漢中文網與python互動的模塊, 以及整個程式的模心模塊

## 主要物件
 - kanhan\_api

## 主要功能
| 功能名稱 | 功能 | 傳入的資料 | 回傳 |
|:----:|:----:|:----:|:----:|
| login | 登入 | 登入名稱, 密碼, 學校ID | 成功與否(Bool) |
| get\_id | 取得練習的id | 日期, 預設為今天, 以datetime.date為格式 | id, 沒有的話會回傳None |
| is\_exercise\_done | 取得練習的token, 以及是否完成. take\_exercise會自動呼叫, 盡量不要呼叫這功能 | 練習id, 預設為今天的 | Token和form build id. 沒有就會回傳0 |
| take\_exercise | 做練習 | 答案(list), id(string), wrong(int) | 成功與否(Bool) |
| get\_answers | 取得已完成練習的答案 | id(string) | 答案, 沒有就會回傳None |

## Todo
 - [ ] 改以request寫成網絡模塊
 - [ ] 加入python 2 支援性
 - [ ] 整理代碼, 令其更簡單(永遠不會完成)
