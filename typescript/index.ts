import { apiClient } from "./api/client";
import type { CourseConfig } from "./types/CourseConfig";
import { readFileSync } from "fs";
import Canvas from "./canvasapi/CanvasApi";
import ModuleItem from "./canvasapi/types/ModuleItem";
import { CourseDefaultView } from "./canvasapi/types/Course";
import mustache from "mustache";






const json = readFileSync("data/courseConfig.json", "utf8");
const courseConfig: CourseConfig = JSON.parse(json);
const canvas = new Canvas(
    process.env.CANVAS_API_URL!,
    process.env.CANVAS_API_KEY!
);

const createAssignmentGroups = async () => {
    var newGroups: Array<{ id: number, canvasId: number }> = await Promise.all(courseConfig.assignmentGroups.assignmentGroupsItems.map(async (assignmentGroup) => {
        const res = await canvas.assignmentGroup.create(
            courseConfig.canvasCourseId,
            {
                name: assignmentGroup.name,
                group_weight: assignmentGroup.percentageOfTotal,
            }
        )

        return { id: assignmentGroup.id, canvasId: res.id };
    }));

    return newGroups;
}

const createAssignments = async (newGroups: Array<{ id: number, canvasId: number }>) => {
    var newAssignments = await Promise.all(courseConfig.assignments.assignmentsItems.map(async (assignment) => {
        const group = newGroups.find((group) => group.id === assignment.assignmentGroupId);
        if (!group) {
            throw new Error(`Assignment group with id ${assignment.assignmentGroupId} not found`);
        }

        const res = await canvas.assignment.create(
            courseConfig.canvasCourseId,
            {
                name: assignment.name,
                assignmentGroupId: group.canvasId,
            }
        );

        return res;
    }));

    return newAssignments;
}


const configureEvaluation = async () => {

}

const configureEcts = async () => {
    let ectsPages: Array<{ name: string, canvasId: number }> = []
    // Evaluatie
    let html = '<b>Eerste examenkans</b>'
    html += '<ul>'
    courseConfig.ects.evaluation.firstAttempt.firstAttemptItems.forEach((item) => {
        html += `<li>${item.name} - ${item.percentageOfTotal}%`

        if (item.description) {
            html += `<ul><li>${item.description}</li></ul>`
        }

        html += '</li>'
    });

    html += '</ul>'

    html += '<b>Tweede examenkans</b>'
    html += '<ul>'
    courseConfig.ects.evaluation.secondAttempt.secondAttemptItems.forEach((item) => {
        html += `<li>${item.name} - ${item.percentageOfTotal}%`

        if (item.description) {
            html += `<ul><li>${item.description}</li></ul>`
        }

        html += '</li>'
    });

    html += '</ul>'

    let page = await canvas.page.create(courseConfig.canvasCourseId, {
        body: html,
        published: true,
        title: "Evaluatie"
    })
    ectsPages.push({ name: "Evaluatie", canvasId: page.page_id });

    // Leerdoelen
    html = '<p>In dit opleidingsonderdeel worden deze leerdoelen afgetoetst:</p>'
    html += '<ol>'
    courseConfig.ects.learningGoals.learningGoalsItems.forEach((item) => {
        html += `<li>${item.name}</li>`
    });
    html += '</ol>'
    page = await canvas.page.create(courseConfig.canvasCourseId, {
        body: html,
        published: true,
        title: "Leerdoelen"
    })
    ectsPages.push({ name: "Leerdoelen", canvasId: page.page_id });

    // Studiemateriaal
    html = '<p>Volgende studiematerialen worden gebruikt:</p>'
    html += '<ul>'
    courseConfig.ects.courseMaterial.courseMaterialItems.forEach((item) => {
        html += `<li>${item.name}</li>`
    });
    html += '</ul>'
    page = await canvas.page.create(courseConfig.canvasCourseId, {
        body: html,
        published: true,
        title: "Studiemateriaal"
    })
    ectsPages.push({ name: "Studiemateriaal", canvasId: page.page_id });

    // Planning
    html = '<p>In deze cursus komen volgende onderwerpen aan bod:</p>'
    html += '<ul>'
    courseConfig.ects.planning.planningItems.forEach((item) => {
        html += `<li>${item.name}</li>`
    });
    html += '</ul>'
    page = await canvas.page.create(courseConfig.canvasCourseId, {
        body: html,
        published: true,
        title: "Planning"
    })
    ectsPages.push({ name: "Planning", canvasId: page.page_id });

    return ectsPages;
}



const configureSyllabus = async () => {

}

const createModules = async () => {
    var newModules = await Promise.all(courseConfig.modules.modulesItems.map(async (module) => {
        const res = await canvas.module.create(
            courseConfig.canvasCourseId,
            {
                name: module.name,
                published: true,
                position: module.position
            }
        )

        return { id: module.id, canvasId: res.id };
    }));

    return newModules;
}

const createStudyguide = async (ectsPages: Array<{ name: string, canvasId: number }>) => {
    console.log("Creating studyguide")
    console.log(ectsPages)
    // Create a new module for the studyguide
    const res = await canvas.module.create(
        courseConfig.canvasCourseId,
        {
            name: "Studiewijzer",
            published: true,
            position: 1
        }
    )
    console.log("Module created ", res)
    // Add all pages to the module
    await Promise.all(ectsPages.map(async (page) => {
        await canvas.moduleItem.create(
            courseConfig.canvasCourseId,
            res.id,
            ModuleItem.pageModuleItem(page.name, page.canvasId, page.name)
        )
    }));
    // Publish the module
    await canvas.module.update(courseConfig.canvasCourseId, res.id, { name: "Studiewijzer", published: true, position: res.position });

    return res.id;
}

const createSyllabus = async (studiewijzerModuleId: number) => {
    let images = [
        { key: 'banner', url: 'https://i.imgur.com/FJTNXIw.png', name: 'banner.png', canvasId: 0 },
        { key: 'info', url: 'https://i.imgur.com/x46YCqA.png', name: 'info.png', canvasId: 0 },
        { key: 'lijst', url: 'https://i.imgur.com/M5HW0ZZ.png', name: 'lijst.png', canvasId: 0 },
        { key: 'persoon', url: 'https://i.imgur.com/Xv4wT1t.png', name: 'persoon.png', canvasId: 0 },
    ]

    await Promise.all(images.map(async (image) => {
        const fetchRes = await fetch(image.url);
        const blob = await fetchRes.blob();
        const res = await canvas.file.upload(courseConfig.canvasCourseId, blob, image.name);
        // Add the id to the images object
        console.log("Image uploaded ", res)
        image.canvasId = res
    }));
    // Read the template syllabus from the file
    let syllabus = readFileSync("data/template-files/syllabus.html", "utf8");
    // Render the template with the course info
    const output = mustache.render(syllabus, {
        courseId: courseConfig.canvasCourseId,
        bannerIconId: images.find((image) => image.key === 'banner')!.canvasId!.toString(),
        infoIconId: images.find((image) => image.key === 'info')!.canvasId!.toString(),
        lijstIconId: images.find((image) => image.key === 'lijst')!.canvasId!.toString(),
        persoonIconId: images.find((image) => image.key === 'persoon')!.canvasId!.toString(),
        courseIntro: courseConfig.courseInfo.shortDescription,
        lecturers: courseConfig.lecturers.LecturersItems.map((lecturer) => '<li><a href="mailto:' + lecturer.email + '">' + lecturer.firstname + ' ' + lecturer.lastname + '</a></li>').join(''),
        studiewijzerModuleId: studiewijzerModuleId
    });

    // Upload the syllabus to canvas
    const res = await canvas.course.update(courseConfig.canvasCourseId, { syllabusBody: output, defaultView: CourseDefaultView.Syllabus });
}

(async () => {
    const newGroups = await createAssignmentGroups();
    console.log("Assignment Groups created")
    console.log("Creating Assignments")
    const newAssignments = await createAssignments(newGroups);
    console.log("Assignments created")
    console.log("Configuring ECTS pages")
    const ectsPages = await configureEcts();
    console.log("ECTS pages configured")
    console.log("Creating studyguide")
    const studyguideModuleId = await createStudyguide(ectsPages);
    console.log("Studyguide created")
    console.log("Creating modules")
    const newModules = await createModules();
    console.log("Modules created")
    console.log("Creating syllabus")
    await createSyllabus(studyguideModuleId);
    console.log("Syllabus created")
})();









