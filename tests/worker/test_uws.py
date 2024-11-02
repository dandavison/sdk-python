from __future__ import annotations

from contextlib import contextmanager
from datetime import timedelta
from enum import Enum
from typing import Iterator
from unittest.mock import patch

import pytest

import temporalio.api.errordetails.v1
import temporalio.worker
from temporalio import activity, workflow
from temporalio.client import (
    Client,
    RPCError,
    WorkflowUpdateFailedError,
    WorkflowUpdateStage,
)
from temporalio.common import (
    WorkflowIDConflictPolicy,
)
from temporalio.exceptions import ApplicationError
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
        self.received_done_signal = False

    @workflow.run
    async def run(self, i: int) -> str:
        await workflow.wait_condition(lambda: self.received_done_signal)
        return f"workflow-result-{i}"

    @workflow.update
    def my_non_blocking_update(self, i: int) -> str:
        if i < 0:
            raise ApplicationError("Workflow deliberate failed update")
        return f"update-result-{i}"

    @workflow.update
    async def my_blocking_update(self, i: int) -> str:
        if i < 0:
            raise ApplicationError("Workflow deliberate failed update")
        await workflow.execute_activity(
            activity_called_by_update, start_to_close_timeout=timedelta(seconds=10)
        )
        return f"update-result-{i}"

    @workflow.signal
    async def done(self):
        self.received_done_signal = True


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

            with_start_handle_1 = client.with_start_workflow(
                WorkflowForUpdateWithStartTest.run,
                1,
                id=self.workflow_id,
                task_queue=self.task_queue,
                id_conflict_policy=id_conflict_policy,
            )

            # First UWS succeeds
            assert (
                await with_start_handle_1.execute_update(update_handler, 1)
                == "update-result-1"
            )
            assert (
                await with_start_handle_1.get_workflow_handle()
            ).first_execution_run_id is not None

            # Whether a repeat UWS succeeds depends on the workflow ID conflict policy
            with_start_handle_2 = client.with_start_workflow(
                WorkflowForUpdateWithStartTest.run,
                2,
                id=self.workflow_id,
                task_queue=self.task_queue,
                id_conflict_policy=id_conflict_policy,
            )

            if expect_error_when_workflow_exists == ExpectErrorWhenWorkflowExists.NO:
                assert (
                    await with_start_handle_2.execute_update(update_handler, 21)
                    == "update-result-21"
                )
                assert (
                    await with_start_handle_2.get_workflow_handle()
                ).first_execution_run_id is not None
            else:
                with pytest.raises(RPCError) as e:
                    await with_start_handle_2.execute_update(update_handler, 21)
                assert e.value.grpc_status.details[0].Is(
                    temporalio.api.errordetails.v1.MultiOperationExecutionFailure.DESCRIPTOR
                )
                assert (
                    await with_start_handle_1.get_workflow_handle()
                ).first_execution_run_id is not None

            # The workflow is still running; finish it.

            wf_handle_1 = await with_start_handle_1.get_workflow_handle()
            await wf_handle_1.signal(WorkflowForUpdateWithStartTest.done)
            assert await wf_handle_1.result() == "workflow-result-1"

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

            with_start_handle_1 = client.with_start_workflow(
                WorkflowForUpdateWithStartTest.run,
                1,
                id=self.workflow_id,
                task_queue=self.task_queue,
                id_conflict_policy=id_conflict_policy,
            )

            update_handle_1 = await with_start_handle_1.start_update(
                update_handler, 1, wait_for_stage=wait_for_stage
            )
            with self.assert_network_call(
                expect_update_result_in_response == ExpectUpdateResultInResponse.NO
            ):
                assert await update_handle_1.result() == "update-result-1"

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


async def test_update_with_start_sets_first_execution_run_id(client: Client):
    async with new_worker(
        client,
        WorkflowForUpdateWithStartTest,
        activities=[activity_called_by_update],
    ) as worker:

        def make_with_start_handle(workflow_id: str):
            return client.with_start_workflow(
                WorkflowForUpdateWithStartTest.run,
                0,
                id=workflow_id,
                id_conflict_policy=WorkflowIDConflictPolicy.FAIL,
                task_queue=worker.task_queue,
            )

        # conflict policy is FAIL
        # First UWS succeeds and sets the first execution run ID
        with_start_handle_1 = make_with_start_handle("wid-1")
        update_handle_1 = await with_start_handle_1.start_update(
            WorkflowForUpdateWithStartTest.my_non_blocking_update,
            1,
            wait_for_stage=WorkflowUpdateStage.COMPLETED,
        )
        assert (
            await with_start_handle_1.get_workflow_handle()
        ).first_execution_run_id is not None
        assert await update_handle_1.result() == "update-result-1"

        # Second UWS start fails because the workflow already exists
        # first execution run ID is not set on the second UWS handle
        with_start_handle_2 = make_with_start_handle("wid-1")
        with pytest.raises(RPCError) as e:
            await with_start_handle_2.start_update(
                WorkflowForUpdateWithStartTest.my_non_blocking_update,
                2,
                wait_for_stage=WorkflowUpdateStage.COMPLETED,
            )
            assert e.value.grpc_status.details[0].Is(
                temporalio.api.errordetails.v1.MultiOperationExecutionFailure.DESCRIPTOR
            )

        # Third UWS start succeeds, but the update fails
        with_start_handle_3 = make_with_start_handle("wid-2")
        update_handle_3 = await with_start_handle_3.start_update(
            WorkflowForUpdateWithStartTest.my_non_blocking_update,
            -1,
            wait_for_stage=WorkflowUpdateStage.COMPLETED,
        )
        assert (
            await with_start_handle_3.get_workflow_handle()
        ).first_execution_run_id is not None
        with pytest.raises(WorkflowUpdateFailedError) as e:
            await update_handle_3.result()

        # Despite the update failure, the first execution run ID is set on the with_start_handle,
        # and the handle can be used to obtain the workflow result.
        assert (
            await with_start_handle_3.get_workflow_handle()
        ).first_execution_run_id is not None
        wf_handle_3 = await with_start_handle_3.get_workflow_handle()
        await wf_handle_3.signal(WorkflowForUpdateWithStartTest.done)
        assert await wf_handle_3.result() == "workflow-result-0"

        # Fourth UWS is same as third, but we use execute_update instead of start_update.
        with_start_handle_4 = make_with_start_handle("wid-3")
        with pytest.raises(WorkflowUpdateFailedError) as e:
            await with_start_handle_4.execute_update(
                WorkflowForUpdateWithStartTest.my_non_blocking_update, -1
            )
        assert (
            await with_start_handle_4.get_workflow_handle()
        ).first_execution_run_id is not None
