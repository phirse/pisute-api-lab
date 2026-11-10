# API lab results

## Part 0
- Step 0.1, the number of pizza names: 18
  - รัน `curl.exe https://quickpizza.grafana.com/api/names` ใน PowerShell (ต้องพิมพ์ `curl.exe` เพราะ `curl` ใน PowerShell เป็นคนละคำสั่ง) ได้ JSON object ที่มี field เดียวคือ `names` เป็น list ของชื่อพิซซ่า 18 ชื่อ ตั้งแต่ "Americana" ถึง "Siciliana"
  - Step 0.2: เพิ่ม `-i` แล้ว status line เป็น `HTTP/1.1 200 OK` ไม่ใช่ HTTP/2 แบบในชีท เพราะ curl.exe ที่มากับ Windows ไม่มี feature HTTP2 (ดูได้จาก `curl.exe -V`) ใน headers มี `Content-Type: application/json` และ `Set-Cookie: AWSALB=...` กับ `AWSALBCORS=...` ซึ่งหมดอายุในอีก 7 วัน (Expires=Tue, 17 Nov 2026) ต่อจากบรรทัดว่างเป็น body JSON เดียวกับ Step 0.1
- Step 0.3, status code of the request without a token: 401 (Unauthorized)
  - `curl.exe -i https://quickpizza.grafana.com/api/tools` ได้ `HTTP/1.1 401 Unauthorized` และ body `{"error":"authentication failed"}` เพราะ request ไม่มี header Authorization
  - ส่งใหม่ด้วย `curl.exe -H "@auth.txt" https://quickpizza.grafana.com/api/tools` (auth.txt มีบรรทัดเดียวคือ `Authorization: token abcdef0123456789`) ได้ `{"tools":["Knife","Pizza cutter","Scissors"]}`
- Step 0.4, the name of your pizza: The Hard Margherita
  - `curl.exe -H "@auth.txt" -d "@veg.json" https://quickpizza.grafana.com/api/pizza` ได้ pizza id 5910 แป้ง Thin ตัดด้วย Knife ingredients 6 อย่างคือ Olive oil, Roma tomatoes, Mozzarella, Green peppers, Broccoli และ Mushrooms ทุกตัวมี `"vegetarian":true` และ response มี `"vegetarian":true` กับ `"calories":400`
  - Step 0.5: ลองส่ง request ชุดเดิมจาก Python shell ด้วย requests ได้ `res.status_code` = 200, `res.headers["Content-Type"]` = `'application/json'`, `type(res.json())` เป็น `dict`, ชื่อแรกคือ `'Americana'` ส่วน `/api/tools` ที่ส่ง `headers=auth` ได้ 200 กับ tools 3 อย่าง และ POST `/api/pizza` ด้วย `json={"mustBeVegetarian": True}` ได้ 200 แต่รอบนี้ได้พิซซ่าชื่อ `'A Fluffy Napoletana'` ไม่ใช่ชื่อเดิม เพราะ QuickPizza สุ่มพิซซ่าใหม่ทุกครั้ง
- Step 0.12, results of the three runs without a session (optional):
- Step 0.16, blocks of "how many of the three tools are excluded":

## Defect report
- Title:
- Request:
- Expected result:
- Actual result:
- Severity:

## Part A
- Step A4, status codes when the other user reads, changes and deletes:

## Part B
1.
2.
3.
4.
5.
6.
7.
8.
