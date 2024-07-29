import os, sys, shutil

project_path = None

sub_dirs = ["figures"]

latex_res = ["xac.bib", "xac.sty"]

template_dir = "chi_template"

if __name__ == "__main__":
    if len(sys.argv) <= 1:
       print("Please specify project directory.")
       exit(1)

    project_path = sys.argv[1]

    if len(sys.argv) > 2:
        template_dir += "_" + sys.argv[2]
    
    # create the main dir and subdirs
    if not os.path.exists(project_path):
        os.makedirs(project_path)
    for sub_dir in sub_dirs:
        if not os.path.exists(project_path + "/" + sub_dir):
            os.makedirs(project_path + "/" + sub_dir)

    # copy the chi paper template
    shutil.copytree(template_dir, project_path, dirs_exist_ok=True)

    # copy some commonly used latex stuff
    for res in latex_res:
        shutil.copy(res, project_path)