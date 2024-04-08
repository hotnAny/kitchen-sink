import os, sys, shutil

project_path = "./nsf_project"

sub_dirs = ["paper_work", "others", "sandbox"]

latex_res = ["xac.bib", "xac.sty", "split.py", "gitignore"]

template_dir = "nsf_template"

if __name__ == "__main__":
    if len(sys.argv) <= 1:
       print("Please specify proposal directory.")
       exit(1)

    project_path = sys.argv[1]

    if len(sys.argv) > 2:
        template_dir += "_" + sys.argv[2]
    
    # create the main dir and subdirs
    os.makedirs(project_path)
    for sub_dir in sub_dirs:
        os.makedirs(project_path + "/" + sub_dir)

    # copy the nsf proposal template
    shutil.copytree(template_dir, project_path + "/proposal")

    # copy some commonly used latex stuff
    for res in latex_res:
        shutil.copy(res, project_path + "/proposal")
    # deal with gitignore
    shutil.move(project_path + "/proposal/gitignore", project_path + "/proposal/.gitignore")