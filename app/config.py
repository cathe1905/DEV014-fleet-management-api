from sqlalchemy import create_engine

engine = create_engine("postgresql://default:eprUF8OXcj7J@ep-shy-field-a4a1qo5z.us-east-1.aws.neon.tech:5432/verceldb?sslmode=require")
conn = engine.connect()
query = 'SELECT * from taxis'
result = conn.exec_driver_sql(query)

for row in result:
    print(row)
