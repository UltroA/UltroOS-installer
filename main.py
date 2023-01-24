import archinstall
import getpass
import os


class Installer:
    def __init__(self):
        self.boot = ''
        self.root = ''
        self.harddrive = ''

    def diskwork(self):
        # Select a harddrive and a disk password
        os.system("lsblk")
        diskn = input('Enter disk name in format: "sdX or nvmeXnY" (where X and Y is nums): ')
        self.harddrive = archinstall.select_disk(archinstall.select_disk(diskn))

        # We disable safety precautions in the library that protects the partitions
        self.harddrive.keep_partitions = False

        # First, we configure the basic filesystem layout
        with archinstall.Filesystem(self.harddrive, archinstall.GPT) as fs:
            # We create a filesystem layout that will use the entire drive
            # (this is a helper function, you can partition manually as well)
            fs.use_entire_disk(root_filesystem_type='btrfs')

            self.boot = fs.find_partition('/boot')
            self.root = fs.find_partition('/')

            self.boot.format('vfat')

            self.boot.mount('/mnt/boot')

    def install_needed_and_mount(self):
        with archinstall.Installer('/mnt') as installation:
            if installation.minimal_installation(hostname='UltroOS'):
                installation.add_bootloader()

                installation.add_additional_packages(['vim', 'wget', 'git'])

                # Optionally, install a profile of choice.
                # In this case, we install a minimal profile that is empty
                installation.install_profile('gnome')

                user = User('devel', 'devel', False)
                installation.create_users(user)
                installation.user_set_pw('root', 'airoot')


if __name__ == '__main__':
    inst = Installer()
    inst.diskwork()
    inst.install_needed_and_mount()
