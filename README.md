# Encore

Encore is a planned social movie-ranking web app that helps people track what they watch and discover what to watch next. Instead of assigning stars or numerical scores, users choose between two movies in head-to-head comparisons to build a personal ranked list.

## Goals

- Make movie preferences more expressive through direct comparisons.
- Let users record watched movies and write one editable review per movie.
- Support friendships, shared rankings, reviews, and comments.
- Recommend unseen movies using personal preferences and friends’ rankings.

## Current progress

This repository contains an early ranking prototype, a draft PostgreSQL schema for Supabase, and setup/design documentation. The React app, authentication integration, social features, recommendations, and deployment are upcoming work. Architecture decisions remain provisional until the next design milestone.

The proposed stack is **React** for the frontend, **Vercel** for hosting, and **Supabase Auth + PostgreSQL** for accounts and data. IMDb is the proposed movie-data provider, subject to confirming access and licensing.

## Repository layout

```text
README.md                         Project overview and entry point
docs/
  living-document.md              Evolving architecture, scope, risks, and milestones
  setup.md                        Prototype and local database setup instructions
prototype/
  ranking.py                      Interactive binary-insertion ranking experiment
  test_ranking.py                 Ranking correctness and comparison-count checks
supabase/
  migrations/
    20261014000000_initial.sql    Draft core tables and access policies
```

The [living document](docs/living-document.md) tracks the design as it develops. See the [setup guide](docs/setup.md) for resource setup and limitations.

## Try the ranking prototype

With Python 3.10 or newer installed, run these commands from the repository root:

```sh
python3 prototype/ranking.py
python3 -m unittest discover -s prototype -v
```

The prototype uses sample titles and runs in the terminal. It demonstrates ranking behavior without requiring a movie API or database; rankings are kept in memory for the session.
