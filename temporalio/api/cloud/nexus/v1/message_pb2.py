# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: temporal/api/cloud/nexus/v1/message.proto
"""Generated protocol buffer code."""

from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2

from temporalio.api.cloud.resource.v1 import (
    message_pb2 as temporal_dot_api_dot_cloud_dot_resource_dot_v1_dot_message__pb2,
)

DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n)temporal/api/cloud/nexus/v1/message.proto\x12\x1btemporal.api.cloud.nexus.v1\x1a,temporal/api/cloud/resource/v1/message.proto\x1a\x1fgoogle/protobuf/timestamp.proto"\xbe\x01\n\x0c\x45ndpointSpec\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x44\n\x0btarget_spec\x18\x02 \x01(\x0b\x32/.temporal.api.cloud.nexus.v1.EndpointTargetSpec\x12\x45\n\x0cpolicy_specs\x18\x03 \x03(\x0b\x32/.temporal.api.cloud.nexus.v1.EndpointPolicySpec\x12\x13\n\x0b\x64\x65scription\x18\x04 \x01(\t"l\n\x12\x45ndpointTargetSpec\x12K\n\x12worker_target_spec\x18\x01 \x01(\x0b\x32-.temporal.api.cloud.nexus.v1.WorkerTargetSpecH\x00\x42\t\n\x07variant"<\n\x10WorkerTargetSpec\x12\x14\n\x0cnamespace_id\x18\x01 \x01(\t\x12\x12\n\ntask_queue\x18\x02 \x01(\t"\x8c\x01\n\x12\x45ndpointPolicySpec\x12k\n#allowed_cloud_namespace_policy_spec\x18\x01 \x01(\x0b\x32<.temporal.api.cloud.nexus.v1.AllowedCloudNamespacePolicySpecH\x00\x42\t\n\x07variant"7\n\x1f\x41llowedCloudNamespacePolicySpec\x12\x14\n\x0cnamespace_id\x18\x01 \x01(\t"\xad\x02\n\x08\x45ndpoint\x12\n\n\x02id\x18\x01 \x01(\t\x12\x18\n\x10resource_version\x18\x02 \x01(\t\x12\x37\n\x04spec\x18\x03 \x01(\x0b\x32).temporal.api.cloud.nexus.v1.EndpointSpec\x12<\n\x05state\x18\x04 \x01(\x0e\x32-.temporal.api.cloud.resource.v1.ResourceState\x12\x1a\n\x12\x61sync_operation_id\x18\x05 \x01(\t\x12\x30\n\x0c\x63reated_time\x18\x06 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x36\n\x12last_modified_time\x18\x07 \x01(\x0b\x32\x1a.google.protobuf.TimestampB\x9d\x01\n\x1eio.temporal.api.cloud.nexus.v1B\x0cMessageProtoP\x01Z\'go.temporal.io/api/cloud/nexus/v1;nexus\xaa\x02\x1dTemporalio.Api.Cloud.Nexus.V1\xea\x02!Temporalio::Api::Cloud::Nexus::V1b\x06proto3'
)


_ENDPOINTSPEC = DESCRIPTOR.message_types_by_name["EndpointSpec"]
_ENDPOINTTARGETSPEC = DESCRIPTOR.message_types_by_name["EndpointTargetSpec"]
_WORKERTARGETSPEC = DESCRIPTOR.message_types_by_name["WorkerTargetSpec"]
_ENDPOINTPOLICYSPEC = DESCRIPTOR.message_types_by_name["EndpointPolicySpec"]
_ALLOWEDCLOUDNAMESPACEPOLICYSPEC = DESCRIPTOR.message_types_by_name[
    "AllowedCloudNamespacePolicySpec"
]
_ENDPOINT = DESCRIPTOR.message_types_by_name["Endpoint"]
EndpointSpec = _reflection.GeneratedProtocolMessageType(
    "EndpointSpec",
    (_message.Message,),
    {
        "DESCRIPTOR": _ENDPOINTSPEC,
        "__module__": "temporal.api.cloud.nexus.v1.message_pb2",
        # @@protoc_insertion_point(class_scope:temporal.api.cloud.nexus.v1.EndpointSpec)
    },
)
_sym_db.RegisterMessage(EndpointSpec)

EndpointTargetSpec = _reflection.GeneratedProtocolMessageType(
    "EndpointTargetSpec",
    (_message.Message,),
    {
        "DESCRIPTOR": _ENDPOINTTARGETSPEC,
        "__module__": "temporal.api.cloud.nexus.v1.message_pb2",
        # @@protoc_insertion_point(class_scope:temporal.api.cloud.nexus.v1.EndpointTargetSpec)
    },
)
_sym_db.RegisterMessage(EndpointTargetSpec)

WorkerTargetSpec = _reflection.GeneratedProtocolMessageType(
    "WorkerTargetSpec",
    (_message.Message,),
    {
        "DESCRIPTOR": _WORKERTARGETSPEC,
        "__module__": "temporal.api.cloud.nexus.v1.message_pb2",
        # @@protoc_insertion_point(class_scope:temporal.api.cloud.nexus.v1.WorkerTargetSpec)
    },
)
_sym_db.RegisterMessage(WorkerTargetSpec)

EndpointPolicySpec = _reflection.GeneratedProtocolMessageType(
    "EndpointPolicySpec",
    (_message.Message,),
    {
        "DESCRIPTOR": _ENDPOINTPOLICYSPEC,
        "__module__": "temporal.api.cloud.nexus.v1.message_pb2",
        # @@protoc_insertion_point(class_scope:temporal.api.cloud.nexus.v1.EndpointPolicySpec)
    },
)
_sym_db.RegisterMessage(EndpointPolicySpec)

AllowedCloudNamespacePolicySpec = _reflection.GeneratedProtocolMessageType(
    "AllowedCloudNamespacePolicySpec",
    (_message.Message,),
    {
        "DESCRIPTOR": _ALLOWEDCLOUDNAMESPACEPOLICYSPEC,
        "__module__": "temporal.api.cloud.nexus.v1.message_pb2",
        # @@protoc_insertion_point(class_scope:temporal.api.cloud.nexus.v1.AllowedCloudNamespacePolicySpec)
    },
)
_sym_db.RegisterMessage(AllowedCloudNamespacePolicySpec)

Endpoint = _reflection.GeneratedProtocolMessageType(
    "Endpoint",
    (_message.Message,),
    {
        "DESCRIPTOR": _ENDPOINT,
        "__module__": "temporal.api.cloud.nexus.v1.message_pb2",
        # @@protoc_insertion_point(class_scope:temporal.api.cloud.nexus.v1.Endpoint)
    },
)
_sym_db.RegisterMessage(Endpoint)

if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b"\n\036io.temporal.api.cloud.nexus.v1B\014MessageProtoP\001Z'go.temporal.io/api/cloud/nexus/v1;nexus\252\002\035Temporalio.Api.Cloud.Nexus.V1\352\002!Temporalio::Api::Cloud::Nexus::V1"
    _ENDPOINTSPEC._serialized_start = 154
    _ENDPOINTSPEC._serialized_end = 344
    _ENDPOINTTARGETSPEC._serialized_start = 346
    _ENDPOINTTARGETSPEC._serialized_end = 454
    _WORKERTARGETSPEC._serialized_start = 456
    _WORKERTARGETSPEC._serialized_end = 516
    _ENDPOINTPOLICYSPEC._serialized_start = 519
    _ENDPOINTPOLICYSPEC._serialized_end = 659
    _ALLOWEDCLOUDNAMESPACEPOLICYSPEC._serialized_start = 661
    _ALLOWEDCLOUDNAMESPACEPOLICYSPEC._serialized_end = 716
    _ENDPOINT._serialized_start = 719
    _ENDPOINT._serialized_end = 1020
# @@protoc_insertion_point(module_scope)
