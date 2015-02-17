vm:
	@if [ -z "`ansible-galaxy list | grep \"angstwad.docker_ubuntu\"`" ]; then ansible-galaxy install angstwad.docker_ubuntu; fi;
	@vagrant up
	@echo "Run: export DOCKER_HOST=\"tcp://`vagrant ssh-config | sed -n "s/[ ]*HostName[ ]*//gp"`:2375\""
