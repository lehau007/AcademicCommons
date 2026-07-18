import json
from asyncio import run
from pathlib import Path
from typing import Annotated

import typer

from app.config import get_settings
from app.db.session import AsyncSessionLocal
from app.llm.cost_report import aggregate_records, load_records, render_markdown
from app.main import create_app
from app.services.seed import DEFAULT_SEED_PASSWORD, SeedResult, seed_database

cli = typer.Typer(help="Backend maintenance commands.")


@cli.command()
def export_openapi(output: Annotated[Path | None, typer.Option("--output", "-o")] = None) -> None:
    """Export the generated OpenAPI schema as JSON-compatible YAML."""
    rendered = json.dumps(create_app().openapi(), indent=2) + "\n"
    if output is None:
        print(rendered, end="")
        return
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(rendered, encoding="utf-8")
    typer.echo(f"OpenAPI schema written to {output}")


@cli.command()
def seed() -> None:
    """Load development seed data into the database."""
    result = run(_seed())
    typer.echo(
        "Seed complete: "
        f"{result.courses} courses, {result.users} users, "
        f"{result.reviewer_assignments} reviewer assignments."
    )
    typer.echo(f"Seed users use the default password {DEFAULT_SEED_PASSWORD!r}; change it outside local dev.", err=True)


async def _seed() -> SeedResult:
    async with AsyncSessionLocal() as session:
        return await seed_database(session)


@cli.command()
def optimizer_report(
    log: Annotated[Path | None, typer.Option("--log", "-l", help="Path to the optimizer JSONL log.")] = None,
    group_by: Annotated[str, typer.Option("--group-by", "-g")] = "flow,provider",
    as_json: Annotated[bool, typer.Option("--json", help="Emit raw aggregates as JSON.")] = False,
) -> None:
    """Aggregate optimizer cost/usage from the JSONL log for cost reporting."""
    log_path = log or Path(get_settings().llm_optimizer_log_path)
    records = load_records(log_path)
    dimensions = tuple(d.strip() for d in group_by.split(",") if d.strip())
    report = aggregate_records(records, group_by=dimensions)
    if not records:
        typer.echo(f"No optimizer log records found at {log_path}", err=True)
    if as_json:
        payload = {
            "group_by": list(report.group_by),
            "groups": [
                {**dict(zip(report.group_by, stat.key, strict=False)),
                 "calls": stat.calls, "cost_usd": stat.cost_usd,
                 "tokens_in": stat.tokens_in, "tokens_out": stat.tokens_out,
                 "cache_hit_rate": stat.cache_hit_rate}
                for stat in report.groups
            ],
            "total": {"calls": report.total.calls, "cost_usd": report.total.cost_usd,
                      "tokens_in": report.total.tokens_in, "tokens_out": report.total.tokens_out,
                      "cache_hit_rate": report.total.cache_hit_rate},
        }
        typer.echo(json.dumps(payload, indent=2))
    else:
        typer.echo(render_markdown(report))


@cli.command()
def reindex_embeddings(
    batch_size: Annotated[int, typer.Option("--batch-size", "-b")] = 50,
) -> None:
    """Re-encode all chunk/summary embeddings with the active embedding tier."""
    chunks, summaries = run(_reindex(batch_size))
    typer.echo(f"Reindexed {chunks} chunks and {summaries} summaries.")


async def _reindex(batch_size: int) -> tuple[int, int]:
    from app.services.reindex_service import reindex_embeddings as run_reindex
    from app.services.retrieval_service import build_embedding_service

    async with AsyncSessionLocal() as session:
        result = await run_reindex(
            session, build_embedding_service(get_settings()), batch_size=batch_size
        )
        await session.commit()
        return result


if __name__ == "__main__":
    cli()
