from fastapi import FastAPI, UploadFile, Form,Response
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.staticfiles import StaticFiles
from typing import Annotated
import sqlite3

con = sqlite3.connect('db.db', check_same_thread=False)
cur = con.cursor()

# 배포된 서버에서 따로 데이터를 만들 테이블을 만들어줘야한다.
# 백엔드 코드에서 자동으로 테이블을 생성할 수 있도록 SQL문을 작성했다.
# 작성해주면 백엔드 코드가 실행될때 테이블을 만든다.
# 단 단 CREATE TABLE items로 만들게 되면 db에 테이블이 이미 존재한다고 뜬다(배포된경우에도)
# 방지하기 위해 테이블이 없을때만 CREATE될 수 있도록
# 조건문 테이블이 없을 때만 생성하는 SQL문 => IF NOT EXISTS items 추가
# cur.execute(f"""
#             CREATE TABLE items (
#                 id INTEGER PRIMARY KEY,
#                 title TEXT NOT NULL,
#                 image BLOB,
#                 price INTEGER NOT NULL,
#                 description TEXT,
#                 place TEXT NOT NULL,
#                 insertAt INTEGER NOT NULL
#             );
#             """)

app = FastAPI()

@app.post("/items")
async def create_item(image:UploadFile,
                title:Annotated[str,Form()],
                price:Annotated[int,Form()],
                description:Annotated[str,Form()],
                place:Annotated[str,Form()],
                insertAt:Annotated[int,Form()]
                ):
    image_bytes = await image.read()
    cur.execute(f"""
                INSERT INTO items(title,image,price,description,place,insertAt)
                VALUES ('{title}','{image_bytes.hex()}',{price},'{description}','{place}',{insertAt})
                """) 
    con.commit()
    return '200'



@app.get('/items')
async def get_items():
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    rows = cur.execute(f"""
                       SELECT * from items;
                       """).fetchall()
    return JSONResponse(jsonable_encoder(dict(row) for row in rows))


@app.get('/images/{item_id}')
async def get_image(item_id):
    cur = con.cursor()
    image_bytes = cur.execute(f"""
                              SELECT image from items WHERE id={item_id}
                              """).fetchone()[0]
    return Response(content=bytes.fromhex(image_bytes), media_type='image/*')


app.mount("/", StaticFiles(directory="frontend", html=True),name="frontend")
