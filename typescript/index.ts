import { apiClient } from "./api/client"
import type { CourseConfig } from "./types/CourseConfig"
import { readFileSync } from "fs"
import Canvas from "./api/canvas"



(async () => {
    console.log(process.env)
    // Read the JSON file
    const json = readFileSync("data/courseConfig.json", "utf8")
    const courseConfig: CourseConfig = JSON.parse(json)
    console.log("🚀 ~ courseConfig:", courseConfig)

    // Create a new Canvas instance
    const canvas = new Canvas(process.env.CANVAS_API_URL!, process.env.CANVAS_API_KEY!)
    const course = await canvas.course.get(courseConfig.canvasCourseId)
    console.log("🚀 ~ course:", course.data)
})();