# Backup & Disaster Recovery Architecture

## Recovery Objectives
- **RPO (Recovery Point Objective)**: < 5 minutes (via PostgreSQL Continuous WAL archiving).
- **RTO (Recovery Time Objective)**: < 30 minutes.

## Backup Routine
1. Daily full database snapshots with AES-256 encryption.
2. Point-in-time recovery (PITR) enabled via pgBackRest / S3 object storage.
