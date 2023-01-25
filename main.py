from venv import create
from bs4 import BeautifulSoup 
import shutil
import os

CREATE_JS_MIN = 'createjs.min.js'

def operation_1():
    for file in os.listdir(os.getcwd()):
        d = os.path.join(os.getcwd(), file)
        if os.path.isdir(d) and 'x' in d:
            # get current folder
            current_folder_arr = d.split(os.sep)
            current_folder = current_folder_arr[len(current_folder_arr) - 1]
            print("Start processing " + current_folder)
            copy_script_to_folder(current_folder)
            add_tags(current_folder)
            remove_fla(current_folder)
            copy_content_of_images_and_remove_folder(current_folder)
            zip_folder(current_folder)
            print("\n==================\n")
    

def add_tags(current_folder):
    try:
        os.chdir(current_folder)
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

            meta_tag_replacer = "meta_tag_replace"
            meta_tag_v2 = '<meta name="ad.size" content="width=$1,height=$2">'.replace("$1", str(width)).replace("$2", str(height))
            soup.head.title.insert_before(meta_tag_replacer)

            # inserting script click tag
            # <script> var clickTag = "https://company_link";</script> 
            # company_link = input("Please insert the company link: ")
            click_tag_script = soup.new_tag('script')
            click_tag_script.attrs['type'] = 'text/javascript'
            click_tag_script.append('var clickTag = "{ad_url}";')
            soup.head.title.insert_after(click_tag_script)

            # inserting script createjs.min.js
            # <script src="createjs.min.js"></script>
            createjs_script_tag = soup.new_tag('script')
            createjs_script_tag.attrs['src'] = CREATE_JS_MIN
            soup.head.title.insert_after(createjs_script_tag)

            # wrapping canvas with a
            # <a href="javascript:window.open(window.clickTag)"><canvas></canvas></a>
            a_wrapper_tag = soup.new_tag('a')
            a_wrapper_tag.attrs['href'] = 'javascript:window.open(window.clickTag)'
            soup.canvas.wrap(a_wrapper_tag)

            # removing cdn createjs.min.js 
            soup.find(attrs={"src": "https://code.createjs.com/1.0.0/createjs.min.js"}).decompose()

            
            with open(file_name, 'w') as f_w:
                content = soup.prettify().replace('images/','').replace(meta_tag_replacer, meta_tag_v2)
                f_w.write(content)
                print("\nTags added")

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


def copy_script_to_folder(current_folder):
    try:
        shutil.copy(CREATE_JS_MIN, current_folder + os.sep + CREATE_JS_MIN)
        print(CREATE_JS_MIN + " is successfully copied to " + current_folder)
    except Exception as ignored:
        print("Coping createjs.min.js failed")


def copy_content_of_images_and_remove_folder(current_folder):
    try:
        for file_name in os.listdir(current_folder + os.sep + "images"):
            shutil.move(os.path.join(os.getcwd(), current_folder, 'images', file_name), os.path.join(os.getcwd(), current_folder))
        
        print("All images moved to " + current_folder)

        os.rmdir(current_folder + os.sep + "images")

        print("Images folder deleted")
    except Exception as ignored:
        print("Coping content of images and removing images folder failed")


def zip_folder(current_folder):
    shutil.make_archive(current_folder, "zip", current_folder)
    print("Folder " + current_folder + " archived")
    

def main():
    print("1. Add meta tags and clean .fla file then zip")
    print("2. Coming soon... ")
    print("\n")
    # op = int(input("Select operation:"))
    op = 1
    print("Currently we have only one operation, becuase of that operation 1 selected by default")

    print("\n")
    if op == 1:
        operation_1()

    print("(c) Webperside / Hamid Sultanzadeh")


if __name__ == '__main__':
    main()