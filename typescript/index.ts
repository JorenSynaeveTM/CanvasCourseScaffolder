import { apiClient } from "./api/client";
import type { CourseConfig } from "./types/CourseConfig";
import { readFileSync } from "fs";
import Canvas from "./canvasapi/CanvasApi";



const json = readFileSync("data/courseConfig.json", "utf8");
const courseConfig: CourseConfig = JSON.parse(json);
const canvas = new Canvas(
    process.env.CANVAS_API_URL!,
    process.env.CANVAS_API_KEY!
);

(async () => {
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

    console.log("Assignment Groups created")


    console.log(newGroups);

    console.log("Creating Assignments")
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
    console.log("Assignments created")
})();









