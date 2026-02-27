<h1 align="center">A simplified Jira clone built with React and Flask</h1>

<div align="center">Auto formatted with Prettier, tested with Cypress 🎗</div>

<h3 align="center">
  <a href="https://jira.ivorreic.com/">Visit the live app</a> |
  <a href="https://github.com/oldboyxx/jira_clone/tree/master/client">View client</a> |
  <a href="https://github.com/oldboyxx/jira_clone/tree/master/api">View API</a>
</h3>

![Tech logos](https://i.ibb.co/DVFj8PL/tech-icons.jpg)

![App screenshot](https://i.ibb.co/W3qVvCn/jira-optimized.jpg)

## What is this and who is it for 🤷‍♀️

I do React consulting and this is a showcase product I've built in my spare time. It's a very good example of modern, real-world React codebase.

There are many showcase/example React projects out there but most of them are way too simple. I like to think that this codebase contains enough complexity to offer valuable insights to React developers of all skill levels while still being _relatively_ easy to understand.

## Features

- Proven, scalable, and easy to understand project structure
- Written in modern React, only functional components with hooks
- A variety of custom light-weight UI components such as datepicker, modal, various form elements etc
- Simple local React state management, without redux, mobx, or similar
- Custom webpack setup, without create-react-app or similar
- Client written in Babel powered JavaScript
- API written in Python (Flask + SQLAlchemy)

## Versioning and release notes

- This fork follows **Semantic Versioning** (`MAJOR.MINOR.PATCH`).
- Release notes and version history are tracked in [`CHANGELOG.md`](./CHANGELOG.md).
- Historical entries were reconstructed from git commit history because this repository does not include git version tags.

## Setting up development environment 🛠

- Install [Node.js](https://nodejs.org/) (Node 22+ supported in this repo).
- Install [PostgreSQL](https://www.postgresql.org/) (PostgreSQL 12+ recommended; tested with 14) and create a database named `jira_development`.
- `git clone https://github.com/oldboyxx/jira_clone.git`
- Create an empty `.env` file in `/api`, copy `/api/.env.example` contents into it, and fill in your database username and password.
- `npm run install-dependencies` (installs root/client npm deps and Python backend deps)
- Start PostgreSQL before running the API.
  - Example (Homebrew): `brew services start postgresql@14`
- `cd api && python3 run.py` (runs the Flask API on port `3000`)
- `cd client && npm start` in another terminal tab
- App should now be running on `http://localhost:8080/`

### Troubleshooting

- If the UI is stuck on the loading spinner, verify the API is running and healthy:
  - `curl -X POST http://localhost:3000/authentication/guest`
  - expected response: HTTP `200` with an `authToken`
- If the API fails to start, check:
  - Postgres service status
  - values in `/api/.env`
  - whether `jira_development` database exists

## Running cypress end-to-end tests 🚥

- Set up development environment
- Create a database named `jira_test` and start the api with `cd api && NODE_ENV=test DB_DATABASE=jira_test python3 run.py`
- `cd client && npm run test:cypress`

## What's missing?

There are features missing from this showcase product which should exist in a real product:

### Migrations 🗄

We're currently using SQLAlchemy auto table creation (`db.create_all`) on application launch. It's fine in a showcase product or during early development while the product is not used by anyone, but before going live with a real product, we should introduce explicit database migrations (for example Alembic).

### Proper authentication system 🔐

We currently auto create an auth token and seed a project with issues and users for anyone who visits the API without valid credentials. In a real product we'd want to implement a proper [email and password authentication system](https://www.google.com/search?q=email+and+password+authentication+node+js&oq=email+and+password+authentication+node+js).

### Accessibility ♿

Not all components have properly defined [aria attributes](https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA), visual focus indicators etc. Most early stage companies tend to ignore this aspect of their product but in many cases they shouldn't, especially once their userbase starts growing.

### Unit/Integration tests 🧪

Both Client and API are currently tested through [end-to-end Cypress tests](https://github.com/oldboyxx/jira_clone/tree/master/client/cypress/integration). That's good enough for a relatively simple application such as this, even if it was a real product. However, as the app grows in complexity, it might be wise to start writing additional unit/integration tests.

## Contributing

I will not be accepting PR's on this repository. Feel free to fork and maintain your own version.

## License

[MIT](https://opensource.org/licenses/MIT)

<hr>

<h3>
  <a href="https://jira.ivorreic.com/">Visit the live app</a> |
  <a href="https://github.com/oldboyxx/jira_clone/tree/master/client">View client</a> |
  <a href="https://github.com/oldboyxx/jira_clone/tree/master/api">View API</a>
</h3>
