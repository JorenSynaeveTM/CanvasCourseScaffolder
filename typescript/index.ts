import { apiClient } from "./api/client";
import type { CourseConfig } from "./types/CourseConfig";
import { readFileSync } from "fs";
import Canvas from "./canvasapi/CanvasApi";
import { ModuleItem, ModuleItemType } from "./canvasapi/types/ModuleItem";
import { CourseDefaultView } from "./canvasapi/types/Course";
import mustache from "mustache";

const json = readFileSync("data/37237.json", "utf8");
const courseConfig: CourseConfig = JSON.parse(json);
const canvas = new Canvas(
    process.env.CANVAS_API_URL!,
    process.env.CANVAS_API_KEY!
);

const validateConfig = () => {
    if (!courseConfig.canvasCourseId) throw new Error("canvasCourseId not set in config");
    if (!courseConfig.tileImage) throw new Error("tileImage not set in config");
    if (!courseConfig.courseInfo) throw new Error("courseInfo not set in config");
    if (!courseConfig.lecturers) throw new Error("lecturers not set in config");
    if (!courseConfig.assignmentGroups) throw new Error("assignmentGroups not set in config");
    if (!courseConfig.assignments) throw new Error("assignments not set in config");
    if (!courseConfig.ects) throw new Error("ects not set in config");
    if (!courseConfig.modules) throw new Error("modules not set in config");
    if (!courseConfig.moduleItems) throw new Error("moduleItems not set in config");
    // Check ects
    if (!courseConfig.ects.planning) throw new Error("ects.evaluation not set in config");
    if (!courseConfig.ects.courseMaterial) throw new Error("ects.courseMaterial not set in config");
    if (!courseConfig.ects.learningGoals) throw new Error("ects.learningGoals not set in config");
    if (!courseConfig.ects.evaluation) throw new Error("ects.evaluation not set in config");
    if (!courseConfig.ects.evaluation.firstAttempt) throw new Error("ects.evaluation.firstAttempt not set in config");
    if (!courseConfig.ects.evaluation.secondAttempt) throw new Error("ects.evaluation.secondAttempt not set in config");
    // Check planning
    if (!courseConfig.ects.planning.planningItems) throw new Error("ects.planning.planningItems not set in config");
    if (courseConfig.ects.planning.planningItems.length == 0) throw new Error("ects.planning.planningItems is empty");
    // Check course material
    if (!courseConfig.ects.courseMaterial.courseMaterialItems) throw new Error("ects.courseMaterial.courseMaterialItems not set in config");
    if (courseConfig.ects.courseMaterial.courseMaterialItems.length == 0) throw new Error("ects.courseMaterial.courseMaterialItems is empty");
    // Check learning goals
    if (!courseConfig.ects.learningGoals.learningGoalsItems) throw new Error("ects.learningGoals.learningGoalsItems not set in config");
    if (courseConfig.ects.learningGoals.learningGoalsItems.length == 0) throw new Error("ects.learningGoals.learningGoalsItems is empty");
    // Check evaluation
    if (!courseConfig.ects.evaluation.firstAttempt.firstAttemptItems) throw new Error("ects.evaluation.firstAttempt.firstAttemptItems not set in config");
    if (courseConfig.ects.evaluation.firstAttempt.firstAttemptItems.length == 0) throw new Error("ects.evaluation.firstAttempt.firstAttemptItems is empty");
    if (courseConfig.ects.evaluation.firstAttempt.firstAttemptItems.reduce((acc, item) => acc + item.percentageOfTotal, 0) !== 100) throw new Error("The sum of the percentages of the first attempt items should be 100");
    if (!courseConfig.ects.evaluation.secondAttempt.secondAttemptItems) throw new Error("ects.evaluation.secondAttempt.secondAttemptItems not set in config");
    if (courseConfig.ects.evaluation.secondAttempt.secondAttemptItems.length == 0) throw new Error("ects.evaluation.secondAttempt.secondAttemptItems is empty");
    if (courseConfig.ects.evaluation.secondAttempt.secondAttemptItems.reduce((acc, item) => acc + item.percentageOfTotal, 0) !== 100) throw new Error("The sum of the percentages of the second attempt items should be 100");
    // Check moduleItems
    if (!courseConfig.moduleItems.moduleItemsItems) throw new Error("moduleItems.moduleItemsItems not set in config");
    // Get all moduleIds
    const moduleIds = courseConfig.modules.modulesItems.map((module) => module.id);
    // Check if all moduleItems have a valid moduleId
    courseConfig.moduleItems.moduleItemsItems.forEach((moduleItem) => {
        if (!moduleIds.includes(moduleItem.moduleId)) throw new Error(`Module with id ${moduleItem.moduleId} not found`);
    });
}

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

        return { id: assignment.assignmentId, canvasId: res.id }
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

const createModules = async () => {
    let newModules: Array<{ id: number, canvasId: number }> = []

    // Use a for loop here as the order of the modules is important
    for (let i = 0; i < courseConfig.modules.modulesItems.length; i++) {
        const module = courseConfig.modules.modulesItems[i];
        const res = await canvas.module.create(
            courseConfig.canvasCourseId,
            {
                name: module.name,
                published: true,
                position: module.position
            }
        )
        newModules.push({ id: module.id, canvasId: res.id });
    }

    return newModules;
}

const createStudyguide = async (ectsPages: Array<{ name: string, canvasId: number }>) => {
    // Create a new module for the studyguide
    const res = await canvas.module.create(
        courseConfig.canvasCourseId,
        {
            name: "Studiewijzer",
            published: true,
            position: 1
        }
    )
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

const createModuleItems = async (newModules: Array<{ id: number, canvasId: number }>, newAssignments: Array<{ id: number, canvasId: number }>) => {
    await Promise.all(courseConfig.moduleItems.moduleItemsItems.map(async (moduleItem) => {
        const module = newModules.find((module) => module.id === moduleItem.moduleId);

        if (!module) {
            throw new Error(`Module with id ${moduleItem.moduleId} not found`);
        }

        let item;

        switch (moduleItem.type) {
            case ModuleItemType.Page:
                // Todo
                break;
            case ModuleItemType.Assignment:
                const assignment = newAssignments.find((assignment) => assignment.id === moduleItem.assignmentId);
                if (!assignment) throw new Error(`Assignment with id ${moduleItem.moduleItemId} not found.`);
                item = ModuleItem.createAssignmentItem(moduleItem.title, assignment!.canvasId);
                break;
            case ModuleItemType.File:
                break;
            case ModuleItemType.Discussion:
                break;
            case ModuleItemType.Quiz:
                break;
            case ModuleItemType.SubHeader:
                item = ModuleItem.createSubHeaderItem(moduleItem.title);
                break;
            case ModuleItemType.ExternalUrl:
                item = ModuleItem.createExternalUrlItem(moduleItem.title, moduleItem.exteralUrl);
                break;
            case ModuleItemType.ExternalTool:
                break;
        }

        await canvas.moduleItem.create(
            courseConfig.canvasCourseId,
            module.canvasId,
            item
        )
    }));
}

const updateTileImage = async () => {
    const fetchRes = await fetch(courseConfig.tileImage);
    const blob = await fetchRes.blob();
    const res = await canvas.file.upload(courseConfig.canvasCourseId, blob, "course-image.png");
    await canvas.course.update(courseConfig.canvasCourseId, { imageId: res });
}

(async () => {
    try {
        validateConfig();
    } catch (error) {
        const err = error as Error;
        console.error("The config is not valid: ", err.message);
        process.exit(1);
    }
    const newGroups = await createAssignmentGroups();
    console.log("Assignment Groups created")
    console.log("Creating Assignments")
    const newAssignments = await createAssignments(newGroups);
    console.log("Assignments created")
    console.log("Configuring ECTS pages")
    const ectsPages = await configureEcts();
    console.log("ECTS pages configured")
    console.log("Creating modules")
    const newModules = await createModules();
    console.log("Modules created")
    await createModuleItems(newModules, newAssignments);
    console.log("Creating studyguide")
    const studyguideModuleId = await createStudyguide(ectsPages);
    console.log("Studyguide created")
    console.log("Creating syllabus")
    await createSyllabus(studyguideModuleId);
    console.log("Syllabus created")
    console.log("Creating tile image")
    await updateTileImage();
    console.log("Tile image created")
    console.log("Done")
})();









