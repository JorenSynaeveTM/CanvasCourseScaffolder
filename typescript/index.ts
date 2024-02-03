import { apiClient } from "./api/client"
import type { CourseConfig } from "./types/CourseConfig"
import { readFileSync } from "fs"




(async () => {
    // Read the JSON file
    const json = readFileSync("data/courseConfig.json", "utf8")
    const courseConfig: CourseConfig = JSON.parse(json)
    console.log("🚀 ~ courseConfig:", courseConfig)

    const course = await apiClient.get(`/courses/${courseConfig.canvasCourseId}`)

    console.log("🚀 ~ course:", course.data.name)
})();