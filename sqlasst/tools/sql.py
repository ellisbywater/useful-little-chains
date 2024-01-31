import sqlite3
from pydantic.v1 import BaseModel
from typing import List
from langchain.tools import Tool

conn = sqlite3.connect('db.sqlite')

def list_tables():
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    rows = c.fetchall()
    return "\n".join(row[0] for row in rows) if rows is not None else "No tables found"

def run_sqlite_query(query):
    c = conn.cursor()
    try:
        c.execute(query)  # Fix: Added closing parenthesis
        return c.fetchall()
    except sqlite3.OperationalError as e:
        return str(e)

class RunQueryArgsSchema(BaseModel):
    query: str
    p

run_query_tool = Tool.from_function(
    name="run_sqlite_query",
    description="Run a query on the sqlite database",
    func=run_sqlite_query
)

def describe_table(table_names):
    c = conn.cursor()
    tables = ', '.join("'" + table + "'" for table in table_names)
    rows = c.execute(f"SELECT sql FROM sqlite_master WHERE type='table' AND name IN ({tables});")

class DescribeTablesArgsSchema(BaseModel):
    table_names: List[str]


describe_table_tool = Tool.from_function(
    name="describe_tables",
    description="Given a list of table names, returns the schema for each table",
    func=describe_table,
    args_schema=DescribeTablesArgsSchema,
)
