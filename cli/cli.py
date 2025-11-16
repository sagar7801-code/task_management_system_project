# Reference from: https://click.palletsprojects.com/en/stable/

import click
import requests
import sys
from datetime import datetime

API_URL_DEFAULT = "http://127.0.0.1:8000"


def parse_date(d):
    if d is None:
        return None
    try:
        return datetime.strptime(d, "%Y-%m-%d").date()
    except ValueError:
        raise click.BadParameter("Date must be in YYYY-MM-DD format")


@click.group()
@click.option("--api-url", default=API_URL_DEFAULT, help="Base URL for the API")
@click.pass_context
def cli(ctx, api_url):
    ctx.ensure_object(dict)
    ctx.obj["api_url"] = api_url.rstrip("/")


@cli.command()
@click.argument("title")
@click.option("--desc", default="", help="Description")
@click.option(
    "--priority", default="medium", type=click.Choice(["low", "medium", "high"])
)
@click.option("--due", default=None, help="Due date YYYY-MM-DD")
@click.pass_context
def create(ctx, title, desc, priority, due):
    """Create a new task"""
    due_parsed = None
    if due:
        try:
            due_parsed = parse_date(due)
        except click.BadParameter as e:
            click.echo(f"Error: {e}")
            sys.exit(1)

    payload = {
        "title": title,
        "description": desc or None,
        "priority": priority,
        "due_date": due_parsed.isoformat() if due_parsed else None,
    }
    url = f"{ctx.obj['api_url']}/tasks"
    r = requests.post(url, json=payload)
    if r.status_code == 201:
        click.echo("Task created:")
        click.echo(r.json())
    else:
        click.echo(f"Error {r.status_code}: {r.text}")


@cli.command()
@click.option("--status", type=click.Choice(["open", "completed"]), default=None)
@click.option("--priority", type=click.Choice(["low", "medium", "high"]), default=None)
@click.option("--due-before", default=None, help="YYYY-MM-DD")
@click.option("--due-after", default=None, help="YYYY-MM-DD")
@click.pass_context
def list(ctx, status, priority, due_before, due_after):
    """List tasks with optional filters"""
    params = {}
    if status:
        params["status"] = status
    if priority:
        params["priority"] = priority
    if due_before:
        try:
            params["due_before"] = parse_date(due_before).isoformat()
        except click.BadParameter as e:
            click.echo(f"Error: {e}")
            sys.exit(1)
    if due_after:
        try:
            params["due_after"] = parse_date(due_after).isoformat()
        except click.BadParameter as e:
            click.echo(f"Error: {e}")
            sys.exit(1)

    url = f"{ctx.obj['api_url']}/tasks"
    r = requests.get(url, params=params)
    if r.status_code == 200:
        tasks = r.json()
        if not tasks:
            click.echo("No tasks found.")
            return
        for t in tasks:
            click.echo(
                f"[{t['id']}] {t['title']} | {t['status']} | {t['priority']} | due: {t.get('due_date')}"
            )
    else:
        click.echo(f"Error {r.status_code}: {r.text}")


@cli.command()
@click.argument("task_id", type=int)
@click.pass_context
def get(ctx, task_id):
    """Get task by id"""
    url = f"{ctx.obj['api_url']}/tasks/{task_id}"
    r = requests.get(url)
    if r.status_code == 200:
        click.echo(r.json())
    else:
        click.echo(f"Error {r.status_code}: {r.text}")


@cli.command()
@click.argument("task_id", type=int)
@click.option("--title", default=None)
@click.option("--desc", default=None)
@click.option("--priority", type=click.Choice(["low", "medium", "high"]), default=None)
@click.option("--due", default=None)
@click.option("--status", type=click.Choice(["open", "completed"]), default=None)
@click.pass_context
def update(ctx, task_id, title, desc, priority, due, status):
    """Update a task"""
    payload = {}
    if title is not None:
        payload["title"] = title
    if desc is not None:
        payload["description"] = desc
    if priority is not None:
        payload["priority"] = priority
    if due is not None:
        try:
            payload["due_date"] = parse_date(due).isoformat()
        except click.BadParameter as e:
            click.echo(f"Error: {e}")
            sys.exit(1)
    if status is not None:
        payload["status"] = status

    if not payload:
        click.echo("No fields to update.")
        return

    url = f"{ctx.obj['api_url']}/tasks/{task_id}"
    r = requests.put(url, json=payload)
    if r.status_code == 200:
        click.echo("Updated:")
        click.echo(r.json())
    else:
        click.echo(f"Error {r.status_code}: {r.text}")


@cli.command()
@click.argument("task_id", type=int)
@click.pass_context
def complete(ctx, task_id):
    """Mark task as completed"""
    url = f"{ctx.obj['api_url']}/tasks/{task_id}/status"
    r = requests.patch(url, params={"status": "completed"})
    if r.status_code == 200:
        click.echo("Task marked completed")
    else:
        click.echo(f"Error {r.status_code}: {r.text}")


@cli.command()
@click.argument("task_id", type=int)
@click.pass_context
def reopen(ctx, task_id):
    """Mark task as open"""
    url = f"{ctx.obj['api_url']}/tasks/{task_id}/status"
    r = requests.patch(url, params={"status": "open"})
    if r.status_code == 200:
        click.echo("Task reopened (status=open)")
    else:
        click.echo(f"Error {r.status_code}: {r.text}")


@cli.command()
@click.argument("task_id", type=int)
@click.pass_context
def delete(ctx, task_id):
    """Delete a task"""
    url = f"{ctx.obj['api_url']}/tasks/{task_id}"
    r = requests.delete(url)
    if r.status_code == 204:
        click.echo("Deleted.")
    else:
        click.echo(f"Error {r.status_code}: {r.text}")


if __name__ == "__main__":
    cli()
