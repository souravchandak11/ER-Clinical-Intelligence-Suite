$env:DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/clinical_suite"
npx prisma generate
if ($LASTEXITCODE -eq 0) {
    Write-Host "Prisma client generated successfully!" -ForegroundColor Green
} else {
    Write-Host "Prisma generation failed" -ForegroundColor Red
}
