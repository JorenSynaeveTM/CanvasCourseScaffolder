import os
from bs4 import BeautifulSoup as bs

from src.models.module_content import ModuleContentType


class Scaffolder:
    def __init__(self, course, path_to_config):
        self.course = course
        self.path_to_config = path_to_config

    def scaffold_course_image(self, path_to_image):
        """ Scaffold the image if present """

        if path_to_image == None or path_to_image == "":
            return

        print("Scaffolding image...")
        try:
            res = self.course.upload(path_to_image)
            image_id = res[1]['id']
            self.course.update(course=({"image_id": image_id}))
            print("Image scaffolded.")
        except:
            print("Image scaffold failed.")

    def scaffold_pages(self, pages):
        """ Scaffolds all pages """
        print("Scaffolding pages...")
        for page in pages:
            existing_pages = self.course.get_pages(search_term=page.title)
            for ex_page in existing_pages:
                ex_page.delete()

            # Create the page
            page_id = self.course.create_page(wiki_page={
                "title": page.title,
                "body": page.body,
                "published": page.published,
                "front_page": page.front_page
            })
            page.id = page_id

        print("Pages scaffolded.")
        return pages

    def scaffold_studiewijzer(self, info) -> int:
        # Get all pages that should be in the studiewijzer module
        leerdoelen_page = self.course.get_pages(search_term="Leerdoelen")
        planning_page = self.course.get_pages(search_term="Planning")
        feedback_page = self.course.get_pages(search_term="Feedback")
        toetsing_page = self.course.get_pages(search_term="Toetsing")
        studiemateriaal_page = self.course.get_pages(search_term="Studiemateriaal")

        pages = [leerdoelen_page, planning_page,
                 feedback_page, toetsing_page, studiemateriaal_page]

        # Delete the old module
        print("Deleting old studiewijzer module...")
        existing_modules = self.course.get_modules(search_term="Studiewijzer")
        for ex_module in existing_modules:
            ex_module.delete()
        print("Old studiewijzer module deleted.")

        # Create the module
        print("Scaffolding studiewijzer module...")
        module = studiewijzer_module = self.course.create_module({
            'name': f"Studiewijzer voor {info.course_name}",
            'position': 1,
        })
        print("Studiewijzer module scaffolded.")

        for page in pages:
            module.create_module_item(module_item={
                'type': "Page",
                'title': page[0].title,
                'page_url': page[0].url,
                'published': True,
            })

        module.edit(module={'published': True})

        return module.id

    def scaffold_syllabus(self, studiewijzer_module_id, info):
        """ Scaffolds the syllabus if present """

        print("Scaffolding syllabus...")

        # Get the absolute path of the script
        script_path = os.path.realpath(__file__)

        # Get the script directory
        script_dir = os.path.dirname(script_path)

        res = self.course.upload(
            os.path.join(script_dir, 'templates', 'info.png'))
        info_icon_id = res[1]['id']

        res = self.course.upload(
            os.path.join(script_dir, 'templates', 'lijst.png'))
        list_icon_id = res[1]['id']

        res = self.course.upload(
            os.path.join(script_dir, 'templates', 'persoon.png'))
        person_icon_id = res[1]['id']

        res = self.course.upload(
            os.path.join(script_dir, 'templates', 'Banner_TM.png'))
        banner_image_id = res[1]['id']

        course_introduction_path = os.path.join(self.path_to_config, 'paginas', 'cursusinleiding.html')
        with open(course_introduction_path, 'r') as html_file:
            course_introduction_body = html_file.read()
        html_file.close()

        syllabus_path = os.path.join(script_dir, 'templates', 'syllabus.html')
        # Check if syllabus.html file exists in the 'scaffold-resources' folder
        if os.path.isfile(syllabus_path):
            # Read the syllabus html file in the same directory as this script
            with open(syllabus_path, 'r') as html_file:
                syllabus_body = html_file.read()
            html_file.close()

            # Replace images
            syllabus_body = syllabus_body.replace(
                "$info_icon_id$", str(info_icon_id))
            syllabus_body = syllabus_body.replace(
                "$list_icon_id$", str(list_icon_id))
            syllabus_body = syllabus_body.replace(
                "$person_icon_id$", str(person_icon_id))
            syllabus_body = syllabus_body.replace(
                "$banner_image_id$", str(banner_image_id))

            # Replace $studiewijzer_module_id$ with the actual studiewijzer module id
            syllabus_body = syllabus_body.replace(
                "$studiewijzer_module_id$", str(studiewijzer_module_id))

            # Replace $courseId$ with the actual course id
            syllabus_body = syllabus_body.replace(
                "$course_id$", str(info.course_id))
            # Replace $contact$ with the actual contacts
            contact_list = ""
            all_contacts = info.contacts.split(',')
            for contact in all_contacts:
                contact_list += f"<li><a href='mailto:{contact.strip()}'>{contact.strip()}</a></li>"
            syllabus_body = syllabus_body.replace("$contact$", contact_list)
            # Replace $course_introduction$ with the actual course introduction
            syllabus_body = syllabus_body.replace(
                "$course_introduction$", course_introduction_body)

            # If the studiewijzer_module_id is None, it should be removed from the syllabus
            if studiewijzer_module_id is None:
                soup = bs(syllabus_body, 'html.parser')
                # Find a tag with id 'studiewijzer' and remove it
                studiewijzer_tag = soup.find(id='studiewijzer')
                studiewijzer_tag.decompose()
                syllabus_body = str(soup)

            # Create the syllabus page
            self.course.update(
                course=({"syllabus_body": syllabus_body, "default_view": "syllabus"}))
            print("Syllabus scaffolded.")
        else:
            print("No syllabus.html file found. Skipping syllabus scaffold.")

    def scaffold_assignment_groups(self, assignment_groups):
        print("Scaffolding assignment groups...")

        # If any of the assignment_groups have a weight different from 0, set the group_weight attribute of the course
        if any(group.weight != 0 for group in assignment_groups):
            self.course.update(course=({"apply_assignment_group_weights": True}))

        # Get the existing assignment groups
        existing_assignment_groups = self.course.get_assignment_groups()
        for group in assignment_groups:
            # check if the group already exists
            existing_group = next(
                (x for x in existing_assignment_groups if x.name == group.name), None)
            if existing_group != None:
                # Update the existing group
                existing_group.edit(
                    group_weight=group.weight, name=group.name)
                group.id = existing_group.id
                continue
            # Create the new group
            a_group = self.course.create_assignment_group(
                name=group.name, group_weight=group.weight)
            group.id = a_group.id

        # Delete the default assignment group called 'Opdrachten'
        default_group = next(
            (x for x in existing_assignment_groups if x.name == "Opdrachten"), None)
        if default_group != None:
            default_group.delete()

        print("Assignment groups scaffolded.")

    def scaffold_assignments(self, assignments, assignment_groups):
        """ Scaffolds the assignments """

        print("Scaffolding assignments...")

        # Delete all existing assignments
        existing_assignments = self.course.get_assignments()
        for assignment in existing_assignments:
            assignment.delete()
        # Scaffold the assignments
        for assignment in assignments:
            assignment_group = next(
                (x for x in assignment_groups if x.name == assignment.assignment_group), None)
            if assignment_group.id is None:
                raise Exception(
                    f"Assignment group with id {assignment.assignment_group} not found")
            a = self.course.create_assignment(assignment={
                'name': assignment.name,
                'due_at': assignment.due_at,
                'points_possible': assignment.points,
                'assignment_group_id': assignment_group.id,
                'published': assignment.published,
                'description': assignment.description_content,
            })
            assignment.id = a.id

        print("Assignments scaffolded.")
        return assignments

    def scaffold_quizzes(self, quizzes, assignment_groups):
        """ Scaffolds the quizzes """

        print("Scaffolding quizzes...")

        # Delete all existing quizzes
        existing_quizzes = self.course.get_quizzes()
        for quiz in existing_quizzes:
            quiz.delete()
        # Scaffold the quizzes
        for quiz in quizzes:
            canvas_assignment_group = next(
                (x for x in assignment_groups if x.name == quiz.assignment_group), None)
            if canvas_assignment_group is None:
                raise Exception(
                    f"Assignment group with id {quiz.assignment_group} not found")
            q = self.course.create_quiz(quiz={
                'title': quiz.name,
                'due_at': quiz.due_at,
                'points_possible': quiz.points,
                'assignment_group_id': canvas_assignment_group.id,
                'published': quiz.published,
            })
            quiz.id = q.id

        print("Quizzes scaffolded.")
        return quizzes

    def scaffold_modules(self, modules, assignments, quizzes):
        """ Scaffolds the modules """

        print("Scaffolding modules...")

        # Delete all existing modules
        existing_modules = self.course.get_modules()
        for module in existing_modules:
            module.delete()
        # Scaffold the modules
        for module in modules:
            m = self.course.create_module(module={
                'name': module.name,
            })
            module.id = m.id
            # Scaffold the contents
            for content in module.contents:
                if content.type == ModuleContentType.URL.name:
                    m.create_module_item({
                        'type': "ExternalUrl",
                        'title': content.display_name,
                        'external_url': content.url,
                        'new_tab': True,
                        'published': content.published,
                    })
                elif content.type == ModuleContentType.ASSIGNMENT.name:
                    assignment = next(
                        (x for x in assignments if x.name == content.assignment), None)
                    if assignment is None:
                        raise Exception(
                            f"Assignment with name {content.assignment} not found")
                    m.create_module_item({
                        'type': "Assignment",
                        'title': content.display_name,
                        'content_id': assignment.id,
                        'published': content.published,
                    })
                elif content.type == ModuleContentType.QUIZ.name:
                    quiz = next(
                        (x for x in quizzes if x.name == content.quiz), None)
                    if quiz is None:
                        raise Exception(
                            f"Quiz with name {content.quiz} not found")
                    m.create_module_item({
                        'type': "Quiz",
                        'title': content.display_name,
                        'content_id': quiz.id,
                        'published': content.published,
                    })
                elif content.type == ModuleContentType.FILE.name:
                    # Check if the file exists
                    if not os.path.isfile(content.file_path):
                        raise Exception(
                            f"File with path {content.file_path} not found")
                    # Upload the file
                    res = self.course.upload(content.file_path)
                    file_id = res[1]['id']
                    # Create the module item
                    m.create_module_item({
                        'type': "File",
                        'title': content.display_name,
                        'content_id': file_id,
                        'published': content.published,
                    })

            m.edit(module={'published': module.published})

        print("Modules scaffolded.")
