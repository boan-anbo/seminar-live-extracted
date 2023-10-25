from dataclasses import dataclass
from typing import Optional, List, Any
from datetime import datetime


@dataclass
class Category:
    short_name_localized: str
    name: str
    short_name: str
    name_localized: str
    id: int
    subcategories: Optional[List[Any]] = None
    schema_url: Optional[str] = None


@dataclass
class End:
    timezone: str
    local: datetime
    utc: datetime


@dataclass
class Logo:
    url: str
    edge_color: str


@dataclass
class Name:
    text: str


@dataclass
class Organizer:
    website: str
    type: str
    user_id: int
    url: str
    twitter: str
    instagram: str
    organization_id: int
    facebook: str
    disable_marketing_opt_in: bool
    id: str
    name: str


@dataclass
class Start:
    utc: datetime
    date_header: str
    timezone: str
    local: datetime
    formatted_time: str


@dataclass
class Address:
    city: str
    country: str
    longitude: str
    localized_address_display: str
    postal_code: str
    address_1: str
    address_2: str
    latitude: str
    localized_multi_line_address_display: List[str]
    localized_area_display: str


@dataclass
class Venue:
    user_id: int
    name: str
    longitude: str
    venue_profile_id: int
    address: Address
    latitude: str
    organizer_id: str
    google_place_id: str
    id: int


@dataclass
class EventViewItem:
    locale: str
    rank: int
    currency: str
    date_header: str
    logo: Logo
    organizer: Organizer
    id: str
    category: Category
    venue_id: int
    user_id: int
    start: Start
    show_seatmap_thumbnail: bool
    inventory_type: str
    show_colors_in_seatmap_thumbnail: bool
    logo_id: int
    source: str
    listed: bool
    is_series: bool
    hide_end_date: bool
    status: str
    type: str
    format: Category
    show_pick_a_seat: bool
    is_free: bool
    organization_id: int
    is_externally_ticketed: bool
    is_protected_event: bool
    is_series_parent: bool
    end: End
    format_id: int
    tld: str
    price_range: str
    name: Name
    language: str
    url: str
    venue: Venue
    summary: str
    is_locked: bool
    shareable: bool
    style_id: int
    online_event: bool
    organizer_id: str
    category_id: int
    survey_type: str
    published: datetime
