-- Draft core schema. Apply with the local Supabase workflow in docs/setup.md.
-- Server-enforced ranking transactions and matchup limits are future work.

create table public.profiles (
  id uuid primary key references auth.users(id) on delete cascade,
  username text not null unique check (char_length(username) between 3 and 30),
  created_at timestamptz not null default now()
);

create table public.movies (
  id bigint generated always as identity primary key,
  provider text not null,
  provider_movie_id text not null,
  title text not null check (char_length(title) > 0),
  release_year integer,
  poster_url text,
  unique (provider, provider_movie_id)
);

create table public.watched_movies (
  user_id uuid not null references public.profiles(id) on delete cascade,
  movie_id bigint not null references public.movies(id) on delete restrict,
  watched_on date,
  rank_position integer check (rank_position > 0),
  created_at timestamptz not null default now(),
  primary key (user_id, movie_id),
  constraint unique_user_rank unique (user_id, rank_position)
    deferrable initially immediate
);

create table public.reviews (
  user_id uuid not null,
  movie_id bigint not null,
  body text not null check (char_length(body) between 1 and 10000),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  primary key (user_id, movie_id),
  foreign key (user_id, movie_id)
    references public.watched_movies(user_id, movie_id) on delete cascade
);

create function public.set_review_updated_at()
returns trigger language plpgsql set search_path = '' as $$
begin
  new.updated_at = now();
  return new;
end;
$$;

create trigger review_updated_at before update on public.reviews
for each row execute function public.set_review_updated_at();

alter table public.profiles enable row level security;
alter table public.movies enable row level security;
alter table public.watched_movies enable row level security;
alter table public.reviews enable row level security;

-- Make privileges explicit; policies further limit authenticated access.
revoke all on public.profiles, public.movies, public.watched_movies,
  public.reviews from anon, authenticated;
grant select, insert, update, delete on public.profiles,
  public.watched_movies, public.reviews to authenticated;
grant select on public.movies to authenticated;

create policy profiles_read on public.profiles
for select to authenticated using (true);
create policy profiles_insert on public.profiles
for insert to authenticated with check ((select auth.uid()) = id);
create policy profiles_update on public.profiles
for update to authenticated using ((select auth.uid()) = id)
with check ((select auth.uid()) = id);
create policy profiles_delete on public.profiles
for delete to authenticated using ((select auth.uid()) = id);

-- Movie metadata is written only by trusted administrative/server connections.
create policy movies_read on public.movies
for select to authenticated using (true);

-- Viewing history and rankings are private in this starter.
create policy watched_owner on public.watched_movies
for all to authenticated using ((select auth.uid()) = user_id)
with check ((select auth.uid()) = user_id);

-- Reviews are readable by signed-in users. Ownership controls every write.
create policy reviews_read on public.reviews
for select to authenticated using (true);
create policy reviews_insert on public.reviews
for insert to authenticated with check ((select auth.uid()) = user_id);
create policy reviews_update on public.reviews
for update to authenticated using ((select auth.uid()) = user_id)
with check ((select auth.uid()) = user_id);
create policy reviews_delete on public.reviews
for delete to authenticated using ((select auth.uid()) = user_id);
