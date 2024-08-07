# Copyright (c) 2024 Airbyte, Inc., all rights reserved.
from __future__ import annotations

import re

import pytest
import requests_mock
from freezegun import freeze_time

from airbyte_cdk.test.utils.assertions import assert_good_read
from airbyte_cdk.test.utils.reading import read_records
from airbyte_protocol.models import SyncMode

from .common import config, source
from .conftest import (
    coupons_http_calls,
    customers_http_calls,
    order_notes_http_calls,
    orders_http_calls,
    payment_gateways_http_calls,
    product_attribute_terms_http_calls,
    product_attributes_http_calls,
    product_categories_http_calls,
    product_reviews_http_calls,
    product_shipping_classes_http_calls,
    product_tags_http_calls,
    product_variations_http_calls,
    products_http_calls,
    refunds_http_calls,
    shipping_methods_http_calls,
    shipping_zone_locations_http_calls,
    shipping_zone_methods_http_calls,
    shipping_zones_http_calls,
    system_status_tools_http_calls,
)


def modified_before() -> str:
    return "2017-01-29T00:00:00"


@freeze_time(modified_before())
@requests_mock.Mocker(kw="mock")
@pytest.mark.parametrize(
    "stream_name, num_records, http_calls",
    [
        # Streams without parent streams
        ("customers", 2, customers_http_calls()),
        ("coupons", 2, coupons_http_calls()),
        ("orders", 2, orders_http_calls()),
        ("payment_gateways", 4, payment_gateways_http_calls()),
        ("product_attributes", 2, product_attributes_http_calls()),
        ("product_categories", 7, product_categories_http_calls()),
        ("product_reviews", 2, product_reviews_http_calls()),
        ("products", 2, products_http_calls()),
        ("product_shipping_classes", 2, product_shipping_classes_http_calls()),
        ("product_tags", 2, product_tags_http_calls()),
        ("shipping_methods", 3, shipping_methods_http_calls()),
        ("shipping_zones", 2, shipping_zones_http_calls()),
        ("system_status_tools", 9, system_status_tools_http_calls()),
        # Streams with parent streams
        ("order_notes", 6, order_notes_http_calls()),
        ("product_attribute_terms", 14, product_attribute_terms_http_calls()),
        ("product_variations", 4, product_variations_http_calls()),
        ("refunds", 4, refunds_http_calls()),
        ("shipping_zone_locations", 2, shipping_zone_locations_http_calls()),
        ("shipping_zone_methods", 4, shipping_zone_methods_http_calls()),
    ]
)
def test_read_simple_endpoints_successfully(stream_name, num_records, http_calls, **kwargs) -> None:
    """Test basic read for  all streams that don't have parent streams."""

    # Register mock response
    for call in http_calls:
        request, response = call["request"], call["response"]
        matcher = re.compile(request["url"]) if request["is_regex"] else request["url"]
        kwargs["mock"].get(matcher, **response)

    # Read records
    output = read_records(source(), config(), stream_name, SyncMode.full_refresh)

    # Check read was successful
    assert_good_read(output, num_records)
