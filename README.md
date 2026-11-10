# api-lab

## Input domain model ของ POST /api/ratings

`POST /api/ratings` รับ body ที่มี 2 fields คือ `pizza_id` กับ `stars` และรับ token ทาง header QuickPizza ยอมรับ stars ที่เป็นจำนวนเต็ม 1 ถึง 5, pizza ที่มีอยู่จริง และ token ของ user ที่ login แล้ว จึงแบ่ง input ออกเป็น 4 characteristics ตามตารางนี้

| Characteristic | Blocks | Values in the tests |
|---|---|---|
| C1 Value of `stars` | below 1, 1 to 5 (base), above 5 | 0, 3, 6 |
| C2 Type of `stars` | whole number (base), decimal, text, missing | 3, 3.5, "3", no field |
| C3 Pizza | exists (base), does not exist | a new pizza, 999999999 |
| C4 Token | the user's own (base), none, wrong length | from `auth`, no header, `token short` |
