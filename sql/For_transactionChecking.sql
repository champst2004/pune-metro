-- selects all transactions from the given transaction table.
delimiter //
create procedure see_transaction(in card_ID int)
begin
select cardID as Card_id, transID as Transaction_id, (select name from stations where transactions.departID = stations.stationID) as departure_station , 
(select name from stations where transactions.arrivalID = stations.stationID) as arrival_station,
timed as date_and_time, amount as fare
from transactions where transactions.cardID = 2;
end //
delimiter ;
