#当删除user表的成员时，同步删除对应student/book_manager表的成员;如果是student,还要删除对应borrow/reserve/violation表
#设计存储过程
#error_code:为0——没有错误，为1——试图删除high_manager,为2——不存在对应表项
Drop procedure delete_user;
drop function search_book;
Delimiter //
create procedure delete_user(
	IN delete_id varchar(20),
    OUT error_code int
)
BEGIN
	set error_code = 0;
	if exists(select * from high_manager where manager_id = delete_id) then
		set error_code = 1;
	elseif exists(select * from book_manager where manager_id = delete_id) then
		delete from book_manager where manager_id = delete_id;
		delete from user where id = delete_id;
		set error_code = 0;
	elseif exists(select * from student where stu_id = delete_id) then
		delete from borrow where stu_id = delete_id;
        delete from reserve where stu_id = delete_id;
        delete from violation where stu_id = delete_id;
		delete from student where stu_id = delete_id;
		delete from user where id = delete_id;
        set error_code = 0;
    end if;
END //

#用下面的函数查询book_info中的特定表项，输入查询字符串，任何相关表项都返回
#对于ISBN.必须完全符合
create function search_book(se_string varchar(200))
returns varchar(1000)
Reads SQL data
BEGIN
	return(
	select group_concat(bid) from book_info
        where ISBN = se_string 
        or bname like concat('%',se_string,'%')
		or author like concat('%',se_string,'%')
        or publisher like concat('%',se_string,'%')
        or btype like concat('%',se_string,'%')
    );
END //
Delimiter ;

drop trigger borrow_book;
Delimiter //
Create Trigger borrow_book After Insert On borrow For Each Row
BEGIN
	Update book_info Set inventory = inventory - 1 Where book_info.bid = new.bid;
    #若存在预定，将对应预定表项删除
    delete from reserve where reserve.stu_id = new.stu_id and reserve.bid = new.bid ;
END //

Delimiter ;

drop event violation_update ;
Delimiter //
Create Event if not exists violation_update 
On Schedule Every 10 Second 
ON COMPLETION PRESERVE 
Do BEGIN
	SET SQL_SAFE_UPDATES = 0;
	insert into violation(stu_id,bid,borrow_date,due_date,id) select stu_id,bid,borrow_date,due_date,id from borrow where due_date < curdate() and return_Date is null;
    SET SQL_SAFE_UPDATES = 1;
END //

Delimiter ;


