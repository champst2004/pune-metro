delimiter //
create procedure get_balance(in user_id int) 
begin
select cards.cardID, cards.cardtype, cards.balance, cards.issuedate, ctype.discount_in_percent as discount_given
from cards join ctype on cards.cardtype = ctype.cardtype 
where cards.userID = user_id ;
end;
//
delimiter ;