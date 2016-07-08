
Vagrant.configure("2") do |config|

	#base box
	config.vm.box = "debian/jessie64"

    #set name and RAM
	config.vm.provider "virtualbox" do |v|
		v.name = "Smartifier_Box"
		v.memory = 1536
	end

    #run vagrant.sh as user
    config.vm.provision "shell", path: "vagrant.sh", privileged: false

end

