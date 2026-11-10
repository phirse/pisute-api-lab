# pisute-api-lab

API testing ของ QuickPizza (https://quickpizza.grafana.com) ด้วย pytest และ requests

## วิธีติดตั้งและรัน

```powershell
py -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
pytest -v
pytest -v --html=report.html --self-contained-html
```

ผลที่ควรได้คือ `32 passed, 1 xfailed` ตัวที่ xfail คือ Defect 1 (ดูใน RESULTS.md) รันทั้งชุดส่ง request 140 ครั้ง ใช้เวลาประมาณ 50 วินาที test ที่ต้องใช้ user จะสร้าง user ใหม่ของตัวเอง จึงไม่ขึ้นกับ test อื่น

## Input domain model ของ POST /api/ratings

| Characteristic | Block | Value ที่ใช้ | Test ที่ครอบคลุม |
|---|---|---|---|
| C1 Value of `stars` | below 1 | 0 | `test_stars_out_of_range[0]` |
| | 1 to 5 (base) | 3 | `test_base_choice_is_saved` |
| | above 5 | 6 | `test_stars_out_of_range[6]` |
| C2 Type of `stars` | whole number (base) | 3 | `test_base_choice_is_saved` |
| | decimal | 3.5 | `test_decimal_stars_are_refused` |
| | text | "3" | `test_text_stars_are_refused` |
| | missing | no field | `test_missing_stars_are_refused` |
| C3 Pizza | exists (base) | a new pizza | `test_base_choice_is_saved` |
| | does not exist | 999999999 | `test_unknown_pizza_is_refused` |
| C4 Token | the user's own (base) | from `auth` | `test_base_choice_is_saved` |
| | none | no header | `test_rating_without_token_is_refused` |
| | wrong length | `token short` | `test_rating_with_short_token_is_refused` |

Base choice coverage ใช้ 1 + 2 + 3 + 1 + 2 = 9 tests (ถ้าเป็น all combinations ต้องใช้ 3 × 4 × 2 × 3 = 72 tests)
