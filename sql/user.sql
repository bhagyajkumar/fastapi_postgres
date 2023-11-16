--creates the user table

create table "users" (id UUID primary key, username varchar(50), email varchar(150), password_hash v
archar(500));
