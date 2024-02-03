class AssignmentGroup {
    id?: number
    name: string
    weight: number

    constructor(id: number, name: string, weight: number) {
        this.id = id;
        this.name = name;
        this.weight = weight;
    }
}

export default AssignmentGroup;