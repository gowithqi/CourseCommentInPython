from BeautifulSoup import BeautifulSoup
import sys

i = 0

def parse(soup, c):
	global i
	courses_html = soup.findAll("tr", {"class": ["tdcolour1", "tdcolour2"]})
	for c_html in courses_html[4:]:
		cc = c_html.findChildren("td")
		i += 1
		print cc[1].string, cc[2].string
	return

def main():
	print sys.argv
	f = open(sys.argv[1])
	file_content = f.read()
	soup = BeautifulSoup(file_content)
	
	parse(soup, "tdcolour1")
	#parse(soup, "tdcolour2")
	print i
	return

if __name__ == "__main__":
	main()

	
