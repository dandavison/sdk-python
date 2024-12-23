# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: temporal/api/cloud/resource/v1/message.proto
"""Generated protocol buffer code."""

from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import enum_type_wrapper

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b"\n,temporal/api/cloud/resource/v1/message.proto\x12\x1etemporal.api.cloud.resource.v1*\xe3\x02\n\rResourceState\x12\x1e\n\x1aRESOURCE_STATE_UNSPECIFIED\x10\x00\x12\x1d\n\x19RESOURCE_STATE_ACTIVATING\x10\x01\x12$\n RESOURCE_STATE_ACTIVATION_FAILED\x10\x02\x12\x19\n\x15RESOURCE_STATE_ACTIVE\x10\x03\x12\x1b\n\x17RESOURCE_STATE_UPDATING\x10\x04\x12 \n\x1cRESOURCE_STATE_UPDATE_FAILED\x10\x05\x12\x1b\n\x17RESOURCE_STATE_DELETING\x10\x06\x12 \n\x1cRESOURCE_STATE_DELETE_FAILED\x10\x07\x12\x1a\n\x16RESOURCE_STATE_DELETED\x10\x08\x12\x1c\n\x18RESOURCE_STATE_SUSPENDED\x10\t\x12\x1a\n\x16RESOURCE_STATE_EXPIRED\x10\nB\xac\x01\n!io.temporal.api.cloud.resource.v1B\x0cMessageProtoP\x01Z-go.temporal.io/api/cloud/resource/v1;resource\xaa\x02 Temporalio.Api.Cloud.Resource.V1\xea\x02$Temporalio::Api::Cloud::Resource::V1b\x06proto3"
)

_RESOURCESTATE = DESCRIPTOR.enum_types_by_name["ResourceState"]
ResourceState = enum_type_wrapper.EnumTypeWrapper(_RESOURCESTATE)
RESOURCE_STATE_UNSPECIFIED = 0
RESOURCE_STATE_ACTIVATING = 1
RESOURCE_STATE_ACTIVATION_FAILED = 2
RESOURCE_STATE_ACTIVE = 3
RESOURCE_STATE_UPDATING = 4
RESOURCE_STATE_UPDATE_FAILED = 5
RESOURCE_STATE_DELETING = 6
RESOURCE_STATE_DELETE_FAILED = 7
RESOURCE_STATE_DELETED = 8
RESOURCE_STATE_SUSPENDED = 9
RESOURCE_STATE_EXPIRED = 10


if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b"\n!io.temporal.api.cloud.resource.v1B\014MessageProtoP\001Z-go.temporal.io/api/cloud/resource/v1;resource\252\002 Temporalio.Api.Cloud.Resource.V1\352\002$Temporalio::Api::Cloud::Resource::V1"
    _RESOURCESTATE._serialized_start = 81
    _RESOURCESTATE._serialized_end = 436
# @@protoc_insertion_point(module_scope)
