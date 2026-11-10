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
- Step 0.12, results of the three runs without a session (optional): fail ทั้ง 3 รอบ (ผ่าน 0 จาก 3)
  - Step 0.9: ลองทำใน Python shell ด้วย `requests.Session()` ได้ชื่อ user ใหม่ `'lab-d2187b2cd309'` สร้าง user ได้ `(201, {'id': 259, 'username': 'lab-d2187b2cd309'})` login แล้วได้ token ยาว 16 ตัว อ่าน ratings ด้วย token ของตัวเองได้ `(200, {'ratings': []})` และ `s.cookies.keys()` ได้ `['AWSALB', 'AWSALBCORS']` คือ cookie ของ load balancer ที่ session เก็บไว้ส่งกลับไปทุก request
  - Step 0.12: รัน `pytest -v test_no_session.py` 3 รอบ ทุกรอบสร้าง user ผ่าน (201) แต่ login ได้ 401 แทน 200 (`E assert 401 == 200`) เพราะ `requests.post` แต่ละครั้งไม่ได้ส่ง cookie AWSALB กลับไป load balancer จึงส่ง login ไปที่ server ตัวอื่นซึ่งไม่มี user นี้ ผลไปทางเดียวกับในชีทที่ login fail 46 จาก 49 ครั้ง test นี้จะผ่านก็ต่อเมื่อบังเอิญได้ server ตัวเดิมทั้งสอง request ผลจึงขึ้นกับดวงทั้งที่โค้ดไม่เปลี่ยน ซึ่งก็คือ flaky test หลังบันทึกผลแล้วจึงลบ test_no_session.py ออก
- Step 0.16, blocks of "how many of the three tools are excluded": มี 4 blocks คือ 0 tools, 1 tool, 2 tools และ 3 tools (exclude ครบทุกอย่าง)
  - test ในชีทใช้ `["Knife"]` กับ `["Scissors"]` ซึ่งอยู่ใน block เดียวกันคือ 1 tool จึงเพิ่ม input ให้ block ที่ยังไม่มี block ละหนึ่งตัว คือ `[]` (0 tools), `["Knife", "Pizza cutter"]` (2 tools) และ `["Knife", "Pizza cutter", "Scissors"]` (3 tools) แล้วใส่ `ids` ให้ชื่อ test บอก block เช่น `test_excluded_tool_is_not_used[2-tools]`
  - block 0, 1 และ 2 tools ผ่านหมด (พิซซ่าไม่ใช้ tool ที่ exclude) แต่ block 3 tools fail ด้วย `assert 500 == 200`
  - ยืนยันด้วย `curl.exe -i -H "@auth.txt" -d "@all-tools.json" https://quickpizza.grafana.com/api/pizza` (all-tools.json คือ `{"excludedTools": ["Knife", "Pizza cutter", "Scissors"]}`) ได้ `HTTP/1.1 500 Internal Server Error` กับ `Content-Length: 0` ไม่มี header Content-Type และ body ว่างเปล่า
  - ย้าย input 3 tools ออกจาก parametrize ไปเป็น test ของตัวเองชื่อ `test_all_tools_excluded_is_refused` ที่คาดว่าได้ 400 และ JSON error message ตามที่ product owner กำหนด test นี้ fail ด้วย `assert 500 == 400` จึง mark ด้วย `@pytest.mark.xfail(reason="Defect 1: ...", strict=True)` หลังจากนั้น `pytest -v` ได้ `16 passed, 1 xfailed`

## Defect report
- Title: Defect 1: POST /api/pizza ตอบ 500 Internal Server Error และ body ว่าง เมื่อ exclude tools ครบทั้ง 3 อย่าง
- Request: `POST https://quickpizza.grafana.com/api/pizza` ส่ง header `Authorization: token <token>` และ body `{"excludedTools": ["Knife", "Pizza cutter", "Scissors"]}` (ไฟล์ all-tools.json) ทดสอบเมื่อ 10 Nov 2026
  - curl: `curl.exe -i -H "@auth.txt" -d "@all-tools.json" https://quickpizza.grafana.com/api/pizza`
  - pytest: `test_excluded_tools.py::test_all_tools_excluded_is_refused` ใช้ token ของ user ที่สร้างและ login เอง ได้ผลเหมือนกัน
- Expected result: `400 Bad Request` พร้อม JSON error message ในรูปแบบเดียวกับ error อื่นของ API เช่น `{"error": "..."}` ที่บอกว่าไม่มีพิซซ่าที่ตรงเงื่อนไข เพราะ product owner กำหนดว่า request ที่ไม่มีพิซซ่าไหนตอบได้ต้องได้ 400 และ JSON error message ห้ามเป็น 500
- Actual result: `500 Internal Server Error`, `Content-Length: 0`, ไม่มี Content-Type และ body ว่าง เรียก `res.json()` ใน Python จึง error เพราะไม่มี JSON ให้ parse ส่วน block 0, 1 และ 2 tools ได้ 200 ตามปกติ และเกิดซ้ำได้ทุกครั้งที่ส่ง request นี้
  - ดูจาก source ของ QuickPizza (`pkg/http/http.go` ใน github.com/grafana/quickpizza) server สุ่ม tool ด้วย `validTools[rand.Intn(len(validTools))]` เมื่อ exclude ครบทุกอย่าง list นี้ว่าง `rand.Intn(0)` จึง panic แล้ว middleware ที่ดัก panic ตอบ 500 แบบไม่มี body แสดงว่า server ไม่ได้ตรวจ input นี้ก่อนเลย
- Severity: Major เพราะเป็น input ที่ client ส่งได้ตามปกติผ่าน field `excludedTools` แต่ server กลับพังด้วย 500 แทนที่จะปฏิเสธ input ทำให้ client แยกไม่ออกว่า request ผิดหรือ server ล่ม และไม่มี message ไปบอกผู้ใช้ ซึ่งขัดกับ requirement ของ product owner ตรง ๆ ที่ไม่ถึงขั้น Critical เพราะ server ยังทำงานต่อได้ ไม่มีข้อมูลเสียหาย และเกิดเฉพาะตอน exclude ครบทุก tool

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
