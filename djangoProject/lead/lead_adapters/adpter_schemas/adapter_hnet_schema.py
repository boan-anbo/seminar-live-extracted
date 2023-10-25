class AdapterHnetSchemaElement:
    url: str
    email: str
    title: str
    item_type: None
    keywords: None
    location: None
    description: str
    start_date_time: None

    def __init__(self, url: str, email: str, title: str, item_type: None, keywords: None, location: None, description: str, start_date_time: None) -> None:
        self.url = url
        self.email = email
        self.title = title
        self.item_type = item_type
        self.keywords = keywords
        self.location = location
        self.description = description
        self.start_date_time = start_date_time
