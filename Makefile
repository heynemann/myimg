help:
	@echo "Available Targets:"
	@cat Makefile | egrep '^(\w+?):' | sed 's/:\(.*\)//g' | sed 's/^/- /g'

test:
	@env PYTHONPATH=.:$$PYTHONPATH pyvows tests/

mongodb:
	@mkdir -p /tmp/mongodb/myimg
	@mongod --cpu --dbpath /tmp/mongodb/myimg --port 20000 --bind_ip 0.0.0.0 -rest --journal
