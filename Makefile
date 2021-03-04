HOME=/home/gustaf
BIN=$(HOME)/prj/EternalTime

CGI=$(HOME)/cgi-bin

deploy: eternal.cgi
	cp $(BIN)/eternal.cgi $(CGI)/eternal.cgi

.PHONY: test
test: 
	perl -Tc $(BIN)/eternal.cgi          > test

deploy-test:
	curl -s http://gerikson.com/cgi-bin/eternal.cgi | lynx -stdin -dump >> test

about.html: about.md about.tt
	perl $(BIN)/generate-docs.pl

