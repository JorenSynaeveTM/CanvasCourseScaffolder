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
    api_key = input("Geef de Canvas API key (laat leeg voor environment variable te gebruiken): ")
    if api_key == "":
        api_key = os.environ.get("CANVAS_API_KEY")
    canvas = Canvas("https://thomasmore.instructure.com/", api_key)

    configure_syllabus = yes_no.ask_yes_no_question("Would you like to configure the syllabus?")
    configure_studyguide = yes_no.ask_yes_no_question("Would you like to configure the study guide?")
    configure_course_image = yes_no.ask_yes_no_question("Would you like to configure the course image?")
    configure_pages = yes_no.ask_yes_no_question("Would you like to configure the pages?")
    configure_assignments = yes_no.ask_yes_no_question("Would you like to configure the assignments?")
    configure_quizzes = yes_no.ask_yes_no_question("Would you like to configure the quizzes?")
    configure_modules = yes_no.ask_yes_no_question("Would you like to configure the modules?")

    studiewijzer_module_id = None
    course = canvas.get_course(info.course_id)
    scaffolder = Scaffolder(course, path_to_config_folder)
    if configure_course_image:
        scaffolder.scaffold_course_image(info.course_image)
    if configure_pages:
        scaffolder.scaffold_pages(pages)
    if configure_studyguide:
        studiewijzer_module_id = scaffolder.scaffold_studiewijzer(info)
    if configure_syllabus:
        scaffolder.scaffold_syllabus(studiewijzer_module_id, info)
    if configure_assignments or configure_quizzes:
        scaffolder.scaffold_assignment_groups(assignment_groups)
    if configure_assignments:
        assignments = scaffolder.scaffold_assignments(assignments, assignment_groups)
    if configure_quizzes:
        quizzes = scaffolder.scaffold_quizzes(quizzes, assignment_groups)
    if configure_modules:
        scaffolder.scaffold_modules(
            modules,
            assignments if configure_assignments else None,
            quizzes if configure_quizzes else None
        )
