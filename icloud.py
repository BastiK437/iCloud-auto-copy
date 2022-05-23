import os
import shutil
import threading
from time import sleep

user_name = os.getlogin()

path_to_photos = "C:\\Users\\" + user_name + "\\Pictures"
icloud_dir_name = "iCloud Photos\\Photos"
icloud_copy_dir = "iCloud Offline"
thread_amount = 5

def task(src, dst):
    print("\nThread started \nCopy from '" + src + "' to '" + dst + "'")
    while True:
        try:
            shutil.copyfile(src, dst)
            break
        except OSError:
            print("OSError: src [" + src + "], dst [" + dst + "] - Trying again")

def rem_dirs(list, path):
    for element in list:
        if os.path.isdir(path + "\\" + element):
            list.remove(element)

def get_element_diff(elements_src, elements_dest):
    diff_list = []
    for element in elements_src:
        if not element in elements_dest:
            diff_list.append(element)
    
    return diff_list

def main():
    if not os.path.isdir(path_to_photos):
        print("Path to photos directory incorrect")
        exit()

    icloud_path = path_to_photos + "\\" + icloud_dir_name
    if not os.path.isdir(icloud_path):
        print("Path to icloud directory incorrect")
        exit()

    icloud_copy_path = path_to_photos + "\\" + icloud_copy_dir
    if not os.path.isdir(icloud_copy_path):
        os.mkdir(icloud_copy_path)

    online_list = os.listdir(icloud_path)
    rem_dirs(online_list, icloud_path)

    offline_list = os.listdir(icloud_copy_path)
    rem_dirs(offline_list, icloud_copy_path)

    print("Calculate diff")
    diff_list = get_element_diff(online_list, offline_list)

    threads = []
    progress = 0
    amount_to_copy = str(len(diff_list))

    for element in diff_list:
        src = icloud_path + "\\" + element
        dst = icloud_copy_path + "\\" + element
        
        amount = 0
        while len(threads) >= thread_amount:
            if amount > 0:
                sleep(0.3)
            for elem in threads:
                if not elem.is_alive():
                    threads.remove(elem)
                    break
            amount = 1

        threads.append(threading.Thread(target=task, args=(src,dst)))
        threads[len(threads)-1].start()

        progress = progress + 1
        print(str(progress) + "/" + amount_to_copy)
        



if __name__=="__main__":
	main()