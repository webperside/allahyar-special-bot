from bs4 import BeautifulSoup 
import shutil
import os

def operation_1():
    for file in os.listdir(os.getcwd()):
        d = os.path.join(os.getcwd(), file)
        if os.path.isdir(d):
            # get current folder
            current_folder_arr = d.split(os.sep)
            current_folder = current_folder_arr[len(current_folder_arr) - 1]
            add_tag(current_folder)
            remove_fla(current_folder)
            zip_folder(current_folder)
            print("\n==================\n")
    

def add_tag(current_folder):
    try:
        os.chdir(current_folder)
        print("Start processing " + current_folder)

        file_name = current_folder+'.html'

        # reading html file
        with open(file_name, 'r+') as f:

            contents = f.read()

            soup = BeautifulSoup(contents, 'html.parser')

            height = soup.canvas["height"]
            width = soup.canvas["width"]

            # inserting meta tag
            # <meta name="ad.size" content="width=300,height=250">
            meta_tag = soup.new_tag('meta')
            meta_tag.attrs['name'] = 'ad.size'
            meta_tag.attrs['content'] = 'width='+width+",height="+height
            soup.head.title.insert_before(meta_tag)
            
            with open(file_name, 'w') as f_w:
                f_w.write(soup.prettify())
                print("Tag added")

    except Exception as e:
        print("Failed " + current_folder + " (description : " + str(e) + ")")
    
    os.chdir("..")


def remove_fla(current_folder):
    os.chdir(current_folder)
    fla_file_name = current_folder+'.fla'
    try:
        os.remove(fla_file_name)
        print(".fla file deleted")
    except Exception as ignored:
        print(fla_file_name + " already deleted (or missed)")

    os.chdir("..")


def zip_folder(current_folder):
    
    shutil.make_archive(current_folder, "zip", current_folder)
    print("Folder " + current_folder + " archived")
    

def main():
    print("1. Add meta tags and clean .fla file then zip")
    print("2. Coming soon... ")
    print("\n")
    op = int(input("Select operation:"))

    print("\n")
    if op == 1:
        operation_1()

    print("(c) Webperside / Hamid Sultanzadeh")


if __name__ == '__main__':
    main()