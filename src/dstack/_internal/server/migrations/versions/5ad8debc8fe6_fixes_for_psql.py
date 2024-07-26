"""Fixes for psql

Revision ID: 5ad8debc8fe6
Revises: 98cd9c8b5927
Create Date: 2024-07-04 17:26:01.937112

"""

import sqlalchemy as sa
from alembic import op
from alembic_postgresql_enum import TableReference
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "5ad8debc8fe6"
down_revision = "98cd9c8b5927"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    sa.Enum(
        "PENDING",
        "SUBMITTED",
        "PROVISIONING",
        "RUNNING",
        "TERMINATING",
        "TERMINATED",
        "FAILED",
        "DONE",
        name="runstatus",
    ).create(op.get_bind())
    with op.batch_alter_table("backends", schema=None) as batch_op:
        batch_op.alter_column(
            "config",
            existing_type=sa.VARCHAR(length=2000),
            type_=sa.String(length=20000),
            existing_nullable=False,
        )
        batch_op.alter_column(
            "auth",
            existing_type=sa.VARCHAR(length=2000),
            type_=sa.String(length=20000),
            existing_nullable=False,
        )

    with op.batch_alter_table("jobs", schema=None) as batch_op:
        batch_op.alter_column(
            "runner_timestamp",
            existing_type=sa.INTEGER(),
            type_=sa.BigInteger(),
            existing_nullable=True,
        )

    with op.batch_alter_table("runs", schema=None) as batch_op:
        batch_op.alter_column(
            "status",
            existing_type=postgresql.ENUM(
                "PENDING",
                "SUBMITTED",
                "PROVISIONING",
                "RUNNING",
                "TERMINATING",
                "TERMINATED",
                "ABORTED",
                "FAILED",
                "DONE",
                name="jobstatus",
            ),
            type_=sa.Enum(
                "PENDING",
                "SUBMITTED",
                "PROVISIONING",
                "RUNNING",
                "TERMINATING",
                "TERMINATED",
                "FAILED",
                "DONE",
                name="runstatus",
            ),
            existing_nullable=False,
            postgresql_using="status::VARCHAR::runstatus",
        )

    sa.Enum(
        "NO_INSTANCE_MATCHING_REQUIREMENTS",
        "FAILED_TO_START_DUE_TO_NO_CAPACITY",
        "INTERRUPTED_BY_NO_CAPACITY",
        "INSTANCE_TERMINATED",
        "CONTAINER_EXITED_WITH_ERROR",
        "PORTS_BINDING_FAILED",
        name="joberrorcode",
    ).drop(op.get_bind())
    op.sync_enum_values(
        "public",
        "backendtype",
        [
            "AWS",
            "AZURE",
            "CUDO",
            "DATACRUNCH",
            "DSTACK",
            "GCP",
            "KUBERNETES",
            "LAMBDA",
            "LOCAL",
            "REMOTE",
            "NEBIUS",
            "OCI",
            "RUNPOD",
            "TENSORDOCK",
            "VASTAI",
        ],
        [
            TableReference(table_schema="public", table_name="instances", column_name="backend"),
            TableReference(table_schema="public", table_name="backends", column_name="type"),
        ],
        enum_values_to_rename=[],
    )
    op.sync_enum_values(
        "public",
        "repotype",
        ["REMOTE", "LOCAL", "VIRTUAL"],
        [TableReference(table_schema="public", table_name="repos", column_name="type")],
        enum_values_to_rename=[],
    )
    op.sync_enum_values(
        "public",
        "jobstatus",
        [
            "SUBMITTED",
            "PROVISIONING",
            "PULLING",
            "RUNNING",
            "TERMINATING",
            "TERMINATED",
            "ABORTED",
            "FAILED",
            "DONE",
        ],
        [TableReference(table_schema="public", table_name="jobs", column_name="status")],
        enum_values_to_rename=[],
    )
    op.sync_enum_values(
        "public",
        "jobterminationreason",
        [
            "FAILED_TO_START_DUE_TO_NO_CAPACITY",
            "INTERRUPTED_BY_NO_CAPACITY",
            "WAITING_INSTANCE_LIMIT_EXCEEDED",
            "WAITING_RUNNER_LIMIT_EXCEEDED",
            "TERMINATED_BY_USER",
            "VOLUME_ERROR",
            "GATEWAY_ERROR",
            "SCALED_DOWN",
            "DONE_BY_RUNNER",
            "ABORTED_BY_USER",
            "TERMINATED_BY_SERVER",
            "CONTAINER_EXITED_WITH_ERROR",
            "PORTS_BINDING_FAILED",
            "CREATING_CONTAINER_ERROR",
            "EXECUTOR_ERROR",
        ],
        [
            TableReference(
                table_schema="public", table_name="jobs", column_name="termination_reason"
            )
        ],
        enum_values_to_rename=[],
    )
    op.sync_enum_values(
        "public",
        "instancestatus",
        ["PENDING", "PROVISIONING", "IDLE", "BUSY", "TERMINATING", "TERMINATED"],
        [TableReference(table_schema="public", table_name="instances", column_name="status")],
        enum_values_to_rename=[],
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.sync_enum_values(
        "public",
        "instancestatus",
        [
            "PENDING",
            "CREATING",
            "STARTING",
            "READY",
            "BUSY",
            "TERMINATING",
            "TERMINATED",
            "FAILED",
        ],
        [TableReference(table_schema="public", table_name="instances", column_name="status")],
        enum_values_to_rename=[],
    )
    op.sync_enum_values(
        "public",
        "jobterminationreason",
        [
            "FAILED_TO_START_DUE_TO_NO_CAPACITY",
            "INTERRUPTED_BY_NO_CAPACITY",
            "WAITING_RUNNER_LIMIT_EXCEEDED",
            "TERMINATED_BY_USER",
            "GATEWAY_ERROR",
            "SCALED_DOWN",
            "DONE_BY_RUNNER",
            "ABORTED_BY_USER",
            "TERMINATED_BY_SERVER",
            "CONTAINER_EXITED_WITH_ERROR",
            "PORTS_BINDING_FAILED",
        ],
        [
            TableReference(
                table_schema="public", table_name="jobs", column_name="termination_reason"
            )
        ],
        enum_values_to_rename=[],
    )
    op.sync_enum_values(
        "public",
        "jobstatus",
        [
            "PENDING",
            "SUBMITTED",
            "PROVISIONING",
            "RUNNING",
            "TERMINATING",
            "TERMINATED",
            "ABORTED",
            "FAILED",
            "DONE",
        ],
        [TableReference(table_schema="public", table_name="jobs", column_name="status")],
        enum_values_to_rename=[],
    )
    op.sync_enum_values(
        "public",
        "repotype",
        ["REMOTE", "LOCAL"],
        [TableReference(table_schema="public", table_name="repos", column_name="type")],
        enum_values_to_rename=[],
    )
    op.sync_enum_values(
        "public",
        "backendtype",
        ["AWS", "AZURE", "GCP", "LAMBDA"],
        [
            TableReference(table_schema="public", table_name="instances", column_name="backend"),
            TableReference(table_schema="public", table_name="backends", column_name="type"),
        ],
        enum_values_to_rename=[],
    )
    sa.Enum(
        "NO_INSTANCE_MATCHING_REQUIREMENTS",
        "FAILED_TO_START_DUE_TO_NO_CAPACITY",
        "INTERRUPTED_BY_NO_CAPACITY",
        "INSTANCE_TERMINATED",
        "CONTAINER_EXITED_WITH_ERROR",
        "PORTS_BINDING_FAILED",
        name="joberrorcode",
    ).create(op.get_bind())
    with op.batch_alter_table("runs", schema=None) as batch_op:
        batch_op.alter_column(
            "status",
            existing_type=sa.Enum(
                "PENDING",
                "SUBMITTED",
                "PROVISIONING",
                "RUNNING",
                "TERMINATING",
                "TERMINATED",
                "FAILED",
                "DONE",
                name="runstatus",
            ),
            type_=postgresql.ENUM(
                "PENDING",
                "SUBMITTED",
                "PROVISIONING",
                "RUNNING",
                "TERMINATING",
                "TERMINATED",
                "ABORTED",
                "FAILED",
                "DONE",
                name="jobstatus",
            ),
            existing_nullable=False,
        )

    with op.batch_alter_table("jobs", schema=None) as batch_op:
        batch_op.alter_column(
            "runner_timestamp",
            existing_type=sa.BigInteger(),
            type_=sa.INTEGER(),
            existing_nullable=True,
        )

    with op.batch_alter_table("backends", schema=None) as batch_op:
        batch_op.alter_column(
            "auth",
            existing_type=sa.String(length=20000),
            type_=sa.VARCHAR(length=2000),
            existing_nullable=False,
        )
        batch_op.alter_column(
            "config",
            existing_type=sa.String(length=20000),
            type_=sa.VARCHAR(length=2000),
            existing_nullable=False,
        )

    sa.Enum(
        "PENDING",
        "SUBMITTED",
        "PROVISIONING",
        "RUNNING",
        "TERMINATING",
        "TERMINATED",
        "FAILED",
        "DONE",
        name="runstatus",
    ).drop(op.get_bind())
    # ### end Alembic commands ###