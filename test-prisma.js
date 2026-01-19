try {
    const { PrismaClient } = require('@prisma/client');
    const prisma = new PrismaClient();
    console.log('PrismaClient found');
} catch (e) {
    console.error('PrismaClient NOT found:', e.message);
}
