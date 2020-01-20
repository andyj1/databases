import sqlalchemy

# root@localhost:3306
engine = sqlalchemy.create_engine('mysql+pymysql://user@localhost:3306/sailors')
connection = engine.connect()

# use existing database sailor
engine.execute("use sailors")

i = 1
def run_query(engine, query_statement):
    global i
    print("Query", i)
    i = i + 1
    qr = engine.execute(query_statement)
    qr.keys()
    for row in qr:
        print(row)

qstmts = []

# query statements
qs1 = 'select distinct b.bid, s.sname, count(*) as rank from boats b join reserves r on b.bid = r.bid join sailors s on s.sid = r.sid group by b.bid, b.bname, s.sid, s.sname having count(*) >= all (select count(*) from reserves r0 where  r0.bid = b.bid group by r0.sid) order by b.bid, s.sname;'
qs2 = 'select distinct reserves.bid,count(reserves.bid) as num_res, boats.bname from reserves join boats on boats.bid=reserves.bid group by reserves.bid'
qs3 = ''
qs4 = 'select distinct s.sid,s.sname from sailors s where \'red\'=all( select b.color from reserves r join boats b on r.bid=b.bid where r.sid=s.sid) and s.sid in (select sid from reserves)'
qs5 = 'select r.bid,b.bname, count(*) rank from reserves r join boats b on r.bid=b.bid group by b.bid order by rank desc limit 1'
qs6 = ''
qs7 = 'select avg(age) from sailors where rating=10'
qs8 = 'select s.sid, s.sname, r.day from sailors s join reserves r on s.sid = r.sid'

# qstmts.append(qs1)
# qstmts.append(qs2)
# qstmts.append(qs4)
# qstmts.append(qs5)
# qstmts.append(qs7)
qstmts.append(qs8)

try:
    for qs in qstmts:
        run_query(engine, qs)
finally:
    connection.close()
