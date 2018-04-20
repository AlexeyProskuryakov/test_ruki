drop table if exists users cascade;
drop table if exists phones;
drop table if exists orders;
drop sequence if exists users_sequence;

BEGIN;
create sequence users_sequence start 1 increment 1;

create table users (
  user_id     serial primary key
);

create table phones (
   phone_number bigint,
   user_id int not null references users (user_id) on delete cascade,
   primary key (phone_number)
);

create table orders (
  order_id    serial primary key,
  details     text,
  user_id int not null references users (user_id) on delete cascade
);
COMMIT;