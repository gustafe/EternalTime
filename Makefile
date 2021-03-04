HOME=/home/gustaf
BIN=$(HOME)/prj/EternalTime
TEMPLATES=$(BIN)/templates
CGI=$(HOME)/cgi-bin

deploy: eternal.cgi $(TEMPLATES)/*.tt
	cp $(BIN)/eternal.cgi $(CGI)/eternal.cgi
	cp $(TEMPLATES)/*.tt $(CGI)/templates

.PHONY: test
test: 
	perl -Tc $(BIN)/eternal.cgi          > test

deploy-test:
	curl -s http://gerikson.com/cgi-bin/eternal.cgi | lynx -stdin -dump >> test

about.html: about.md $(TEMPLATES)/about.tt
	perl $(BIN)/generate-docs.pl

