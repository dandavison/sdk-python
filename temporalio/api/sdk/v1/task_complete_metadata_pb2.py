# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: temporal/api/sdk/v1/task_complete_metadata.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n0temporal/api/sdk/v1/task_complete_metadata.proto\x12\x13temporal.api.sdk.v1"Q\n\x1dWorkflowTaskCompletedMetadata\x12\x17\n\x0f\x63ore_used_flags\x18\x01 \x03(\r\x12\x17\n\x0flang_used_flags\x18\x02 \x03(\rB\x87\x01\n\x16io.temporal.api.sdk.v1B\x19TaskCompleteMetadataProtoP\x01Z\x1dgo.temporal.io/api/sdk/v1;sdk\xaa\x02\x15Temporalio.Api.Sdk.V1\xea\x02\x18Temporalio::Api::Sdk::V1b\x06proto3'
)


_WORKFLOWTASKCOMPLETEDMETADATA = DESCRIPTOR.message_types_by_name[
    "WorkflowTaskCompletedMetadata"
]
WorkflowTaskCompletedMetadata = _reflection.GeneratedProtocolMessageType(
    "WorkflowTaskCompletedMetadata",
    (_message.Message,),
    {
        "DESCRIPTOR": _WORKFLOWTASKCOMPLETEDMETADATA,
        "__module__": "temporal.api.sdk.v1.task_complete_metadata_pb2"
        # @@protoc_insertion_point(class_scope:temporal.api.sdk.v1.WorkflowTaskCompletedMetadata)
    },
)
_sym_db.RegisterMessage(WorkflowTaskCompletedMetadata)

if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b"\n\026io.temporal.api.sdk.v1B\031TaskCompleteMetadataProtoP\001Z\035go.temporal.io/api/sdk/v1;sdk\252\002\025Temporalio.Api.Sdk.V1\352\002\030Temporalio::Api::Sdk::V1"
    _WORKFLOWTASKCOMPLETEDMETADATA._serialized_start = 73
    _WORKFLOWTASKCOMPLETEDMETADATA._serialized_end = 154
# @@protoc_insertion_point(module_scope)