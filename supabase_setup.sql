-- MeeGame: thống kê lượt bấm nút Chơi trên toàn bộ thiết bị
-- Chạy toàn bộ file này trong Supabase Dashboard > SQL Editor > New query.

create table if not exists public.game_play_stats (
  game_url text primary key,
  game_name text not null default '',
  play_count bigint not null default 0 check (play_count >= 0),
  updated_at timestamptz not null default now()
);

alter table public.game_play_stats enable row level security;

-- Ai cũng có thể đọc số lượt để trang GitHub Pages hiển thị thứ hạng.
drop policy if exists "Public can read MeeGame play stats" on public.game_play_stats;
create policy "Public can read MeeGame play stats"
  on public.game_play_stats for select
  to anon, authenticated
  using (true);

grant select on public.game_play_stats to anon, authenticated;

-- Chỉ tăng bộ đếm qua RPC để lượt chơi được cộng nguyên tử, tránh ghi đè khi nhiều người bấm cùng lúc.
create or replace function public.increment_game_play(p_game_url text, p_game_name text)
returns bigint
language plpgsql
security definer
set search_path = public
as $$
declare new_count bigint;
begin
  if p_game_url is null or length(p_game_url) > 2048 or p_game_url !~ '^https?://' then
    raise exception 'Invalid game URL';
  end if;
  insert into public.game_play_stats (game_url, game_name, play_count, updated_at)
  values (p_game_url, coalesce(nullif(left(p_game_name, 200), ''), p_game_url), 1, now())
  on conflict (game_url) do update
    set play_count = public.game_play_stats.play_count + 1,
        game_name = coalesce(nullif(left(excluded.game_name, 200), ''), public.game_play_stats.game_name),
        updated_at = now()
  returning play_count into new_count;
  return new_count;
end;
$$;

revoke all on function public.increment_game_play(text, text) from public;
grant execute on function public.increment_game_play(text, text) to anon, authenticated;
