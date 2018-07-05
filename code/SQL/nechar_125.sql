USE [BR_SHARD]
GO
/****** Object:  StoredProcedure [dbo].[_AddNewChar]    Script Date: 2018/6/25 23:51:48 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

ALTER PROCEDURE [dbo].[_AddNewChar]
	@UserJID			INT,        
	--@CharSlot			INT,        
	@RefCharID			INT,        
	@CharName			varchar (64),        
	@CharScale			tinyINT,        
	@StartRegionID			INT,        
	@StartPos_X			real,        
	@StartPos_Y			real,        
	@StartPos_Z			real,        
	@DefaultTeleport	INT,        
	@RefMailID			INT,        
	@RefPantsID			INT,        
	@RefBootsID			INT,        
	@RefWeaponID		INT,        
	@RefShield			INT,        
	@DurMail			tinyINT,        
	@DurPants			tinyINT,        
	@DurBoots			tinyINT,        
	@DurWeapon			tinyINT,        
	@DurShield			tinyINT,        
	@DefaultArrow		INT        
AS    
    
SET NOCOUNT ON      

	DECLARE @Slot  INT        
	DECLARE @temp  INT        
	        
	DECLARE @NewCharID  INT        
	SET @NewCharID = 0        
       
       
	-----------------------------------------------------------------------------        
	-- 1. Ä³¸¯ÅÍ ½½·Ô ³Ñ¹ö°¡ validÇÑ °ÍÀÎÁö, ±×¸®°í ºó½½·ÔÀÌ ¸Â´ÂÁö ¸ÕÀú Ã¼Å©ÇÑ´Ù.        
	-----------------------------------------------------------------------------        
	     
	-- start by novice.        
	SELECT @temp = count(CharID) FROM _User WITH (NOLOCK) WHERE UserJID = @UserJID        
	      
	IF (@temp >= 8)        
	BEGIN        
		-- ³Ê¹« ¸¹ÀÚ³ª        
		RETURN -2        
	END        
	-- finish by novice.        
      
	-----------------------------------------------------------------------------        
	-- 2. Ä³¸¯ÅÍ Ãß°¡ÇÏ±â        
	-----------------------------------------------------------------------------        
	IF (@CharScale > 68) -- 0100 0100 --> 68 ÀÌ´Ù!        
	BEGIN        
		-- Ä³¸¯ÅÍ »ý¼º ½ÇÆÐ! ½ºÄÉÀÏ °ªÀÌ ÀÌ»óÇÏ´Ù!         
		RETURN -3        
	END
        
	EXEC @temp = _IsExistingCharName @CharName        
	IF (@temp <> 0)        
	BEGIN        
		-- ÀÌ¹Ì »ç¿ëÁßÀÎ ÀÌ¸§ÀÌ¶ó´Âµ¥?        
		RETURN -4        
	END        
    
BEGIN TRANSACTION
    
-- ???????????? ?????????? ???????? WorldID?? 1???? ?? ???? ??????!        
INSERT INTO _Char (RefObjID, CharName16, Scale, Strength, Intellect, LatestRegion,PosX, PosY, PosZ, AppointedTeleport, InventorySize,        
LastLogout, CurLevel, MaxLevel, RemainGold, RemainStatPoint, RemainSkillPoint, HP, MP, JobLvl_Trader, JobLvl_Hunter, JobLvl_Robber, WorldID)        
VALUES (@RefCharID, @CharName, @CharScale, 20, 20, @StartRegionID, @StartPos_X, @StartPos_Y, @StartPos_Z, @DefaultTeleport, 90,        
GetDate(), 1, 1, 0, 0, 0, 200,200, 1, 1, 1, 1)        
       
	SET @NewCharID = @@IDENTITY        
	IF (@@ERROR <> 0 OR @@ROWCOUNT = 0)        
	BEGIN        
		-- Ä³¸¯ÅÍ »ý¼º ½ÇÆÐ!        
		ROLLBACK TRANSACTION        
		RETURN -5        
	END        
	    
	       
	-- start by novice.        
	-- ÀÌÁ¦ Slot ¾È¾´´Ù.. ±×³É Insert ¸¸..        
	INSERT INTO _User VALUES (@UserJID, @NewCharID)        
	-- finish by novice.        
      
      
	 -----------------------------------------------------------------------------        
	 -- 3-1. Àåºñ ½½·Ô Ã¤¿ì±â        
	 -- [ÀÎº¥Åä¸® ½½·Ô 96°³] + [Àåºñ½½·Ô 13°³] <- ÀÎº¥Åä¸® È®Àå ¼­ºñ½º ÈÄ 48°³¿¡¼­ 96°³·Î Áõ°¡!!!(woos0)
	 -----------------------------------------------------------------------------        
	 --PATCH WARNING!!!PATCH WARNING!!!PATCH WARNING!!!PATCH WARNING!!!PATCH WARNING!!!PATCH WARNING!!!PATCH WARNING!!!PATCH WARNING!!!PATCH WARNING!!!        
	 INSERT INTO _Inventory(CharID, Slot, ItemID)        
	  SELECT @NewCharID, cnt, 0        
	   FROM _RefDummySlot with( nolock )       
	    WHERE cnt < 109        

	      
	IF (@@ERROR <> 0)        
	BEGIN        
		-- ÀÎº¥Åä¸® »ý¼º ½ÇÆÐ!        
		ROLLBACK TRANSACTION        
		RETURN -7         
	END        

	--PATCH WARNING!!!PATCH WARNING!!!PATCH WARNING!!!PATCH WARNING!!!PATCH WARNING!!!PATCH WARNING!!!PATCH WARNING!!!PATCH WARNING!!!PATCH WARNING!!!        
	       
	
	-----------------------------------------------------------------------------        
	 -- 3-2. ¾Æ¹ÙÅ¸ Inventory ½½·Ô Ã¤¿ì±â        
	 -- [¾Æ¹ÙÅ¸ ÀÎº¥Åä¸® ½½·Ô 5°³]
	 -- APPLY_AVATAR_SYSTEMÀÌ Àû¿ëµÇ¸é¼­ Ãß°¡µÇ´Â ºÎºÐ
	 -----------------------------------------------------------------------------        
	 --PATCH WARNING!!!PATCH WARNING!!!PATCH WARNING!!!PATCH WARNING!!!PATCH WARNING!!!PATCH WARNING!!!PATCH WARNING!!!PATCH WARNING!!!PATCH WARNING!!!        
	 INSERT INTO _InventoryForAvatar(CharID, Slot, ItemID)        
	  SELECT @NewCharID, cnt, 0
	   FROM _RefDummySlot with( nolock )       
	    WHERE cnt < 5

	      
	IF (@@ERROR <> 0)        
	BEGIN        
		-- ¾Æ¹ÙÅ¸ ÀÎº¥Åä¸® »ý¼º ½ÇÆÐ!        
		ROLLBACK TRANSACTION        
		RETURN -14
	END        
	--PATCH WARNING!!!PATCH WARNING!!!PATCH WARNING!!!PATCH WARNING!!!PATCH WARNING!!!PATCH WARNING!!!PATCH WARNING!!!PATCH WARNING!!!PATCH WARNING!!!        
	      
	-----------------------------------------------------------------------------        
	-- default skill³Ö¾îÁÖ±â        
	-----------------------------------------------------------------------------        
	DECLARE @country tinyINT        
	EXEC @country = _GetObjCountry @RefCharID        
	       
	INSERT INTO _CharSkillMastery (CharID, MasteryID, Level)        
	SELECT @NewCharID, MasteryID, 0        
	FROM _RefCharDefault_SkillMastery  with(nolock)      
	WHERE Race = @country or Race = 3        
	IF (@@error <> 0)        
	BEGIN        
		ROLLBACK TRANSACTION        
		RETURN -15        
	END        
	INSERT INTO _CharSkill (CharID,SkillID,Enable)        
	SELECT @NewCharID, SkillID, 1        
	FROM  _RefCharDefault_Skill  with(nolock)      
	WHERE Race = @country or Race = 3        
	IF (@@error <> 0)        
	BEGIN        
		ROLLBACK TRANSACTION        
		RETURN -16        
	END        
	-----------------------------------------------------------------------------        
	-- ±âº» Äù½ºÆ® ³Ö¾îÁÖ±â
	-----------------------------------------------------------------------------        
	INSERT INTO _CharQuest (CharID, QuestID, Status, AchievementCount, StartTime, EndTime, QuestData1, QuestData2)        
	SELECT @NewCharID, ID, 1, 0, getdate(), getdate(), 0, 0        
	FROM _RefQuest
	WHERE CodeName in (SELECT CodeName FROM _RefCharDefault_Quest  with(nolock) WHERE (Race = @country or Race = 3) and RequiredLevel = 1 and Service = 1)
	IF (@@error <> 0)
	BEGIN
		ROLLBACK TRANSACTION        
		RETURN -17        
	END    
	-----------------------------------------------------------------------------        
	-- Static Avatar Initial Record ³Ö±â        
	-----------------------------------------------------------------------------        
	INSERT INTO _StaticAvatar(CharID) values(@NewCharID)        
	IF (@@ERROR <> 0)        
	BEGIN        
		ROLLBACK TRANSACTION        
		RETURN -18        
	END         
	      
	-----------------------------------------------------------------------------        
	-- Trijob Ã¤¿ö³Ö±â!!!!!        
	-----------------------------------------------------------------------------        
	INSERT INTO _CharTrijob VALUES (@NewCharID, 0, 1, 0, 0, 0)        
	IF (@@ERROR <> 0)        
	BEGIN        
		-- ÀÎº¥Åä¸® »ý¼º ½ÇÆÐ!        
		ROLLBACK TRANSACTION        
		RETURN -19        
	END         
	      
    
	-----------------------------------------------------------------------------               
	----------------------------------------------------------------------------- 	 
      insert _TimedJob ( [CharID],[Category],[JobID],[TimeToKeep],[Data1],[Data2] ,[Data3],[Data4],[Data5],[Data6],[Data7],[Data8],[Serial64])
      values (@NewCharID,0,31858,1495526072,0,1,0,0,0,0,0,0,72339069015696862)  
     insert _TimedJob ( [CharID],[Category],[JobID],[TimeToKeep],[Data1],[Data2] ,[Data3],[Data4],[Data5],[Data6],[Data7],[Data8],[Serial64])
      values (@NewCharID,0,3977,1495526072,0,1,0,0,0,0,0,0,72339069015696862)  
     insert _TimedJob ( [CharID],[Category],[JobID],[TimeToKeep],[Data1],[Data2] ,[Data3],[Data4],[Data5],[Data6],[Data7],[Data8],[Serial64])
      values (@NewCharID,0,33808,1495526072,0,1,0,0,0,0,0,0,72339069015696862)
     insert _TimedJob ( [CharID],[Category],[JobID],[TimeToKeep],[Data1],[Data2] ,[Data3],[Data4],[Data5],[Data6],[Data7],[Data8],[Serial64])
      values (@NewCharID,0,33809,1495526072,0,1,0,0,0,0,0,0,72339069015696862)
     insert _TimedJob ( [CharID],[Category],[JobID],[TimeToKeep],[Data1],[Data2] ,[Data3],[Data4],[Data5],[Data6],[Data7],[Data8],[Serial64])
      values (@NewCharID,0,33810,1495526072,0,1,0,0,0,0,0,0,72339069015696862)  			    
	-----------------------------------------------------------------------------  
    -----------------------------------------------------------------------------        
	-- CharList¿¡ ID ³Ö¾îÁÖ±â        
	-----------------------------------------------------------------------------        
	INSERT _CharNameList VALUES(@CharName, @NewCharID)        
/*
exec _ADD_ITEM_EXTERN @CharName,'ITEM_ETC_E060118_60EXP_HELP',1,1        
exec _ADD_ITEM_EXTERN @CharName,'ITEM_ETC_E060118_100EXP_HELP',1,1        
exec _ADD_ITEM_EXTERN @CharName,'ITEM_ETC_SCROLL_RETURN_NEWBIE_01',20,1

-- #ifdef 2010. 07. 23 thailand new user Event
exec _ADD_ITEM_EXTERN @CharName,'ITEM_ETC_100EXP_BASIC', 3, 1
exec _ADD_ITEM_EXTERN @CharName,'ITEM_ETC_SPEED_UP_BASIC', 10, 1
exec _ADD_ITEM_EXTERN @CharName,'ITEM_QNO_RM_FLYSHIP2_2_02', 10, 1
-- #endif 2010. 07. 23 thailand new user Event
*/
UPDATE _Char SET RemainGold=1000000000, RemainSkillPoint=100000000 WHERE _Char.CharID = @NewCharID --pas 2	
INSERT INTO BR_Account.dbo.SK_Silk (JID, silk_own, silk_gift, silk_point) VALUES (@UserJID, 0 , 0, 0);      


-----------------------------------------------------------------------------        

	
exec _AddNewClientConfig @NewCharID  -- by novice...... for saving client configurations...        

EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_BLADE_13_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_BOW_13_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_EARRING_13_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_M_CLOTHES_13_AA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_M_CLOTHES_13_BA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_M_CLOTHES_13_CA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_M_CLOTHES_13_FA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_M_CLOTHES_13_HA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_M_CLOTHES_13_LA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_M_CLOTHES_13_SA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_M_HEAVY_13_AA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_M_HEAVY_13_BA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_M_HEAVY_13_CA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_M_HEAVY_13_FA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_M_HEAVY_13_HA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_M_HEAVY_13_LA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_M_HEAVY_13_SA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_M_LIGHT_13_AA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_M_LIGHT_13_BA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_M_LIGHT_13_CA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_M_LIGHT_13_FA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_M_LIGHT_13_HA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_M_LIGHT_13_LA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_M_LIGHT_13_SA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_NECKLACE_13_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_RING_13_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_RING_13_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_SHIELD_13_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_SPEAR_13_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_SWORD_13_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_TBLADE_13_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_W_CLOTHES_13_AA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_W_CLOTHES_13_BA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_W_CLOTHES_13_CA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_W_CLOTHES_13_FA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_W_CLOTHES_13_HA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_W_CLOTHES_13_LA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_W_CLOTHES_13_SA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_W_HEAVY_13_AA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_W_HEAVY_13_BA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_W_HEAVY_13_CA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_W_HEAVY_13_FA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_W_HEAVY_13_HA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_W_HEAVY_13_LA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_W_HEAVY_13_SA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_W_LIGHT_13_AA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_W_LIGHT_13_BA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_W_LIGHT_13_CA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_W_LIGHT_13_FA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_W_LIGHT_13_HA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_W_LIGHT_13_LA_C_RARE',255,12
EXEC _ADD_ITEM_EXTERN @CharName,'ITEM_CH_W_LIGHT_13_SA_C_RARE',255,12

DELETE FROM [BR_ACCOUNT].[dbo].[SK_Silk] where JID = @UserJID

INSERT INTO [BR_ACCOUNT].[dbo].[SK_Silk] VALUES (@UserJID,9999,9999,9999)

EXEC  _Dkchar @NewCharID

COMMIT TRANSACTION        
	      
RETURN @NewCharID

