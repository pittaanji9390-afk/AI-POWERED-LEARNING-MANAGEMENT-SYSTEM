# Enterprise Disaster Recovery & Continuous Backup Runbook

## 1. Recovery Objectives
- **RPO (Recovery Point Objective)**: `< 5 minutes`
- **RTO (Recovery Time Objective)**: `< 30 minutes`

---

## 2. Continuous PostgreSQL WAL Archiving
Database transactions are streamed to encrypted S3 object storage in real-time via PostgreSQL Write-Ahead Logging (WAL).

```bash
# PostgreSQL WAL Configuration (postgresql.conf)
wal_level = replica
archive_mode = on
archive_command = 'pgbackrest --stanza=ailms_db archive-push %p'
archive_timeout = 300
```

---

## 3. Full & Incremental Snapshot Schedule
1. **Daily Full Backup**: Executed at 01:00 UTC with AES-256 encryption. Retained for 90 days.
2. **Hourly Differential Backup**: Executed every hour on the hour. Retained for 14 days.
3. **Point-In-Time Recovery (PITR)**: Allows restoring database state to any specific timestamp within the last 14 days.

---

## 4. Disaster Recovery Procedure (Failover Runbook)
1. **Detect Outage**: Health checks alert on 3 consecutive failed probes to `/api/v1/health`.
2. **Promote Standby Database**:
   ```bash
   pgbackrest --stanza=ailms_db --type=standby restore
   pg_ctl promote -D /var/lib/postgresql/data
   ```
3. **Update Database Connection Pool**: Shift traffic to promoted primary endpoint.
4. **Flush Redis L2 Cache**: Prevent stale cache reads from pre-failover transactions.
5. **Verify API Integrity**: Run automated health validation suite:
   ```bash
   curl -f http://localhost:8080/api/v1/health
   ```
