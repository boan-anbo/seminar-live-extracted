from datetime import datetime


class Description:
    html: str
    text: str

    def __init__(self, html: str, text: str) -> None:
        self.html = html
        self.text = text


class End:
    utc: datetime
    local: datetime
    timezone: str

    def __init__(self, utc: datetime, local: datetime, timezone: str) -> None:
        self.utc = utc
        self.local = local
        self.timezone = timezone


class TopLeft:
    x: int
    y: int

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y


class CropMask:
    width: int
    height: int
    top_left: TopLeft

    def __init__(self, width: int, height: int, top_left: TopLeft) -> None:
        self.width = width
        self.height = height
        self.top_left = top_left


class Original:
    url: str
    width: int
    height: int

    def __init__(self, url: str, width: int, height: int) -> None:
        self.url = url
        self.width = width
        self.height = height


class Logo:
    id: int
    url: str
    original: Original
    crop_mask: CropMask
    edge_color: str
    aspect_ratio: int
    edge_color_set: bool

    def __init__(self, id: int, url: str, original: Original, crop_mask: CropMask, edge_color: str, aspect_ratio: int, edge_color_set: bool) -> None:
        self.id = id
        self.url = url
        self.original = original
        self.crop_mask = crop_mask
        self.edge_color = edge_color
        self.aspect_ratio = aspect_ratio
        self.edge_color_set = edge_color_set


class AdapterEventbriteSchema:
    id: str
    end: End
    url: str
    logo: Logo
    name: Description
    start: End
    listed: bool
    locale: str
    source: str
    status: str
    changed: datetime
    created: datetime
    is_free: bool
    logo_id: int
    summary: str
    version: None
    capacity: None
    currency: str
    venue_id: None
    format_id: int
    is_locked: bool
    is_series: bool
    published: datetime
    shareable: bool
    vanity_url: str
    category_id: int
    description: Description
    online_event: bool
    organizer_id: int
    resource_uri: str
    hide_end_date: bool
    tx_time_limit: int
    inventory_type: str
    subcategory_id: None
    hide_start_date: bool
    organization_id: str
    privacy_setting: str
    is_series_parent: bool
    show_pick_a_seat: bool
    capacity_is_custom: None
    is_reserved_seating: bool
    is_externally_ticketed: bool
    show_seatmap_thumbnail: bool
    show_colors_in_seatmap_thumbnail: bool

    def __init__(self, id: str, end: End, url: str, logo: Logo, name: Description, start: End, listed: bool, locale: str, source: str, status: str, changed: datetime, created: datetime, is_free: bool, logo_id: int, summary: str, version: None, capacity: None, currency: str, venue_id: None, format_id: int, is_locked: bool, is_series: bool, published: datetime, shareable: bool, vanity_url: str, category_id: int, description: Description, online_event: bool, organizer_id: int, resource_uri: str, hide_end_date: bool, tx_time_limit: int, inventory_type: str, subcategory_id: None, hide_start_date: bool, organization_id: str, privacy_setting: str, is_series_parent: bool, show_pick_a_seat: bool, capacity_is_custom: None, is_reserved_seating: bool, is_externally_ticketed: bool, show_seatmap_thumbnail: bool, show_colors_in_seatmap_thumbnail: bool) -> None:
        self.id = id
        self.end = end
        self.url = url
        self.logo = logo
        self.name = name
        self.start = start
        self.listed = listed
        self.locale = locale
        self.source = source
        self.status = status
        self.changed = changed
        self.created = created
        self.is_free = is_free
        self.logo_id = logo_id
        self.summary = summary
        self.version = version
        self.capacity = capacity
        self.currency = currency
        self.venue_id = venue_id
        self.format_id = format_id
        self.is_locked = is_locked
        self.is_series = is_series
        self.published = published
        self.shareable = shareable
        self.vanity_url = vanity_url
        self.category_id = category_id
        self.description = description
        self.online_event = online_event
        self.organizer_id = organizer_id
        self.resource_uri = resource_uri
        self.hide_end_date = hide_end_date
        self.tx_time_limit = tx_time_limit
        self.inventory_type = inventory_type
        self.subcategory_id = subcategory_id
        self.hide_start_date = hide_start_date
        self.organization_id = organization_id
        self.privacy_setting = privacy_setting
        self.is_series_parent = is_series_parent
        self.show_pick_a_seat = show_pick_a_seat
        self.capacity_is_custom = capacity_is_custom
        self.is_reserved_seating = is_reserved_seating
        self.is_externally_ticketed = is_externally_ticketed
        self.show_seatmap_thumbnail = show_seatmap_thumbnail
        self.show_colors_in_seatmap_thumbnail = show_colors_in_seatmap_thumbnail
