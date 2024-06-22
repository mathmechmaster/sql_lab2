use sql_lab2;

alter table book_manager drop mpass;
alter table student drop spass;

#存储管理员/学生密码
create table user(
	id varchar(20) primary key, #管理员/学生的id
	is_manager bool, #为1——是管理员
    password blob	#密码
);