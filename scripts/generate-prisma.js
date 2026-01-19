// Script to generate Prisma client
require('dotenv').config();
const { execSync } = require('child_process');

console.log('DATABASE_URL:', process.env.DATABASE_URL ? 'Set' : 'Not set');

try {
    execSync('npx prisma generate', {
        stdio: 'inherit',
        env: {
            ...process.env,
            DATABASE_URL: process.env.DATABASE_URL || 'postgresql://postgres:postgres@localhost:5432/clinical_suite'
        }
    });
    console.log('✅ Prisma client generated successfully!');
} catch (error) {
    console.error('❌ Prisma generation failed:', error.message);
    process.exit(1);
}
