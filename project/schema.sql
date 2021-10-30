-- 1. Open DB connection,
-- 2. create the DB based on defined schema (if doesn't already exist'),
-- 3. close connection

drop table if exists entries;
create table entries (
  id integer primary key autoincrement,
  title text not null,
  text text not null
);