from __future__ import annotations

from contextlib import contextmanager
from datetime import timedelta
from enum import Enum
from typing import Iterator, cast
from unittest.mock import patch

import pytest

import temporalio.api.errordetails.v1
import temporalio.worker
from temporalio import activity, workflow
from temporalio.client import (
    Client,
    RPCError,
    WorkflowHandle,
    WorkflowUpdateStage,
)
from temporalio.common import (
    WorkflowIDConflictPolicy,
)
from tests.helpers import (
    new_worker,
)


@activity.defn
async def activity_called_by_update() -> None:
    pass


@workflow.defn
class WorkflowForUpdateWithStartTest:
    def __init__(self) -> None:
        self.update_finished = False
        self.update_may_exit = False
        self.may_exit = False

    @workflow.run
    async def run(self) -> str:
        await workflow.wait_condition(lambda: self.update_finished and self.may_exit)
        return "workflow-result"

    @workflow.update
    def my_non_blocking_update(self) -> str:
        self.update_finished = True
        return "update-result"

    @workflow.update
    async def my_blocking_update(self) -> str:
        await workflow.execute_activity(
            activity_called_by_update, start_to_close_timeout=timedelta(seconds=10)
        )
        self.update_finished = True
        return "update-result"

    @workflow.signal
    async def done(self):
        self.may_exit = True


class ExpectErrorWhenWorkflowExists(Enum):
    YES = "yes"
    NO = "no"


class ExpectUpdateResultInResponse(Enum):
    YES = "yes"
    NO = "no"


class UpdateHandlerType(Enum):
    NON_BLOCKING = "non-blocking"
    BLOCKING = "blocking"


class TestUpdateWithStart:
    client: Client
    workflow_id: str
    task_queue: str
    update_id = "test-uws-up-id"

    @pytest.mark.parametrize(
        "wait_for_stage",
        [WorkflowUpdateStage.ACCEPTED, WorkflowUpdateStage.COMPLETED],
    )
    async def test_non_blocking_update_with_must_create_workflow_semantics(
        self, client: Client, wait_for_stage: WorkflowUpdateStage
    ):
        await self._do_test(
            client,
            f"test-uws-nb-mc-wf-id-{wait_for_stage.name}",
            UpdateHandlerType.NON_BLOCKING,
            wait_for_stage,
            WorkflowIDConflictPolicy.FAIL,
            ExpectUpdateResultInResponse.YES,
            ExpectErrorWhenWorkflowExists.YES,
        )

    @pytest.mark.parametrize(
        "wait_for_stage",
        [WorkflowUpdateStage.ACCEPTED, WorkflowUpdateStage.COMPLETED],
    )
    async def test_non_blocking_update_with_get_or_create_workflow_semantics(
        self, client: Client, wait_for_stage: WorkflowUpdateStage
    ):
        await self._do_test(
            client,
            f"test-uws-nb-goc-wf-id-{wait_for_stage.name}",
            UpdateHandlerType.NON_BLOCKING,
            wait_for_stage,
            WorkflowIDConflictPolicy.USE_EXISTING,
            ExpectUpdateResultInResponse.YES,
            ExpectErrorWhenWorkflowExists.NO,
        )

    @pytest.mark.parametrize(
        "wait_for_stage",
        [WorkflowUpdateStage.ACCEPTED, WorkflowUpdateStage.COMPLETED],
    )
    async def test_blocking_update_with_get_or_create_workflow_semantics(
        self, client: Client, wait_for_stage: WorkflowUpdateStage
    ):
        await self._do_test(
            client,
            f"test-uws-b-goc-wf-id-{wait_for_stage.name}",
            UpdateHandlerType.BLOCKING,
            wait_for_stage,
            WorkflowIDConflictPolicy.USE_EXISTING,
            {
                WorkflowUpdateStage.ACCEPTED: ExpectUpdateResultInResponse.NO,
                WorkflowUpdateStage.COMPLETED: ExpectUpdateResultInResponse.YES,
            }[wait_for_stage],
            ExpectErrorWhenWorkflowExists.NO,
        )

    async def _do_test(
        self,
        client: Client,
        workflow_id: str,
        update_handler_type: UpdateHandlerType,
        wait_for_stage: WorkflowUpdateStage,
        id_conflict_policy: WorkflowIDConflictPolicy,
        expect_update_result_in_response: ExpectUpdateResultInResponse,
        expect_error_when_workflow_exists: ExpectErrorWhenWorkflowExists,
    ):
        await self._do_execute_update_test(
            client,
            workflow_id + "-execute-update",
            update_handler_type,
            id_conflict_policy,
            expect_error_when_workflow_exists,
        )
        await self._do_start_update_test(
            client,
            workflow_id + "-start-update",
            update_handler_type,
            wait_for_stage,
            id_conflict_policy,
            expect_update_result_in_response,
        )

    async def _do_execute_update_test(
        self,
        client: Client,
        workflow_id: str,
        update_handler_type: UpdateHandlerType,
        id_conflict_policy: WorkflowIDConflictPolicy,
        expect_error_when_workflow_exists: ExpectErrorWhenWorkflowExists,
    ):
        update_handler = (
            WorkflowForUpdateWithStartTest.my_blocking_update
            if update_handler_type == UpdateHandlerType.BLOCKING
            else WorkflowForUpdateWithStartTest.my_non_blocking_update
        )
        async with new_worker(
            client,
            WorkflowForUpdateWithStartTest,
            activities=[activity_called_by_update],
        ) as worker:
            self.client = client
            self.workflow_id = workflow_id
            self.task_queue = worker.task_queue

            # First UWS succeeds
            with_start_1 = client.with_start_workflow(
                WorkflowForUpdateWithStartTest.run,
                id=self.workflow_id,
                task_queue=self.task_queue,
                id_conflict_policy=id_conflict_policy,
            )

            assert await with_start_1.execute_update(update_handler) == "update-result"

            # Whether a repeat UWS succeeds depends on the workflow ID conflict policy
            with_start_2 = client.with_start_workflow(
                WorkflowForUpdateWithStartTest.run,
                id=self.workflow_id,
                task_queue=self.task_queue,
                id_conflict_policy=id_conflict_policy,
            )
            if expect_error_when_workflow_exists == ExpectErrorWhenWorkflowExists.NO:
                assert (
                    await with_start_2.execute_update(update_handler) == "update-result"
                )
            else:
                with pytest.raises(RPCError) as e:
                    await with_start_2.execute_update(update_handler)
                assert e.value.grpc_status.details[0].Is(
                    temporalio.api.errordetails.v1.MultiOperationExecutionFailure.DESCRIPTOR
                )

            # The workflow is still running; finish it.

            # TODO: add get_workflow_handle method to WithStartWorkflowHandle? That means making it
            # into a concrete class; perhaps use an Updateable interface to share code with
            # WorkflowHandle.
            wf_handle = cast(
                WorkflowHandle[WorkflowForUpdateWithStartTest, str], with_start_1
            )
            await wf_handle.signal(WorkflowForUpdateWithStartTest.done)
            assert await wf_handle.result() == "workflow-result"

    async def _do_start_update_test(
        self,
        client: Client,
        workflow_id: str,
        update_handler_type: UpdateHandlerType,
        wait_for_stage: WorkflowUpdateStage,
        id_conflict_policy: WorkflowIDConflictPolicy,
        expect_update_result_in_response: ExpectUpdateResultInResponse,
    ):
        update_handler = (
            WorkflowForUpdateWithStartTest.my_blocking_update
            if update_handler_type == UpdateHandlerType.BLOCKING
            else WorkflowForUpdateWithStartTest.my_non_blocking_update
        )
        async with new_worker(
            client,
            WorkflowForUpdateWithStartTest,
            activities=[activity_called_by_update],
        ) as worker:
            self.client = client
            self.workflow_id = workflow_id
            self.task_queue = worker.task_queue

            with_start = client.with_start_workflow(
                WorkflowForUpdateWithStartTest.run,
                id=self.workflow_id,
                task_queue=self.task_queue,
                id_conflict_policy=id_conflict_policy,
            )

            update_handle = await with_start.start_update(
                update_handler, wait_for_stage=wait_for_stage
            )
            with self.assert_network_call(
                expect_update_result_in_response == ExpectUpdateResultInResponse.NO
            ):
                assert await update_handle.result() == "update-result"

    @contextmanager
    def assert_network_call(
        self,
        expect_network_call: bool,
    ) -> Iterator[None]:
        with patch.object(
            self.client.workflow_service,
            "poll_workflow_execution_update",
            wraps=self.client.workflow_service.poll_workflow_execution_update,
        ) as _wrapped_poll:
            yield
            # TODO: cache known outcomes locally
            # assert _wrapped_poll.called == expect_network_call
