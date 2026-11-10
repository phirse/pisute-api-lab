# API lab results

## Part 0
- Step 0.1, the number of pizza names: 18
  - รัน `curl.exe https://quickpizza.grafana.com/api/names` ใน PowerShell (ต้องพิมพ์ `curl.exe` เพราะ `curl` ใน PowerShell เป็นคนละคำสั่ง) ได้ JSON object ที่มี field เดียวคือ `names` เป็น list ของชื่อพิซซ่า 18 ชื่อ ตั้งแต่ "Americana" ถึง "Siciliana"
  - Step 0.2: เพิ่ม `-i` แล้ว status line เป็น `HTTP/1.1 200 OK` ไม่ใช่ HTTP/2 แบบในชีท เพราะ curl.exe ที่มากับ Windows ไม่มี feature HTTP2 (ดูได้จาก `curl.exe -V`) ใน headers มี `Content-Type: application/json` และ `Set-Cookie: AWSALB=...` กับ `AWSALBCORS=...` ซึ่งหมดอายุในอีก 7 วัน (Expires=Tue, 17 Nov 2026) ต่อจากบรรทัดว่างเป็น body JSON เดียวกับ Step 0.1
- Step 0.3, status code of the request without a token:
- Step 0.4, the name of your pizza:
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
