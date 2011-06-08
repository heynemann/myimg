help:
	@echo "Available Targets:"
	@cat Makefile | egrep '^(\w+?):' | sed 's/:\(.*\)//g' | sed 's/^/- /g'

requirements:
	@sudo aptitude install -y `cat aptitude-requirements.txt`
	@pip install -r pip-requirements.txt

test:
	@env PYTHONPATH=.:$$PYTHONPATH pyvows --cover --cover_package syncr tests/

mongodb:
	@mkdir -p /tmp/mongodb/myimg
	@mongod --cpu --dbpath /tmp/mongodb/myimg --port 20000 --bind_ip 0.0.0.0 -rest --journal
