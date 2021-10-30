from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.sql.expression import false, true
from starlette.middleware.cors import CORSMiddleware

from database import engine

from db.schema import ConditionRecord

app = FastAPI()

# Dependency

origins = [
    "http://localhost:3000",
    "localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/get_record", tags=["records"])
async def get_record(page: int, limit: int):
    with engine.connect() as con:
        print(con)
        rs = con.execute('SELECT * FROM records desc ')
        rowcount = con.execute("select count(*) from records desc ")
        total = rowcount.fetchone()[0]
        print(page)
        print(limit)
        print(total)
        records = []
        i = -1
        for row in rs:
            i = i + 1
            print(i)
            print((page - 1) * limit)
            print(page * limit - 1)
            if i < (page - 1) * limit:
                continue
            elif i > page * limit - 1:
                break
            else:

                records.append(row)

        rs.close()

    return {
        "data": records,
        "paging": {
            "total": total,
            "page": page,
            "limit": limit
        }
    }


@app.post(
    "/set_condition", tags=["conditions"]
)
async def set_condition(con: ConditionRecord):
    _engine = create_engine("sqlite:///./sql_app.db")
    _conn = engine.connect()
    try:
        _conn.execute("INSERT INTO condition (key, price, vol) VALUES (:key, :price, :vol)", key=con.key,
                      price=con.price, vol=con.vol)
        rs = _conn.execute('SELECT * FROM condition ORDER BY id DESC LIMIT 1')
        print(rs)
        return {"success": 1}
    except:
        return {"success": 0}


@app.get("/get_condition", tags=["conditions"])
async def get_condition():
    with engine.connect() as con:
        rs = con.execute('SELECT * FROM condition ORDER BY id DESC LIMIT 1')
        list = []
        for row in rs:
            list.append(row)
        rs.close()
    return list
