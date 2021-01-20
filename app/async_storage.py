import asyncio
import motor.motor_asyncio
from quart import render_template_string, request, jsonify, Quart

from redis import Redis
from rq import Queue
from rq.decorators import job

from models import Search_query

from datetime import datetime

app = Quart(__name__)

SUCCESS = {
    "success": "success"
}

loop = asyncio.get_event_loop()

client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://localhost:27017')
db = client.textbase

async def add_query(data):
    await Search_query.q(db).create_indexes()
    q =  await Search_query(query=data['query'], engine=data['engine'], user_id=data['user_id'],
                            result=data['result'], date=datetime.now()).save(db)

async def find_querry(data):
    querries = [q async for q in Search_query.q(db).find(data)]
    return querries

async def show_all():
    querries = [q async for q in Search_query.q(db).find({})]
    return querries

@app.route('/')
async def all_list():
    q = await show_all()
    result = [query.to_json() for query in q]
    return  jsonify(result)

'''
Add query loop
'''
@app.route('/api/storage/add')
async def insert_query():
    await Search_query.q(db).create_indexes()
    data = await request.get_json(force=True)
    result = await add_query(data)
    return await render_template_string('{{data}}', data=SUCCESS)

'''
Loop with search queries
'''
@app.route('/api/storage/search', methods=['post', 'get'])
async def save_query():
    temp = []
    json_data = await request.get_json(force=True)
    await Search_query.q(db).create_indexes()
    q = await find_querry(data_modifier(json_data))
    result = [query.to_json() for query in q]

    return  jsonify(result)


def data_modifier(json_data):
    if 'user_id' in json_data and 'query' not in json_data:
        if 'engine' in json_data:
            data = {"user_id": json_data['user_id'], "engine": json_data['engine']}
        else: 
            data = {"user_id": json_data['user_id']}     
    elif 'query' in json_data and 'user_id' not in json_data:
        if 'engine' in json_data:
            data = {"query": json_data['user_id'], "engine": json_data['engine']} 
        else:
            data = {"query": json_data['query']} 
    elif 'user_id' in json_data and 'query' in json_data:
        if 'engine' in json_data:
            data = {"user_id": json_data['user_id'], "engine": json_data['engine'], "query": json_data['query']}             
        else:
            data = {"user_id": json_data['user_id'], "query": json_data['query']}
    return data

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True, loop=loop)
