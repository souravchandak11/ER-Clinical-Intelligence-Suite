let PrismaClient: any;
try {
    PrismaClient = require("@prisma/client").PrismaClient;
} catch (e) {
    console.warn("Prisma client not found, using fallbacks");
}

const createMockPrisma = () => ({
    user: {
        findFirst: async () => null,
        findMany: async () => [],
    },
    $connect: async () => { },
    $disconnect: async () => { },
});

const createPrismaClient = () => {
    if (!PrismaClient) return createMockPrisma();
    try {
        return new PrismaClient({
            log: process.env.NODE_ENV === "development" ? ["query", "error", "warn"] : ["error"],
        });
    } catch (e) {
        console.warn("Failed to instantiate PrismaClient:", e);
        return createMockPrisma();
    }
};

const globalForPrisma = globalThis as unknown as {
    prisma: any;
};

export const db = globalForPrisma.prisma ?? createPrismaClient();

if (process.env.NODE_ENV !== "production") globalForPrisma.prisma = db;

