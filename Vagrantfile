# -*- mode: ruby -*-
# https://atlas.hashicorp.com/parallels/boxes/boot2docker

Vagrant.require_version ">= 1.6.3"

Vagrant.configure("2") do |config|
  config.vm.define "boot2docker"

  config.vm.box = "parallels/boot2docker"
  config.vm.box_check_update = false

  config.vm.network "private_network", type: "dhcp"
  config.vm.network :forwarded_port, host: 27017, guest: 27017

  config.vm.provision :shell do |s|
    s.inline = <<-EOT
      if ! grep -qs ^nameserver /etc/resolv.conf; then
        sudo /sbin/udhcpc
      fi
      cat /etc/resolv.conf
    EOT
  end

  config.vm.provision :shell do |s|
    s.inline = <<-EOT
      sudo /usr/local/bin/ntpclient -s -h pool.ntp.org
      date
    EOT
  end

  config.vm.provision :docker do |d|
    d.run "mongo",
      image: "mongo",
      args: "-p 27017:27017"
  end
end
