class AssignmentGroup {
    id?: number
    name: string
    group_weight: number

    constructor(id: number, name: string, weight: number) {
        this.id = id;
        this.name = name;
        this.group_weight = weight;
    }
}

export default AssignmentGroup;