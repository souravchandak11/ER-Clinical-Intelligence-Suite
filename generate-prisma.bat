@echo off
set DATABASE_URL=postgresql://postgres:postgres@localhost:5432/clinical_suite
npx prisma generate
