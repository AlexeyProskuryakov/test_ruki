create database test_ruki;
create user test_ruki_manager with password '100500';
grant all privileges on database test_ruki to test_ruki_manager;