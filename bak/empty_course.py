from canvasapi import Canvas
import os

from src.helpers import yes_no

# Main program
if __name__ == "__main__":
    # Ask the user for the Canvas course id
    course_id = input("Geef de id van de Canvas cursus: ")
    # Ask the user for a canvas api key, if not set as environment variable
    api_key = input("Geef de Canvas API key (laat leeg voor environment variable te gebruiken): ")
    if api_key == "":
        api_key = os.environ.get("CANVAS_API_KEY")

    canvas = Canvas("https://thomasmore.instructure.com/", api_key)
    course = canvas.get_course(course_id)

    proceed = yes_no.ask_yes_no_question("Dit script zorgt er voor dat alle inhoud in een Canvas cursus verwijderd wordt. Ben je heel zeker dat je dit wil doen?")

    if proceed:
        # Delete all pages in the course
        print("Deleting all pages in the course")
        existing_pages = course.get_pages()
        for page in existing_pages:
            page.delete()
        print("Done")

        # Delete all assignments in the course
        print("Deleting all assignments in the course")
        existing_assignments = course.get_assignments()
        for assignment in existing_assignments:
            assignment.delete()
        print("Done")

        # Delete all modules in the course
        print("Deleting all modules in the course")
        existing_modules = course.get_modules()
        for module in existing_modules:
            module.delete()
        print("Done")

        # Create a default assignment group called 'Opdrachten'
        print("Creating default assignment group")
        new_group = course.create_assignment_group(name="Opdrachten", position=1)
        print("Done")

        # Delete all assignment groups in the course, except the newly created 'Opdrachten' group
        print("Deleting all assignment groups in the course, except the newly created 'Opdrachten' group")
        existing_assignment_groups = course.get_assignment_groups()
        for assignment_group in existing_assignment_groups:
            if assignment_group.id != new_group.id:
                assignment_group.delete()
        print("Done")

        # Delete all quizzes in the course
        print("Deleting all quizzes in the course")
        existing_quizzes = course.get_quizzes()
        for quiz in existing_quizzes:
            quiz.delete()
        print("Done")

        # Delete all files in the course
        print("Deleting all files in the course")
        existing_files = course.get_files()
        for file in existing_files:
            file.delete()
        print("Done")

        # Empty the syllabus
        print("Emptying the syllabus")
        course.update(course={"syllabus_body": ""})
        print("Done")