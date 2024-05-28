from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from db_conn import connect_to_database
import uvicorn

app = FastAPI()


class Item(BaseModel):
    name:str
    address:str

conn = connect_to_database()


# Route to create an item
@app.post("/items/", response_model=Item)
def create_item(item: Item):
    cursor = conn.cursor()
    query = "INSERT INTO std_details (name, address) VALUES (%s, %s)"
    cursor.execute(query, (item.name, item.address))
    conn.commit()
    cursor.close()
    return item


@app.put("/itemsupda/{item_id}")
def update_item(item_id: int, new_address: Item):

    cursor = conn.cursor()
    query = "UPDATE std_details SET name=%s, address = %s WHERE id = %s"
    cursor.execute(query, (new_address.name,new_address.address, item_id))
    cursor.execute("SELECT name FROM std_details WHERE id=%s",(item_id,))
    updated_name=cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    return {"name":updated_name}




@app.get("/items/{name}", response_model=list[Item])
def read_items(name:str):
    cursor = conn.cursor()
    query = "SELECT name,address,age FROM std_details WHERE name=%s"
    cursor.execute(query,(name,))
    items = cursor.fetchall()
    cursor.close()
    result=[]
    for item in items:
        result.append({
            "name": item[0],
            "address":item[1],
            "age":item[2]
            })
    
    return result

@app.get("/items/", response_model=dict)
def read_item_name():
    cursor = conn.cursor()
    query = "SELECT name FROM std_details WHERE name = %s"
    cursor.execute(query,)
    item = cursor.fetchone()
    cursor.close()

    if item:
        return {"name": item[0]}
    else:
        {"msg":"Dorkledu"}

@app.get('/address')
def get_name():
    cursor=conn.cursor()
    query="SELECT name FROM std_details WHERE address='vzm' "
    cursor.execute(query)
    item=cursor.fetchall()
    return item

@app.post('/addcol')
def add_col():
    cursor=conn.cursor()
    query="ALTER TABLE std_details ADD age INT"
    cursor.execute(query)
    return {"age":"Column added"}

class Item1(BaseModel):
    age:int
@app.put('/age/{id}')
def add_age(id: int, data: Item1):
    cursor = conn.cursor()
    query = "UPDATE std_details SET age=%s WHERE id=%s"
    cursor.execute(query, (data.age, id))
    print(cursor)
    conn.commit()
    cursor.close()
    return {"result": f"Added age '{data.age}' to item with ID '{id}' successfully"}


@app.delete('/del/{id}')
def del_col(id:int):
    cursor=conn.cursor()
    query="DELETE FROM std_details WHERE id=%s"
    cursor.execute(query,(id,))
    conn.commit()
    cursor.close()
    return { "result":f"deleted item '{id}' successfully"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)