DELIMITER //

CREATE FUNCTION fare(card_ID INT, dept_st varchar(100), arr_st varchar(100))
RETURNS DECIMAL(10,2)
DETERMINISTIC
BEGIN
    DECLARE baseFare DECIMAL(10,2);
    DECLARE discount DECIMAL(10,2);
    DECLARE cardType VARCHAR(25);
    declare ini int;
    declare fin int;
    select stationID into ini from stations where name = dept_st;
    select stationID into fin from stations where name = arr_st;
    -- Calculate base fare
    if ini - fin = -1 or ini - fin = 1 then set baseFare = 10.00;
elseif ini - fin = -2 or ini - fin = 2 then set baseFare = 15.00;
elseif ini - fin = -3 or ini - fin = 3 then set baseFare = 20.00;
elseif ini - fin = -4 or ini - fin = 4 then set baseFare = 25.00;
elseif ini - fin <= -4 or ini - fin >= 4 then set baseFare = 30.00;
else set baseFare = 0.00;
end if;

    -- Default no discount
    SET discount = 0.00;

    -- Check if cardID is provided
    IF cardID IS NOT NULL THEN
        SELECT cardtype INTO cardType FROM cards WHERE cards.cardID = card_ID;
        IF cardType = 'Student' THEN
            SET discount = 0.30;
        ELSEIF cardType = 'General' THEN
            SET discount = 0.10;
        END IF;
    END IF;

    RETURN baseFare - (baseFare * discount);
END //

DELIMITER ;


--  trigger for updating the balance of card after transaction
DELIMITER //

CREATE TRIGGER update_balance_after_booking
AFTER INSERT ON transactions
FOR EACH ROW
BEGIN
    UPDATE cards 
    SET balance = balance - NEW.amount 
    WHERE cards.cardID = NEW.cardID;
END //

DELIMITER ;

--function if balance is not sufficient 
delimiter //
create function insuff_balance(fare decimal(10,2), card_ID int) returns int
deterministic
begin
declare judgement int;
declare bal decimal(10,2);
select balance into bal from cards where cardID = card_ID;
if bal >= fare then set judgement = 1;
else set judgement = 0;
end if;
return judgement;
end//
delimiter ;

--inserting into transactions table without card:-
INSERT INTO transactions (departID, arrivalID, amount)
SELECT 
    (SELECT stationID FROM stations WHERE stations.name = "Vanaz"), 
    (SELECT stationID FROM stations WHERE stations.name = "Nal Stop"), 
    fare_without_card("Vanaz", "Nal Stop");


--inserting into transactions table with card:-
INSERT INTO transactions (departID, arrivalID, amount)
SELECT
    2,
    (SELECT stationID FROM stations WHERE stations.name = "Vanaz"), 
    (SELECT stationID FROM stations WHERE stations.name = "Nal Stop"), 
    fare_with_card("Vanaz", "Nal Stop");