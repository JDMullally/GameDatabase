USE game_schema;

Drop procedure if exists select_game_name_by_id;
Drop procedure if exists select_all_games;
Drop procedure if exists select_publisher_by_game_id;
Drop function if exists insert_game_with_publisher;
Drop procedure if exists select_game_id_by_name;
Drop function if exists remove_game_by_id;
Drop function if exists update_game_by_id;
Drop procedure if exists select_genres_by_game_id;
Drop procedure if exists get_all_publishers;
Drop procedure if exists get_all_genres;
Drop procedure if exists get_all_platforms;
Drop procedure if exists get_all_platforms_by_game_id;
Drop function if exists insert_platform;
Drop function if exists add_platform_to_game;
Drop function if exists add_genre_to_game;
Drop function if exists insert_genre;

#selects all games.
Delimiter //
create procedure select_all_games()
Begin
	Select game_id, game_name from game order by game_id;
end //

#This one is funky, I don't know if we will need it.
Delimiter //
create procedure select_game_id_by_name
(
input_game_name varchar(255)
)
Begin
	Select game_id from game where input_game_name = game_name;
end //

#game name getter
Delimiter //
create procedure select_game_name_by_id
(
input_game_id int
)
Begin
	Select game_name from game where game_id = input_game_id;
end //

Delimiter //
create procedure select_genres_by_game_id
(
input_game_id int
)
Begin
	SELECT genre_name, genre_id from genre join
	(SELECT genre_genre_id as ggid from game_defined_by_genre 
    where game_game_id = input_game_id) as g where genre.genre_id = g.ggid;
end //

#publisher getter
Delimiter //
create procedure select_publisher_by_game_id
(
input_game_id int
)
Begin
	SELECT distinct publisher.publisher_name
	FROM publisher
	INNER JOIN game ON 
    game.publisher_id=publisher.publisher_id 
    AND input_game_id = game.game_id;
end //

#insert function returns a 1 on success and a 0 on failure
Delimiter //
create function insert_game_with_publisher
(
input_game_name nvarchar(255),
input_game_year int,
input_game_sales double,
input_game_pub_id int
)
Returns int
READS SQL DATA
Begin
	declare table_exists int;
    
	SELECT COUNT(*) into table_exists FROM game WHERE EXISTS
	(SELECT * FROM game WHERE game_name=input_game_name);
	
    IF table_exists = 0 THEN
	INSERT INTO game (game_name, year, global_sales, publisher_id)
		VALUES (input_game_name, input_game_year, input_game_sales, input_game_pub_id);
        RETURN 1;
	END IF;
	IF table_exists > 0 THEN
		RETURN 0;
	END IF;
end //

#delete function returns a 1 on success and a 0 on failure
Delimiter //
create function remove_game_by_id
(
input_game_id int
)
Returns int
READS SQL DATA
Begin
declare table_exists int;

SELECT COUNT(*) into table_exists FROM game WHERE EXISTS
(SELECT * FROM game WHERE game_id=input_game_id);

	IF table_exists > 0 THEN
	DELETE FROM game WHERE game_id=input_game_id;
    RETURN 1;
	end if;
    IF table_exists = 0 THEN
    RETURN 0;
    end if;
end //

#function updats game's name.  Returns a 1 on a success and 0 on a failure.

Delimiter //
create function update_game_by_id
(
input_game_id int,
input_game_name varchar(255)
)
Returns int
READS SQL DATA
Begin
declare table_exists int;

SELECT COUNT(*) into table_exists FROM game WHERE EXISTS
(SELECT * FROM game WHERE game_id=input_game_id);

	IF table_exists > 0 THEN
    UPDATE game
	SET game_name = input_game_name
	WHERE input_game_id = game_id;
    RETURN 1;
	end if;
    IF table_exists = 0 THEN
    RETURN 0;
    end if;
end //


#get_all_publisher_ids
Delimiter //
create procedure get_all_publishers()
Begin
	Select publisher_name, publisher_id from publisher order by publisher_id;
end //


#get_all_publisher_ids
Delimiter //
create procedure get_all_genres()
Begin
	Select genre_id, genre_name from genre order by genre_id;
end //

Delimiter //
create procedure get_all_platforms()
Begin
	Select platform_id, platform_name from platform order by platform_id;
end //

Delimiter //
create function insert_platform
(
input_platform_name nvarchar(255)
)
Returns int
READS SQL DATA
Begin
	declare table_exists int;
    
	SELECT COUNT(*) into table_exists FROM platplatform_nameform WHERE EXISTS
	(SELECT * FROM platform WHERE platform_name=input_platform_name);
	
    IF table_exists = 0 THEN
	INSERT INTO platform (platform_name)
		VALUES (input_platform_name);
        RETURN 1;
	END IF;
	IF table_exists > 0 THEN
		RETURN 0;
	END IF;
end //

Delimiter //
create function insert_genre
(
input_genre_name nvarchar(255)
)
Returns int
READS SQL DATA
Begin
	declare table_exists int;
    
	SELECT COUNT(*) into table_exists FROM genre WHERE EXISTS
	(SELECT * FROM genre WHERE genre_name=input_genre_name);
	
    IF table_exists = 0 THEN
	INSERT INTO genre (genre_name)
		VALUES (input_genre_name);
        RETURN 1;
	END IF;
	IF table_exists > 0 THEN
		RETURN 0;
	END IF;
end //


Delimiter //
create procedure get_all_platforms_by_game_id
(
input_game_id int
)
Begin
	SELECT platform_id, platform_name from platform join
	(SELECT platform_platform_id as ppid from game_hosted_on_platform
    where game_game_id = input_game_id) as g where platform.platform_id = g.ppid;
end //


Delimiter //
create function add_genre_to_game
(
input_genre_id int,
input_game_id int
)
Returns int
READS SQL DATA
Begin
	declare genre_exists int;
    declare game_exists int;
    
	SELECT COUNT(*) into genre_exists FROM genre WHERE EXISTS
	(SELECT * FROM genre WHERE genre_id=input_genre_id);
    
    SELECT COUNT(*) into game_exists FROM game WHERE EXISTS
	(SELECT * FROM game WHERE game_id=input_game_id);
	
    IF genre_exists > 0 AND game_exists > 0 THEN
	INSERT INTO game_defined_by_genre (genre_genre_id,game_game_id)
		VALUES (input_genre_id, input_game_id);
        RETURN 1;
	END IF;
	IF genre_exists = 0 OR game_exists = 0 THEN
		RETURN 0;
	END IF;
end //


Delimiter //
create function add_platform_to_game
(
input_platform_id int,
input_game_id int
)
Returns int
READS SQL DATA
Begin
	declare platform_exists int;
    declare game_exists int;
    
	SELECT COUNT(*) into platform_exists FROM platform WHERE EXISTS
	(SELECT * FROM platform WHERE platform_id=input_platform_id);
    
    SELECT COUNT(*) into game_exists FROM game WHERE EXISTS
	(SELECT * FROM game WHERE game_id=input_game_id);
	
    IF platform_exists > 0 AND game_exists > 0 THEN
	INSERT INTO game_hosted_on_platform (platform_platform_id,game_game_id)
		VALUES (input_platform_id, input_game_id);
        RETURN 1;
	END IF;
	IF platform_exists = 0 OR game_exists = 0 THEN
		RETURN 0;
	END IF;
end //





#These calls and selects all work

# Select `game_schema`.`add_platform_to_game`(1,2);
#Call `game_schema`.`get_all_genres`();
# Call `game_schema`.`get_all_platforms_by_game_id`(26);
#Select `game_schema`.`insert_platform`("Bonk Time Rush");
# CALL `game_schema`.`get_all_platforms`();
#CALL `game_schema`.`select_game_name_by_id`(3);
#CALL `game_schema`.`select_all_games`();
#CALL `game_schema`.`select_publisher_by_game_id`(1);
#SELECT `game_schema`.`insert_game_with_publisher`("BinkTown", 2007, 88.8, 1);
#SELECT `game_schema`.`insert_game_with_publisher`("Bink City", 2008, 188.8, 1);
#SELECT `game_schema`.`remove_game_by_id`(29);
#SELECT `game_schema`.`update_game_by_id`(45, "BonkCity");
#CALL `game_schema`.`select_genres_by_game_id`(3);
