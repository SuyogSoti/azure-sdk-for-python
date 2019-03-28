# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
#
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class TransferDetails(Model):
    """Details of the transfer.

    Variables are only populated by the server, and will be ignored when
    sending a request.

    :ivar creation_time: Transfer creation time.
    :vartype creation_time: datetime
    :ivar expiration_time: Transfer expiration time.
    :vartype expiration_time: datetime
    :ivar invoice_section_id: Target invoice section Id.
    :vartype invoice_section_id: str
    :ivar billing_account_id: Target billing account Id.
    :vartype billing_account_id: str
    :ivar transfer_status: Overall transfer status. Possible values include:
     'Pending', 'InProgress', 'Completed', 'CompletedWithErrors', 'Failed',
     'Canceled', 'Declined'
    :vartype transfer_status: str or ~azure.mgmt.billing.models.TransferStatus
    :ivar recipient_email_id: Email Id of recipient of transfer.
    :vartype recipient_email_id: str
    :ivar initiator_email_id: Email Id of initiator of transfer.
    :vartype initiator_email_id: str
    :ivar canceled_by: Email Id who user canceled the transfer.
    :vartype canceled_by: str
    :ivar last_modified_time: Transfer last modification time.
    :vartype last_modified_time: datetime
    :ivar detailed_transfer_status: Detailed transfer status.
    :vartype detailed_transfer_status:
     list[~azure.mgmt.billing.models.DetailedTransferStatus]
    """

    _validation = {
        'creation_time': {'readonly': True},
        'expiration_time': {'readonly': True},
        'invoice_section_id': {'readonly': True},
        'billing_account_id': {'readonly': True},
        'transfer_status': {'readonly': True},
        'recipient_email_id': {'readonly': True},
        'initiator_email_id': {'readonly': True},
        'canceled_by': {'readonly': True},
        'last_modified_time': {'readonly': True},
        'detailed_transfer_status': {'readonly': True},
    }

    _attribute_map = {
        'creation_time': {'key': 'properties.creationTime', 'type': 'iso-8601'},
        'expiration_time': {'key': 'properties.expirationTime', 'type': 'iso-8601'},
        'invoice_section_id': {'key': 'properties.invoiceSectionId', 'type': 'str'},
        'billing_account_id': {'key': 'properties.billingAccountId', 'type': 'str'},
        'transfer_status': {'key': 'properties.transferStatus', 'type': 'str'},
        'recipient_email_id': {'key': 'properties.recipientEmailId', 'type': 'str'},
        'initiator_email_id': {'key': 'properties.initiatorEmailId', 'type': 'str'},
        'canceled_by': {'key': 'properties.canceledBy', 'type': 'str'},
        'last_modified_time': {'key': 'properties.lastModifiedTime', 'type': 'iso-8601'},
        'detailed_transfer_status': {'key': 'properties.detailedTransferStatus', 'type': '[DetailedTransferStatus]'},
    }

    def __init__(self, **kwargs) -> None:
        super(TransferDetails, self).__init__(**kwargs)
        self.creation_time = None
        self.expiration_time = None
        self.invoice_section_id = None
        self.billing_account_id = None
        self.transfer_status = None
        self.recipient_email_id = None
        self.initiator_email_id = None
        self.canceled_by = None
        self.last_modified_time = None
        self.detailed_transfer_status = None
