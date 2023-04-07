alter session set "_ORACLE_SCRIPT"=true;
create user john identified by ipiheb60;
grant create session to john;
alter user john quota unlimited on users;
grant create procedure  to john;