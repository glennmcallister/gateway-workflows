# Copyright 2017 BlueCat Networks. All rights reserved.

from wtforms import SubmitField
from bluecat.wtform_fields import Configuration, View, Zone, IP4Address, CustomStringField
from bluecat.wtform_extensions import GatewayForm


def filter_unallocated(res):
    if res['status'] == 'SUCCESS' and res['data']['state'] != u'UNALLOCATED':
        res['status'] = 'FAIL'
        res['message'] = 'IP status must be unallocated.'
    return res


class GenericFormTemplate(GatewayForm):
    # When updating the form, remember to make the corresponding changes to the workflow pages
    workflow_name = 'add_dhcp_ip4_address_example'
    workflow_permission = 'add_dhcp_ip4_address_example_page'
    configuration = Configuration(
        workflow_name=workflow_name,
        permissions=workflow_permission,
        label='Configuration',
        required=True,
        coerce=int,
        validators=[],
        is_disabled_on_start=False,
        on_complete=['call_view'],
        enable_on_complete=['view']
    )

    view = View(
        workflow_name=workflow_name,
        permissions=workflow_permission,
        label='View',
        required=True,
        one_off=True,
        on_complete=['call_zone'],
        enable_on_complete=['zone']
    )

    zone = Zone(
        workflow_name=workflow_name,
        permissions=workflow_permission,
        label='Zone',
        required=True,
        enable_on_complete=['ip4_address']
    )

    ip4_address = IP4Address(
        workflow_name=workflow_name,
        permissions=workflow_permission,
        label='Address',
        required=True,
        inputs={'configuration': 'configuration', 'address': 'ip4_address'},
        result_decorator=filter_unallocated,
        enable_on_complete=['hostname', 'mac_address', 'description', 'submit']
    )

    hostname = CustomStringField(
        label='Hostname',
        required=True
    )

    mac_address = CustomStringField(
        label='MAC Address'
    )

    description = CustomStringField(
        label='Description'
    )

    submit = SubmitField(label='Submit')
