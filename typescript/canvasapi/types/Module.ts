class Module {
    name: string;
    published?: boolean;
    position?: number;

    constructor(name: string, published?: boolean, position?: number) {
        this.name = name;
        this.published = published;
        this.position = position;
    }

    static toFormData = (module: Module) => {
        let formdata = new FormData();
        formdata.append("module[name]", module.name);
        if (module.position) {
            formdata.append("module[position]", module.position.toString());
        }
        if (module.published) {
            formdata.append("module[published]", module.published.toString());
        }
        return formdata;
    }
}

export default Module;