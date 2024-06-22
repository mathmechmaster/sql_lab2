use sql_lab2;

create table book_info(
	bid varchar(20) primary key,
    ISBN varchar(20),
    bname varchar(100),
    author varchar(100),
    publisher varchar(100), #出版社
	publish_date date,	#出版日期
    btype varchar(20),	#图书类别
    inventory integer,	#库存数量
    store_loc varchar(200), #存放位置
    book_pic varchar(200)	#图书图片信息
);

create table book_manager(
	manager_id varchar(20) primary key,
    manager_name varchar(20),
    gender varchar(10), #性别
    phone_num varchar(20), #联系电话
    email varchar(64), #邮箱
    mpass blob #管理员密码
);

create table high_manager(	#高级管理员
	manager_id varchar(20) primary key,
    constraint K_manager foreign key(manager_id) references book_manager(manager_id)
);

create table student(
	stu_id varchar(20) primary key,
    stu_name varchar(20),
    gender varchar(10), #性别
    grade varchar(16), #年级
    major varchar(30), #专业
    phone_num varchar(20), #联系电话
    email varchar(64), #邮箱
    spass blob #学生密码
);

create table borrow(
	stu_id varchar(20),
    bid varchar(20),
	borrow_date date,
    due_date date, #应还日期
    return_Date date,
    constraint PK primary key(stu_id,bid,borrow_date),
    constraint K_book foreign key(bid) references book_info(bid),
    constraint K_stu foreign key(stu_id) references student(stu_id)
);

create table violation(	#借阅违规信息
	stu_id varchar(20),
    bid varchar(20),
	borrow_date date,
    vio_day integer,	#违规天数
    fine decimal,	#罚款金额	
    constraint PK primary key(stu_id,bid,borrow_date)

);

create table reserve(
	stu_id varchar(20),
    bid varchar(20),
    reserve_Date date,
    reserve_status integer,	#预定状态
	constraint PK primary key(stu_id,bid,reserve_Date)
);

