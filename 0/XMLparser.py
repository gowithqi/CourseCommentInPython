import xsp
import sys 
import MySQLdb

reload(sys)

try:
	conn = MySQLdb.connect(host="localhost", port=3306, user="zzq", passwd="zzq_sjtu", db="CourseComment", charset="utf8")
except Exception, e:
	print e
	sys.exit()

cursor = conn.cursor()

def main() :
	XML_INFILE = sys.argv[1]
	
	PARSE_VOCABULARY = {
		'Detail': {
			'yxmc'    : str,
			'xm'      : str,
			'zcmc'    : str,
			'kcmc'    : str,
			'kcbm'    : str,
			'xqxs'    : str,
			'xqxf'    : str,
			'sjms'    : str,
			'nj'      : str,
			'xn'      : str,
			'xq'      : str,
			'yqdrs'   : str
		}
	}
	
	sys.setdefaultencoding('utf-8')
	res = xsp.parse(XML_INFILE, PARSE_VOCABULARY)
	
	count = 0
	for (key, values) in res.items():
		for value in values:
			count = count + 1
			if count%10 == 0 : print count
			# course
			# name, number, credit, school
			course = [value['kcmc'].strip(), value['kcbm'][17:22], float(value['xqxf']), value['yxmc'].strip()]
			s_sql = "select id from course where name=%s and number=%s"
			c = cursor.execute(s_sql, (course[0], course[1]))
			c_id = 0
			if (c != 0): c_id = cursor.fetchall()[0][0]
			else: 
				i_sql = "insert into course (name, number, credit, school) values(%s, %s, %s, %s)"
				if cursor.execute(i_sql, (course[0], course[1], course[2], course[3])) == 0L: print "insert Course failed!"
				conn.commit()
				c = cursor.execute(s_sql, (course[0], course[1]))
				c_id = cursor.fetchall()[0][0]

			# professor
			# name, title
			try:
				professor = [value['xm'].strip(), value['zcmc'].strip()]
			except KeyError:
				for i in course: print i
				print
				continue
			s_sql = "select id from professor where name=%s"
			p = cursor.execute(s_sql, (professor[0]))
			p_id = 0
			if (p != 0): p_id = cursor.fetchall()[0][0]
			else:
				i_sql = "insert into professor (name, title) values(%s, %s)"
				if cursor.execute(i_sql, (professor[0].encode("UTF-8"), professor[1])) == 0L: print "insert Professor failed"
				conn.commit()
				p = cursor.execute(s_sql, (professor[0]))
				try: 
					aa = cursor.fetchall()
					p_id = aa[0][0]
				except IndexError:
					print aa
					for i in course: print i
					for i in professor: print i
					print
					continue
			
			# lecture
			s_sql = "select * from lecture where course_id=%s and professor_id=%s"
			l = cursor.execute(s_sql, (c_id, p_id))
			if (l != 0):
				continue
				pass
			else:
				i_sql = "insert into lecture (course_id, professor_id) values(%s, %s)"
				cursor.execute(i_sql, (c_id, p_id))
				conn.commit()
			
	print count-1
	cursor.close()
	conn.close()

			

if __name__ == "__main__": main()
