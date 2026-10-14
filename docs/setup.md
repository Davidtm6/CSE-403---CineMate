# Development setup

## Ranking experiment

Install Python 3.10 or newer. From the repository root:

```sh
python3 prototype/ranking.py
python3 -m unittest discover -s prototype -v
```

No packages, credentials, or network access are required. Choose the preferred film in each matchup. Enter `q` to cancel; canceling does not change the list. The list lasts only for the current session.

## Local Supabase resources

Prerequisites: a running Docker-compatible container runtime and the [Supabase CLI](https://supabase.com/docs/guides/local-development/cli/getting-started). Follow the official installation instructions for your platform. With the global CLI installed, run from the repository root:

```sh
supabase init
supabase start
supabase db reset
```

`init` generates local configuration in `supabase/config.toml`. `start` launches local services. `db reset` recreates the **local** database and applies the supplied migration; it deletes local development data. Do not add remote-target flags to this command.

Open the Studio URL printed by the CLI and check that `profiles`, `movies`, `watched_movies`, and `reviews` exist. Use the local Auth tools to create test accounts. Then verify that an authenticated user can manage their own viewing records and reviews, cannot access another user’s private viewing history, and cannot write movie metadata. Populate sample movies through Studio’s administrative connection; provider writes are reserved for trusted server code.

The migration is an initial draft and has not been applied to a running database in this starter. Review and validate it before connecting an app. See the [official migration workflow](https://supabase.com/docs/guides/local-development/database-migrations).

Stop local services when finished:

```sh
supabase stop
```

## Frontend and hosted setup — next increment

The React app is not scaffolded yet. When the architecture is finalized:

1. Create a React frontend and connect it to a separate Supabase development project.
2. Configure Supabase email confirmation and allowed Auth redirect URLs.
3. Implement server-side movie search, ranking transactions, verified-email checks, and the 100-matchups-per-hour limit.
4. Add the browser-safe Supabase project URL and publishable key to frontend configuration. Keep Supabase secret/service-role credentials and movie-provider credentials exclusively in server environment variables.
5. Connect the GitHub repository to Vercel, set its frontend build settings, and add the deployed URL to Auth redirect settings.

No hosted accounts, paid API subscriptions, or deployment have been created by this starter. Commit reviewed local configuration and migrations to GitHub; keep environment files and credentials out of version control.
