
Vagrant.configure("2") do |config|

	#base box
	#config.vm.box = "hashicorp/precise64"
	config.vm.box = "debian/jessie64"

	#backup url
	# config.vm.box_url = "http://files.vagrantup.com/precise32.box"

    #set name
	config.vm.define :Smartifier_Box do |t|
	end

    #exec scripts
    config.vm.provision "shell", path: "vagrant.sh"


end

