"""
Read-only production schema inspection via raw SQLAlchemy.
Does NOT import Flask app, create_app, or db.
Standalone. Disposable. Do not commit.
"""
import os
import sys
import re
from sqlalchemy import create_engine, MetaData, inspect, text

DATABASE_URL = os.environ.get('DATABASE_URL', '').strip()
if not DATABASE_URL:
    print('ABORT: DATABASE_URL is not set or is empty.')
    sys.exit(1)

# Masked connection info (never print raw URL)
from urllib.parse import urlparse
parsed = urlparse(DATABASE_URL)
host = parsed.hostname or 'unknown'
database = (parsed.path or '').lstrip('/') or 'unknown'
masked_host = re.sub(r'^[^.]+', '****', host)

if parsed.scheme and parsed.scheme.startswith('postgresql'):
    dialect = 'postgresql'
else:
    dialect = parsed.scheme or 'unknown'

print('Target database:')
print(f'  dialect:  {dialect}')
print(f'  host:     {masked_host}')
print(f'  database: {database}')
print()

if dialect != 'postgresql':
    print('ABORT: dialect is not PostgreSQL. Refusing to proceed.')
    sys.exit(1)

engine = create_engine(DATABASE_URL, isolation_level='AUTOCOMMIT')
insp = inspect(engine)

# ── 1. Alembic state ──
print('=' * 60)
print('1. ALEMBIC STATE')
print('=' * 60)
alembic_exists = False
alembic_version = None
with engine.connect() as conn:
    result = conn.execute(text(
        "SELECT EXISTS (SELECT FROM information_schema.tables "
        "WHERE table_name = 'alembic_version')"
    ))
    alembic_exists = result.scalar()

    if alembic_exists:
        result = conn.execute(text("SELECT version_num FROM alembic_version"))
        row = result.fetchone()
        alembic_version = row[0] if row else None
        print(f'  alembic_version table: EXISTS')
        print(f'  version_num:           {alembic_version}')
    else:
        print('  alembic_version table: NOT FOUND')
print()

# ── 2. Table inventory ──
print('=' * 60)
print('2. TABLE INVENTORY')
print('=' * 60)
tables = insp.get_table_names()
tables.sort()
for t in tables:
    print(f'  {t}')
print()

# ── 3. Relevant table schemas ──
TARGET_TABLES = ['users', 'clients', 'links', 'orders']

print('=' * 60)
print('3. RELEVANT TABLE SCHEMAS')
print('=' * 60)
for table_name in TARGET_TABLES:
    if table_name not in tables:
        print(f'  [{table_name}] TABLE NOT FOUND')
        print()
        continue
    columns = insp.get_columns(table_name)
    print(f'  [{table_name}]')
    for col in columns:
        nullable = 'NULL' if col.get('nullable', True) else 'NOT NULL'
        default = col.get('default')
        default_str = f' default={default}' if default is not None else ''
        print(f'    {col["name"]:25s} {str(col["type"]):30s} {nullable}{default_str}')
    print()

# ── 4. Migration field checks ──
print('=' * 60)
print('4. MIGRATION FIELD CHECKS')
print('=' * 60)

# 363419dae104: links.link_type
links_cols = {c['name']: c for c in insp.get_columns('links')} if 'links' in tables else {}
if 'link_type' in links_cols:
    print('  [links.link_type] EXISTS — migration 363419dae104 applied')
else:
    print('  [links.link_type] MISSING — migration 363419dae104 NOT applied')

# 001_add_order_fields: 7 columns on orders
orders_cols = {c['name']: c for c in insp.get_columns('orders')} if 'orders' in tables else {}
expected_order_fields = [
    'stripe_session_id', 'tier', 'delivery_name',
    'delivery_line1', 'delivery_line2', 'delivery_city', 'delivery_postcode',
]
all_present = True
for field in expected_order_fields:
    if field in orders_cols:
        print(f'  [orders.{field}] EXISTS')
    else:
        print(f'  [orders.{field}] MISSING — migration 001_add_order_fields NOT fully applied')
        all_present = False

if all_present:
    print('  All expected order fields present — migration 001_add_order_fields applied')

print()

# ── 5. Final comparison ──
print('=' * 60)
print('5. FINAL COMPARISON')
print('=' * 60)

migration_0001_applied = all_present
migration_363419_applied = 'link_type' in links_cols

if alembic_version == '363419dae104' and migration_0001_applied and migration_363419_applied:
    print('  MATCHES MIGRATIONS')
    print('  Alembic version matches latest migration; all schema changes present.')
    print('  Recommendation: remove db.create_all() from app/__init__.py.')
    print('  The Alembic chain is current and production schema matches.')
elif alembic_version is None and migration_0001_applied and migration_363419_applied:
    print('  SCHEMA HAS MIGRATION CHANGES BUT ALEMBIC VERSION IS MISSING/STALE')
    print('  All migration changes exist in the schema, but alembic_version')
    print('  table is absent — likely because db.create_all() built the schema')
    print('  directly without going through Alembic.')
    print('  Recommendation: remove db.create_all(), then stamp the latest')
    print('  revision (363419dae104) to align Alembic with reality.')
elif alembic_version and not migration_0001_applied:
    print('  SCHEMA IS MISSING MIGRATION CHANGES')
    print(f'  Alembic reports {alembic_version} but orders table is missing expected fields.')
    print('  Manual review required.')
elif alembic_version and not migration_363419_applied:
    print('  SCHEMA IS MISSING MIGRATION CHANGES')
    print(f'  Alembic reports {alembic_version} but links.link_type is missing.')
    print('  Manual review required.')
else:
    print('  UNKNOWN / MANUAL REVIEW REQUIRED')
    print(f'  alembic_version: {alembic_version}')
    print(f'  migration_0001_applied: {migration_0001_applied}')
    print(f'  migration_363419_applied: {migration_363419_applied}')

print()
print('Read-only inspection complete. No data was modified.')
