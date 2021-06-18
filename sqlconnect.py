import pymysql

def mysqlconnect(date_id,specialty):
	# To connect MySQL database
	conn = pymysql.connect(
		host='bpfsakhgvayk9oawkrtl-mysql.services.clever-cloud.com',
        user='uhc4dju2xkqp2shl',
        password='bXundo1ws1qmMyu1Yyhu',
		db='bpfsakhgvayk9oawkrtl',
        charset='utf8mb4',
		port=3306
		) 
	table=specialty
	cur = conn.cursor()
	cur.execute("SELECT id, name ,time"
	            " FROM %s " %table + 
				" WHERE date = %s AND Status='empty' ", (date_id))
	output = cur.fetchall()
	conn.close()    # To close the connection
	strn = []
	doc_avail = ''
	for i in output:
		strn1 = str(i[0]) + '\t-\t'+ i[1] + ' : ' + i[2]
		strn.append(strn1)
	for i in strn:
	    doc_avail = doc_avail + i + '\n'
	#print(doc_avail)
	return doc_avail

def name(id_num,specialty):
	conn = pymysql.connect(
		host='bpfsakhgvayk9oawkrtl-mysql.services.clever-cloud.com',
        user='uhc4dju2xkqp2shl',
        password='bXundo1ws1qmMyu1Yyhu',
		db='bpfsakhgvayk9oawkrtl',
        charset='utf8mb4',
		port=3306
		) 
	table=specialty
	cur = conn.cursor()
	print (id_num)
	cur.execute("SELECT Name "" FROM %s " %table + 
				"  WHERE id = %s",(id_num))
	
	output= cur.fetchall()
	for i in output:
         for j in i:
           n=j
	conn.close()  
	return n

def time(id_num,specialty):
	conn = pymysql.connect(
		host='bpfsakhgvayk9oawkrtl-mysql.services.clever-cloud.com',
        user='uhc4dju2xkqp2shl',
        password='bXundo1ws1qmMyu1Yyhu',
		db='bpfsakhgvayk9oawkrtl',
        charset='utf8mb4',
		port=3306
		) 
	table=specialty
	cur = conn.cursor()
	cur.execute("SELECT time " " FROM %s " %table + 
				"  WHERE id= %s",(id_num))
	output= cur.fetchall()
	for i in output:
         for j in i:
           t=j 
	conn.close() 
	return t
def book_appointment(id_num,specialty):
	conn = pymysql.connect(
		host='bpfsakhgvayk9oawkrtl-mysql.services.clever-cloud.com',
        user='uhc4dju2xkqp2shl',
        password='bXundo1ws1qmMyu1Yyhu',
		db='bpfsakhgvayk9oawkrtl',
        charset='utf8mb4',
		port=3306
		) 
	table=specialty
	cur = conn.cursor()
	sql = "UPDATE %s " %table + " SET Status = 'booked' WHERE id = %s"
	cur.execute(sql,(id_num))

	conn.commit()
	print(cur.rowcount, "record(s) affected")
	conn.close() 
	
def checkdate(specialty,date):
  conn = pymysql.connect(
		host='bpfsakhgvayk9oawkrtl-mysql.services.clever-cloud.com',
        user='uhc4dju2xkqp2shl',
        password='bXundo1ws1qmMyu1Yyhu',
		db='bpfsakhgvayk9oawkrtl',
        charset='utf8mb4',
		port=3306
		) 
  cur = conn.cursor()
  n=1
  #query=SELECT date FROM general WHERE date='2021-06-15'
  cur.execute("SELECT Date " "FROM %s " %specialty + 
				"  WHERE date= %s",(date))
  out = cur.fetchone()
  
  conn.close() 
  return out





# Driver Code
# if __name__ == "__main__" :
# 	mysqlconnect(date_id)

# host='localhost',
#         user='root',
#         password='manashri',
# 		db='pm_bot',
#         charset='utf8mb4'
