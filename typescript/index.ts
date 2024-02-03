import { apiClient } from "./api/client"
import type { CourseConfig } from "./types/CourseConfig"
import { readFileSync } from "fs"
import Canvas from "./canvasapi/CanvasApi";



(async () => {
    // Read the JSON file
    const json = readFileSync("data/courseConfig.json", "utf8")
    const courseConfig: CourseConfig = JSON.parse(json)
    console.log("🚀 ~ courseConfig:", courseConfig)

    const canvas = new Canvas(process.env.CANVAS_API_URL!, process.env.CANVAS_API_KEY!)
    const course = await canvas.course.get(courseConfig.canvasCourseId)
    await canvas.assignmentGroup.create(courseConfig.canvasCourseId, {
        name: "Test Assignment Group",
        weight: 10
    })
})();