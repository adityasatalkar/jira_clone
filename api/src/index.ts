import 'module-alias/register';
import 'dotenv/config';
import 'reflect-metadata';
import express from 'express';
import cors from 'cors';

import createDatabaseConnection from 'database/createConnection';
import { addRespondToResponse } from 'middleware/response';
import { authenticateUser } from 'middleware/authentication';
import { handleError } from 'middleware/errors';
import { RouteNotFoundError } from 'errors';

import { attachPublicRoutes, attachPrivateRoutes } from './routes';

const establishDatabaseConnection = async (): Promise<void> => {
  await createDatabaseConnection();
  console.log('Database connection established.');
};

const initializeExpress = (): void => {
  const app = express();
  const port = Number(process.env.PORT) || 3000;

  app.use(cors());
  app.use(express.json());
  app.use(express.urlencoded());

  app.use(addRespondToResponse);

  attachPublicRoutes(app);

  app.use('/', authenticateUser);

  attachPrivateRoutes(app);

  app.use((req, _res, next) => next(new RouteNotFoundError(req.originalUrl)));
  app.use(handleError);

  app.listen(port, () => {
    console.log(`API is running on http://localhost:${port}`);
  });
};

const initializeApp = async (): Promise<void> => {
  try {
    await establishDatabaseConnection();
    initializeExpress();
  } catch (error) {
    console.error('Failed to start API: unable to connect to Postgres.');
    console.error(error);
    process.exit(1);
  }
};

initializeApp();
