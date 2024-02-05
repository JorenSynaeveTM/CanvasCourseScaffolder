class Page {
    title: string;
    body: string;
    published: boolean;
    constructor(title: string, body: string, published: boolean) {
        this.title = title;
        this.body = body;
        this.published = published;
    }
}

export default Page;