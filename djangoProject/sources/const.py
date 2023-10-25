from enum import Enum
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List, Any


class TrackingCategory(Enum):
    LISTING = "listing"


@dataclass
class Breadcrumb:
    text: str
    tracking_category: TrackingCategory
    link: str
    tracking_action: str


@dataclass
class Description:
    text: str
    html: str


@dataclass
class End:
    timezone: str
    local: datetime
    utc: datetime


@dataclass
class EventSalesStatus:
    start_sales_date: End
    default_message: None
    sales_status: str
    message_code: None
    message: None
    message_type: None


@dataclass
class ExternalTicketingProperties:
    ticketing_provider_name: None
    maximum_ticket_price: None
    minimum_ticket_price: None
    is_free: None
    sales_end: None
    sales_start: None
    external_url: None


@dataclass
class GroupSettings:
    has_advanced_teams_enabled: bool


@dataclass
class MusicProperties:
    event_id: str
    age_restriction: None
    presented_by: None
    door_time: None


@dataclass
class DiscountInfo:
    pass


@dataclass
class PublicTicketsInfo:
    has_hold_code_without_tickets: bool
    discount_info: DiscountInfo


class Alignment(Enum):
    LEFT = "left"


@dataclass
class Body:
    text: str
    alignment: Alignment


@dataclass
class TopLeft:
    y: int
    x: int


@dataclass
class CropMask:
    width: Optional[int] = None
    top_left: Optional[TopLeft] = None
    height: Optional[int] = None


@dataclass
class Original:
    url: str
    width: int
    height: int


@dataclass
class Image:
    edge_color_set: bool
    corner_style: str
    url: str
    original: Original
    image_id: int
    crop_mask: CropMask
    aspect_ratio: str
    id: int
    edge_color: Optional[str] = None


@dataclass
class Data:
    display_restrictions: List[Any]
    body: Optional[Body] = None
    image: Optional[Image] = None


@dataclass
class ModuleBrokerSOADefaults:
    type: str
    data: DiscountInfo


class TemplatePath(Enum):
    STRUCTURED_CONTENT_IMAGE_HTML = "structured_content/image.html"
    STRUCTURED_CONTENT_TEXT_HTML = "structured_content/text.html"


class TypeEnum(Enum):
    IMAGE = "image"
    TEXT = "text"


@dataclass
class ModuleBroker:
    soa_defaults: ModuleBrokerSOADefaults
    image_set: None
    public_id: int
    template_path: TemplatePath
    type: TypeEnum
    display_restrictions: List[Any]
    nested_keys: List[Any]
    json_blocklist_set: List[Any]
    data: Data
    id: int
    empty_string_for_none: List[Any]
    body_text: Optional[str] = None
    body_alignment: Optional[Alignment] = None
    caption_text: Optional[str] = None
    original_image_url: Optional[str] = None
    alt_text: Optional[str] = None
    image_url: Optional[str] = None


@dataclass
class Module:
    display_restrictions: List[Any]
    type: TypeEnum
    data: Data
    id: int


@dataclass
class StructuredContentSOADefaults:
    modules: List[Any]


@dataclass
class StructuredContent:
    soa_defaults: StructuredContentSOADefaults
    image_set: None
    public_id: int
    has_admat: bool
    artist_list_module: None
    admat: None
    has_artist_presented_by_module: bool
    modules: List[Module]
    nested_keys: List[Any]
    has_text_module: bool
    module_brokers: List[ModuleBroker]
    artist_presented_by_module: None
    has_artist_list_module: bool
    json_blocklist_set: List[Any]
    has_module_brokers: bool
    empty_string_for_none: List[Any]


@dataclass
class TicketModalButton:
    text: str
    tracking_label: str


@dataclass
class AddressToDict:
    city: str
    country: str
    region: str
    longitude: int
    postal_code: str
    address_1: str
    address_2: str
    longaddress: str
    latitude: int


@dataclass
class VenueSOADefaults:
    localized_multi_line_address_display: List[Any]
    postal_code: str
    has_address: bool
    localized_area_display: str
    city: str
    name: str
    country: str
    region: str
    longitude: int
    localized_address_display: str
    address_1: str
    address_2: str
    latitude: int


@dataclass
class Venue:
    public_id: None
    address_to_dict: AddressToDict
    venue: str
    display_multi_line_address: List[Any]
    localized_multi_line_address_display: List[Any]
    postal_code: str
    has_address: None
    json_blocklist_set: List[Any]
    city: str
    venue_id: None
    display_venue_name: str
    localized_area_display: str
    state: str
    latitude: int
    soa_defaults: VenueSOADefaults
    nested_keys: List[str]
    display_address_2: str
    display_address_1: str
    display_area_address: str
    display_full_address_and_name: str
    image_set: None
    name: str
    country: str
    region: str
    should_display_country: bool
    longitude: int
    localized_address_display: str
    address_1: str
    address_2: str
    continent_name: str
    display_full_address: str
    empty_string_for_none: List[Any]


@dataclass
class EventbriteDetail:
    display_date: str
    common_sales_end_date_with_tz: datetime
    public_id: int
    event_is_pick_a_seat_enabled: bool
    panel_display_price: str
    copy_link_absolute_url: str
    event_payment_type: str
    get_team: None
    should_show_sales_end: bool
    attendee_preferred_language: str
    music_properties: MusicProperties
    formatted_external_ticketing_maximum_ticket_price: None
    should_display_order_button: bool
    should_show_credit_card_methods: bool
    paypal_icon_to_display: List[Any]
    is_eventbrite_venue_event: bool
    vanity_url: str
    public_tickets_info: PublicTicketsInfo
    password: str
    display_name: str
    breadcrumbs: List[Breadcrumb]
    show_seatmap_thumbnail: bool
    start_month_abbr: str
    display_short_end_date_time: str
    hide_end_date: bool
    should_show_sales_ended_message: None
    campaign_token: str
    meta_keywords: str
    event_details_door_time_line_two: str
    should_show_related_events_expired: bool
    shortname: str
    add_to_waitlist_url: str
    formatted_max_price: str
    event_details_date_line_one: str
    modal_checkout_button_text: str
    status_is_sold_out: bool
    form_action_url: str
    hide_start_and_end_dates: bool
    has_access_codes: bool
    is_same_start_end_date: bool
    should_accept_mastercard_for_payment: bool
    should_show_status: bool
    is_free: bool
    is_google_analytics_ecommerce_tracking_enabled: bool
    should_show_waitlist_button: bool
    is_protected_event: bool
    display_name_truncated: str
    event_details_door_time_line_one: str
    status_is_sold_out_with_no_resellers: bool
    should_show_remind_me_button: bool
    organizer_id: str
    is_draft: bool
    should_hide_all_dates: bool
    refund_policy_description: str
    should_display_ticket_end_date: bool
    should_show_password_field: bool
    name: Description
    total_tickets: int
    order_payment_options_enabled: bool
    description_has_image: bool
    has_cropped_logo: bool
    display_short_start_date: str
    venue: Venue
    is_unavailable: bool
    should_show_related_events: bool
    is_online_event: bool
    is_sales_ended: bool
    hide_start_date: bool
    moneris_cards_list: List[Any]
    source: str
    should_accept_amex_for_payment: bool
    online_event: bool
    is_series: bool
    event_in_preview_with_no_tickets: bool
    is_reserved_seating: bool
    is_paid: bool
    should_accept_offline: None
    error_message: None
    waitlist_enabled_on_actionable_ticket: bool
    plain_description: str
    should_accept_oxxo: bool
    formatted_min_price: str
    all_tickets_hidden: bool
    start_datetime: datetime
    should_accept_visa_for_payment: bool
    all_tickets_unavailable: bool
    status_to_display: str
    event_details_date_line_two: str
    referral_code: str
    structured_content: StructuredContent
    formatted_sales_end_date: str
    summary: str
    ticket_resellers: List[Any]
    canonical_url: str
    ticket_modal_button: TicketModalButton
    meta_description: str
    should_load_embedded_checkout: bool
    listing_tickets_header: str
    invite_key: None
    fb_plain_description: str
    tracking_beacons: List[Any]
    should_track_user_timing: bool
    status_is_not_yet_started: bool
    should_accept_boleto_bancario: bool
    display_short_end_date: str
    privacy_setting: str
    event_password: None
    display_price: str
    not_yet_on_sale_label: str
    payment_type: str
    show_pick_a_seat: bool
    should_accept_mercado_pago_credit_cards: bool
    external_ticketing_provider_name: str
    listing_panel_datetime: str
    is_access_only: bool
    should_show_aggregate_offer_markup: bool
    should_fire_tracking_beacon: bool
    should_show_price: bool
    should_show_ticket_box: bool
    ticket_classes: List[Any]
    authnet_cards_list: List[Any]
    should_accept_ideal: bool
    payment_method_icons_to_display: List[Any]
    should_accept_pagofacil: bool
    status_any_ticket_not_yet_started: bool
    should_show_door_time: None
    event_expansions: List[str]
    language: str
    created: datetime
    external_tickets_are_free: None
    external_ticketing_provider_label_text: str
    changed: datetime
    is_no_pas: bool
    event_is_reserved_seating: bool
    should_show_promo_code_link: bool
    end_day: str
    place: None
    first_ticket_sales_start_date: str
    affiliate_user: str
    google_analytics: None
    external_tickets_url: None
    is_published: bool
    group_settings: GroupSettings
    should_show_turn_off_reminder_button: bool
    is_sales_client: bool
    should_display_breadcrumbs: bool
    end_month_abbr: str
    should_show_external_ticketing_provider: bool
    image: str
    is_series_parent: bool
    event_details_door_time_line_three: str
    should_show_add_to_calendar: bool
    should_accept_maestro_bancontact: bool
    has_unlimited_donations: bool
    url: str
    formatted_event_details_date_line_one: str
    start_date_with_tz: datetime
    display_start_date_with_tz: datetime
    has_donation_tickets_available: None
    should_accept_discover_for_payment: bool
    is_shareable: bool
    hide_start_time_enabled: bool
    is_donation: bool
    display_end_date_with_tz: datetime
    has_presenter_or_age_restriction: bool
    should_display_crawlable_series_children_links: bool
    display_short_start_date_without_time: str
    should_only_accept_amex_for_payment: bool
    event_invite_key: str
    inventory_type: str
    should_show_hero_image: bool
    show_colors_in_seatmap_thumbnail: bool
    logo_id: int
    locale: str
    remaining_tickets: int
    accept_moneris: bool
    listed: bool
    is_sold_out: bool
    all_tickets_hidden_and_no_access_codes_available: bool
    listing_series_events: None
    is_bookmarked_for_current_user: bool
    should_track_event_view: bool
    is_locked: bool
    external_tickets_sales_start_date_is_in_the_future: bool
    non_vanity_absolute_url_ssl: str
    ssl_logo_url: str
    should_show_paypal_payment_method: bool
    has_advanced_teams_enabled: bool
    display_short_start_date_time: str
    externally_ticketed_event_status_to_display: str
    should_use_embedded_checkout: bool
    should_use_embedded_for_music_event: bool
    organization_id: str
    display_short_start_date_year_optional: str
    is_externally_ticketed: bool
    event_is_sold_out: bool
    should_robots_index: bool
    formatted_external_ticketing_minimum_ticket_price: None
    min_price_decimal: int
    style_id: int
    event_currency_exponent: int
    event_title_tag: str
    status_is_near_sales_end: bool
    password_form_action_url: str
    has_hold_codes: bool
    status_not_yet_on_sale: bool
    should_display_short_address: bool
    should_show_timezone: bool
    accept_authnet: bool
    is_live: bool
    should_block_images: bool
    shareable: bool
    end_datetime: datetime
    get_series_default_option_terminology: str
    has_available_hidden_ticket: bool
    should_display_map: None
    can_purchase_tickets_or_join_event_waitlist: bool
    should_not_index_images: bool
    should_accept_invoice: bool
    max_price_decimal: int
    subcategory_id: int
    display_og_url: str
    should_accept_visa_debit_for_payment: bool
    start_day: str
    should_accept_sofort: bool
    is_opted_out_of_google_analytics_universal: bool
    sales_ended_message: None
    currency: str
    correlation_id: str
    should_show_related_events_expired_v2: bool
    has_logo: bool
    is_viewable_invite_only_without_purchasable_tickets: bool
    should_show_price_on_hero: bool
    should_use_embedded_for_event_with_tiered_inventory: bool
    id: str
    end: End
    status_is_ended: bool
    should_show_offline_payments: bool
    seconds_to_end_date: int
    survey_type: str
    should_show_related_events_live: bool
    sales_not_yet_started: bool
    start: End
    display_sales_ended_message: None
    is_protected: bool
    not_yet_started_notification_text: str
    should_show_event_reseller: bool
    logo_url: str
    get_description_abstract: str
    door_time: None
    external_tickets_are_available: bool
    has_payment_options: bool
    status: str
    should_display_organizer_facebook: bool
    should_display_organizer_twitter: bool
    description: Description
    display_short_address: None
    published: datetime
    status_not_yet_on_sale_access_coded: bool
    end_date_with_tz: datetime
    status_is_unavailable: bool
    is_ended: bool
    should_show_checkout_button: bool
    event_public_id: str
    sales_have_ended: None
    should_accept_rapipago: bool
    format_id: int
    should_show_waitlist_for_event: bool
    tld: str
    event_sales_status: EventSalesStatus
    has_more_than_one_child: None
    sales_status_code: None
    user_id: str
    external_tickets_button_text: str
    has_structured_content: bool
    external_ticketing_properties: ExternalTicketingProperties
    should_use_registration_terminology: bool
    affiliate_code: str
    has_external_ticketing_properties: ExternalTicketingProperties
    should_display_rsvp: bool
    tx_time_limit: int
    should_accept_sepa_direct_debit: bool
    category_id: int
    non_vanity_absolute_url: str
