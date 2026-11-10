# api-lab

## Input domain model ของ POST /api/ratings

`POST /api/ratings` รับ body ที่มี 2 fields คือ `pizza_id` กับ `stars` และรับ token ทาง header QuickPizza ยอมรับ stars ที่เป็นจำนวนเต็ม 1 ถึง 5, pizza ที่มีอยู่จริง และ token ของ user ที่ login แล้ว จึงแบ่ง input ออกเป็น 4 characteristics ตามตารางนี้

| Characteristic | Blocks | Values in the tests |
|---|---|---|
| C1 Value of `stars` | below 1, 1 to 5 (base), above 5 | 0, 3, 6 |
| C2 Type of `stars` | whole number (base), decimal, text, missing | 3, 3.5, "3", no field |
| C3 Pizza | exists (base), does not exist | a new pizza, 999999999 |
| C4 Token | the user's own (base), none, wrong length | from `auth`, no header, `token short` |

### Block และ test ที่ครอบคลุม

ทุก test อยู่ใน `test_create_rating.py` แต่ละ test เปลี่ยน characteristic ทีละตัวจาก base แล้วคงตัวอื่นไว้ที่ base คือ 3 stars แบบจำนวนเต็ม, pizza ใหม่จาก fixture `pizza_id` และ token ของ user เองจาก fixture `auth`

| Characteristic | Block | Value | ผลที่ API ตอบ | Test ที่ครอบคลุม |
|---|---|---|---|---|
| C1 Value of `stars` | below 1 | 0 | 400 `number of stars must be between 1 and 5 (inclusive)` | `test_stars_out_of_range[0]` |
| | 1 to 5 (base) | 3 | 201 ได้ rating ใหม่ | `test_base_choice_is_saved` |
| | above 5 | 6 | 400 `number of stars must be between 1 and 5 (inclusive)` | `test_stars_out_of_range[6]` |
| C2 Type of `stars` | whole number (base) | 3 | 201 | `test_base_choice_is_saved` |
| | decimal | 3.5 | 400 `json: cannot unmarshal number 3.5 into Go struct field Rating.stars of type int` | `test_decimal_stars_are_refused` |
| | text | "3" | 400 `json: cannot unmarshal string into Go struct field Rating.stars of type int` | `test_text_stars_are_refused` |
| | missing | no field | 400 `number of stars must be between 1 and 5 (inclusive)` | `test_missing_stars_are_refused` |
| C3 Pizza | exists (base) | a new pizza | 201 | `test_base_choice_is_saved` |
| | does not exist | 999999999 | 400 `pizza ID 999999999 not found` | `test_unknown_pizza_is_refused` |
| C4 Token | the user's own (base) | from `auth` | 201 | `test_base_choice_is_saved` |
| | none | no header | 401 `authentication failed` | `test_rating_without_token_is_refused` |
| | wrong length | `token short` | 401 `authentication failed` | `test_rating_with_short_token_is_refused` |

base choice coverage ใช้ 1 + 2 + 3 + 1 + 2 = 9 tests คือ base test 1 ตัว บวกจำนวน block ที่ไม่ใช่ base ของ C1, C2, C3 และ C4 ตรงกับ 9 tests ใน `test_create_rating.py` ถ้าทำ all combinations coverage จะต้องใช้ 3 × 4 × 2 × 3 = 72 tests

error message ทุกตัวหาด้วย curl ก่อนเขียน test โดย body ที่ใช้อยู่ในไฟล์ `user.json` และ `rating-*.json` รายละเอียดอยู่ใน RESULTS.md

## Boundary values ของการแก้ rating

`PUT /api/ratings/{id}` รับ stars 1 ถึง 5 จึงทดสอบค่าทั้งสองฝั่งของขอบทั้งสองด้าน ใน `test_update_rating.py::test_update_stars_at_the_boundaries` ซึ่ง parametrize เป็นคู่ของ stars กับ status ที่คาด ทุกรอบเริ่มจาก rating 3 stars ของ fixture `rating` และอ่าน rating กลับมาหลังแก้ทุกครั้ง เพราะการแก้ที่ถูกปฏิเสธต้องไม่ทำให้ rating เปลี่ยน

| stars | status ที่คาด | stars ที่อ่านกลับมา |
|---|---|---|
| 0 | 400 `number of stars must be between 1 and 5 (inclusive)` | 3 (ไม่เปลี่ยน) |
| 1 | 200 | 1 |
| 5 | 200 | 5 |
| 6 | 400 `number of stars must be between 1 and 5 (inclusive)` | 3 (ไม่เปลี่ยน) |

## ใครแก้ rating ได้บ้าง

`test_rating_owner.py` ใช้ fixture `auth` เป็นเจ้าของ rating และ `other_auth` เป็น user อีกคน (ทั้งคู่สร้างจาก `log_in_new_user` ใน conftest.py) แต่ละ test ให้ user อีกคนลองอ่าน แก้ หรือลบ rating ของเจ้าของ แล้วเช็คว่าโดนปฏิเสธด้วย status 400–499 จากนั้นให้เจ้าของอ่าน rating อีกครั้งเพื่อดูว่าไม่มีอะไรเปลี่ยน

| Test | สิ่งที่ user อีกคนทำ | status ที่ได้ |
|---|---|---|
| `test_other_user_cannot_read_rating` | GET `/api/ratings/{id}` | 404 |
| `test_other_user_cannot_change_rating` | PUT `/api/ratings/{id}` ด้วย `{"stars": 5}` | 400 |
| `test_other_user_cannot_delete_rating` | DELETE `/api/ratings/{id}` | 400 |
