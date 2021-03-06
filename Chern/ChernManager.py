"""
This is the top class for project manager
"""
import os
from subprocess import call, PIPE
from Chern import utils
# from Chern.VAlgorithm import VAlgorithm
# from Chern.VTask import VTask
# from Chern.VData import VData
# from Chern.VDirectory import VDirectory
# from Chern.VProject import VProject

class ChernManager(object):
    """ ChernManager class
    """
    instance = None
    c = None

    @classmethod
    def get_manager(cls):
        """ Return the manager itself
        """
        if cls.instance is None:
            cls.instance = ChernManager()
        return cls.instance

    def __init__(self):
        self.init_global_config()

    def root_object(self):
        """ Get the root object
        """
        pass

    def current_object(self):
        """ Get the current object
        """
        # os.get_current_directory()
        # return create_object_instance()
        pass

    def init_global_config(self):
        chern_config_path = os.environ.get("CHERNCONFIGPATH")
        if chern_config_path is None:
            raise Exception("CHERNCONFIGPATH is not set")
        self.global_config_path = utils.strip_path_string(chern_config_path) + "/config.py"

    def get_current_project(self):
        """ Get the name of the current working project.
        If there isn't a working project, return None
        """
        global_config_file = utils.ConfigFile(self.global_config_path)
        current_project = global_config_file.read_variable("current_project")
        return current_project

    def get_all_projects(self):
        """ Get the list of all the projects.
        If there is not a list create one.
        """
        global_config_file = utils.ConfigFile(self.global_config_path)
        projects_path = global_config_file.read_variable("projects_path")
        return projects_path.keys()

    def ls_projects(self):
        """
        ls projects
        """
        projects_list = self.get_all_projects()
        for project_name in projects_list:
            print(project_name)

    def get_project_path(self, project_name):
        """ Get The path of a specific project.
        You must be sure that the project exists.
        This function don't check it.
        """
        global_config_file = utils.ConfigFile(self.global_config_path)
        projects_path = global_config_file.read_variable("projects_path")
        return projects_path[project_name]


    def switch_project(self, project_name):
        """ Switch the current project

        """
        global_config_file = utils.ConfigFile(self.global_config_path)
        global_config_file.write_variable("current_project", project_name)
        # global global_vproject
        # del global_vproject
        # global_vproject = VProject()


    def new_project(self, project_name):
        """ Create a new project
        """
        project_name = utils.strip_path_string(project_name)
        print("The project name is ", project_name)

        # Check the forbidden name
        forbidden_names = ["config", "new", "projects", "start"]
        def check_project_failed(project_name, forbidden_names):
            message = "The following project names are forbidden:"
            message += "\n    "
            for name in forbidden_names:
                message += name + ", "
            raise Exception(message)
        if project_name in forbidden_names:
            check_project_failed(project_name, forbidden_names)

        ncpus = int(input("Please input the number of cpus to use for this project: "))
        user_name = input("Please input your name:")
        user_mail = input("Please input your email:")

        pwd = os.getcwd()
        project_path = pwd + "/" + project_name
        if not os.path.exists(project_path):
            os.mkdir(project_path)
        else:
            raise Exception("Project exist")
        config_file = utils.ConfigFile(project_path+"/.config.py")
        config_file.write_variable("object_type", "project")
        config_file.write_variable("ncpus", ncpus)
        config_file.write_variable("user_name", user_name)
        config_file.write_variable("user_mail", user_mail)
        with open(project_path + ".README.md", "w") as f:
            f.write("Please write README for this project")
        call("vim %s/.README.md"%project_path, shell=True)
        global_config_file = utils.ConfigFile(self.global_config_path)
        projects_path = global_config_file.read_variable("projects_path")
        if projects_path is None:
            projects_path = {}
        projects_path[project_name] = project_path
        global_config_file.write_variable("projects_path", projects_path)
        global_config_file.write_variable("current_project", project_name)
        print(project_path)
        os.chdir(project_path)
        call("git init", shell=True, stdout=PIPE, stderr=PIPE)
        call("git add .config.py", shell=True, stdout=PIPE, stderr=PIPE)
        call("git commit -m \" Create config file for the project\"", shell=True, stdout=PIPE, stderr=PIPE)
        call("git add .README.md", shell=True, stdout=PIPE, stderr=PIPE)
        call("git commit -m \" Create README file for the project\"", shell=True, stdout=PIPE, stderr=PIPE)

        # global global_vproject
        # global_vproject = VProject(pwd+"/"+project_name, None)

        """
        def update_configuration():
            if not os.path.exists(global_config_path):
                shutil.copyfile(os.environ["CHENSYSPATH"]+"/config/global_config.py", os.environ["HOME"])

        This is something not used currently
        def main(command_list):
            #current_project = get_current_project()
            #projects_list = get_all_projects()

            if len(command_list) == 0 :
                # print "Current project is:", get_current_project()
                # print "All the projects are:",
                for obj in get_all_projects():
                    pass
                    # print obj,
                return

            if command_list[0] == "config":
                update_configuration()
                from subprocess import call
                call("vim " + get_project_path(get_current_project()) + "/.config/config.py", shell = True)
                return

            if not command_list[0] in get_all_projects():
                print("No such a project ", command_list[0], " try to create a new one.")
                #try:
                new_project(command_list[0])
                #except Exception as e:
                #    print e

            if command_list[0] in get_all_projects():
                switch_project(command_list[0])
                print("Switch to project", command_list[0])
                return "cd " + get_project_path(command_list[0]) + "\n"

            #except :
            #    print "Can not config new project for some reason"
        """

def get_manager():
    return ChernManager.get_manager()
