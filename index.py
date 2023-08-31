from canvasapi import Canvas
import os

from src.scaffolder import Scaffolder
from src.config_reader import ConfigReader
from src.helpers import yes_no

# Main program
if __name__ == "__main__":
    # Ask the user for the config file
    path_to_config_folder = input(
        "Geef het pad naar de map met de excel configuratie file (config.xlsx): ")

    # Check the config
    config_reader = ConfigReader(path_to_config_folder)
    info, assignment_groups, assignments, quizzes, modules, pages = config_reader.check_config()

    # Ask the user for a canvas api key, if not set as environment variable
    api_key = None
    if "CANVAS_API_KEY" in os.environ:
        api_key = os.environ["CANVAS_API_KEY"]
    else:
        api_key = input("Geef de Canvas API key: ")
    canvas = Canvas("https://thomasmore.instructure.com/", api_key)

    configure_assignments = yes_no.ask_yes_no_question("Would you like to configure the assignments?")
    configure_quizzes = yes_no.ask_yes_no_question("Would you like to configure the quizzes?")
    configure_modules = yes_no.ask_yes_no_question("Would you like to configure the modules?")

    course = canvas.get_course(info.course_id)
    scaffolder = Scaffolder(course, path_to_config_folder)
    scaffolder.scaffold_course_image(info.course_image)
    scaffolder.scaffold_pages(pages)
    studiewijzer_module_id = scaffolder.scaffold_studiewijzer(info)
    scaffolder.scaffold_syllabus(studiewijzer_module_id, info)
    if configure_assignments or configure_quizzes:
        scaffolder.scaffold_assignment_groups(assignment_groups)
    if configure_assignments:
        assignments = scaffolder.scaffold_assignments(assignments, assignment_groups)
    if configure_quizzes:
        quizzes = scaffolder.scaffold_quizzes(quizzes, assignment_groups)
    if configure_modules:
        scaffolder.scaffold_modules(modules, assignments, quizzes)
