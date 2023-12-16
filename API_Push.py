import pyodbc
import sys
import time
import datetime
import requests
import json


conn = pyodbc.connect(
    "Driver={ODBC Driver 17 for SQL Server};"
    "Server=localhost;"
    "Database=Demo_Database_CICD;"
    "uid=giannis;"
    "pwd=giannis;"
    "autocommit=false"
)

cursor = conn.cursor()

api_url = ""
TimeStamp = datetime.datetime.now()

query = """
select 
Message_Count = isnull(sum(p.rows), 0),
Active_Reader_Count = isnull(sum(ar.current_readers),0)
from sys.service_queues as sq 
left join sys.objects as o 
on sq.object_id = o.object_id
left join sys.objects as o2 
on o2.parent_object_id = o.object_id
left join sys.partitions as p 
on p.object_id = o2.object_id
left join (select queue_id, count(*) current_readers from sys.dm_broker_activated_tasks
           group by queue_id
		   ) ar
on sq.object_id = ar.queue_id
where sq.is_ms_shipped = 0 and sq.Name like '%Target%'
"""

for x in range(0,1000000):
    result = cursor.execute(query)
    data = []

    for row in result:
        data.append(f"Message_Count:{row[0]}, Active_Reader_Count: {row[1]}, TimeStamp: {TimeStamp.isoformat()}")
        payload = json.dumps(data)
        print(f"Message_Count:{row[0]}, Active_Reader_Count: {row[1]}, TimeStamp: {TimeStamp.isoformat()}")

        time.sleep(.25)
        TimeStamp = datetime.datetime.now()


cursor.close()
conn.close()
